/* Learner player: one slide at a time, optional narrated playback, captions and transcript.
 *
 * Deliberate behaviour, each for a reason:
 *   - Narration NEVER autoplays. Pressing Play starts the first narrated slide and then continues.
 *   - Auto-next waits a short wall-clock beat between slides so the learner can read, and that beat
 *     is shortened for prefers-reduced-motion (ai_qe has no such branch; this is our addition).
 *   - audio.currentTime is the only clock: captions, the seek bar and the time readout all derive
 *     from it, so nothing can drift.
 *   - A slide with no recording still navigates; the learner is told why the player is absent.
 *   - Progress is remembered per deck in localStorage and offered back on return.
 *   - If captions fail to load, playback still works and a Retry button plus the transcript remain.
 */
(() => {
  'use strict';

  const body = document.body;
  const slides = Array.from(document.querySelectorAll('.slide'));
  if (!slides.length || !window.APSNarrationMedia) return;

  const manifestPath = body.dataset.narrationManifest;
  const deckId = body.dataset.narrationDeck || 'deck';
  const siteBase = body.dataset.siteBase || '.';
  const progressKey = `aps:progress:${deckId}`;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  const els = {
    start: document.querySelector('[data-narration-start]'),
    prev: document.querySelector('[data-nav="prev"]'),
    next: document.querySelector('[data-nav="next"]'),
    picker: document.querySelector('[data-slide-picker]'),
    status: document.querySelector('.slide-status'),
    message: document.querySelector('.deck-message'),
    nav: document.querySelector('.deck-navigation'),
    present: document.querySelector('[data-present]'),
    reading: document.querySelector('[data-reading]'),
    notes: document.querySelector('[data-notes]'),
    drawer: document.querySelector('.deck-drawer'),
    drawerMeta: document.querySelector('[data-drawer-meta]'),
    drawerNotes: document.querySelector('[data-drawer-notes]'),
    closeDrawer: document.querySelector('[data-close-drawer]'),
  };

  let entries = {};
  let index = 0;
  let clip = null;                 // manifest entry for the current slide
  let cueList = [];
  let clipVersion = 0;
  let captionsOn = true;
  let audioFailed = false;
  let advanceTimer = 0;
  let pendingAdvance = null;
  let frame = 0;
  let panelEl = null;

  const audio = document.createElement('audio');
  audio.preload = 'none';
  audio.setAttribute('aria-label', 'Slide narration');
  audio.dataset.narrationAudio = '';

  const clock = seconds => {
    const value = Number.isFinite(seconds) ? Math.max(0, Math.floor(seconds)) : 0;
    return `${Math.floor(value / 60)}:${String(value % 60).padStart(2, '0')}`;
  };

  function assetURL(path) {
    if (typeof path !== 'string' || !path.trim()) return null;
    const base = new URL(siteBase.endsWith('/') ? siteBase : `${siteBase}/`, location.href);
    const url = new URL(path.replace(/^\//, ''), base);
    return ['http:', 'https:', 'file:'].includes(url.protocol) ? url.href : null;
  }

  /* ---------------------------------------------------------------- panel */

  function buildPanel() {
    const panel = document.createElement('section');
    panel.className = 'narration-panel';
    panel.setAttribute('aria-label', 'Slide narration, captions and transcript');
    panel.hidden = true;
    panel.innerHTML = `
      <div class="narration-caption" data-caption aria-label="Captions" aria-live="off"></div>
      <div class="narration-controls">
        <button type="button" data-play aria-label="Play narration">▶ Play</button>
        <button type="button" data-replay aria-label="Replay this slide's narration">↺ Replay</button>
        <label class="narration-seek"><span class="sr-only">Narration position</span>
          <input data-seek type="range" min="0" max="0" step="0.05" value="0" disabled></label>
        <span class="narration-time" data-time>0:00 / 0:00</span>
        <label class="narration-speed"><span class="sr-only">Narration speed</span>
          <select data-speed aria-label="Narration speed">
            <option value="0.75">0.75×</option><option value="1" selected>1×</option>
            <option value="1.25">1.25×</option><option value="1.5">1.5×</option>
          </select></label>
        <button type="button" data-cc aria-label="Captions" aria-pressed="true">CC</button>
        <label class="narration-auto"><input type="checkbox" data-auto checked> Auto-next</label>
      </div>
      <div class="narration-meta">
        <p data-status role="status" aria-live="polite"></p>
        <button type="button" data-retry hidden>Retry captions</button>
        <button type="button" data-transcript hidden>Transcript</button>
      </div>`;
    els.nav.before(panel);
    panel.append(audio);
    panelEl = panel;
    // Reserve the panel's height so the fixed bar never covers the bottom of a slide. The observer
    // path is debounced through rAF because mutating the observed element inside its own callback
    // would resize it again in the same cycle (the ai_qe lesson); `reservePanelHeight` is also called
    // directly when the panel is shown, so the reservation does not depend on a later animation frame.
    let resizeFrame = 0;
    if (window.ResizeObserver) {
      new ResizeObserver(() => {
        cancelAnimationFrame(resizeFrame);
        resizeFrame = requestAnimationFrame(reservePanelHeight);
      }).observe(panel);
    }
    const controls = Object.fromEntries(['play', 'replay', 'seek', 'time', 'speed', 'cc', 'auto',
      'caption', 'status', 'retry', 'transcript']
      .map(key => [key, panel.querySelector(`[data-${key}]`)]));
    controls.panel = panel;
    return controls;
  }
  const ui = buildPanel();

  // Everything between the top of the page and the bottom of the navigation strip, except the
  // slide itself: the header, the honesty badge, their margins, the panel gap and the nav. It is
  // measured rather than assumed because the badge only appears on preview decks, and a wrong
  // constant silently pushes the narration controls under the navigation strip.
  function fitChrome() {
    const root = document.documentElement;
    const slidesEl = document.querySelector('.slides');
    const gap = parseFloat(getComputedStyle(root).getPropertyValue('--narration-gap')) || 12;
    const navHeight = els.nav ? els.nav.getBoundingClientRect().height : 0;
    const slidesTop = slidesEl ? slidesEl.getBoundingClientRect().top : 0;
    const value = `${Math.ceil(slidesTop + gap * 2 + navHeight)}px`;  // gap above and below the panel
    if (root.style.getPropertyValue('--chrome-height') !== value) {
      root.style.setProperty('--chrome-height', value);
    }
  }

  function reservePanelHeight() {
    if (!panelEl) return;
    const root = document.documentElement;
    const height = panelEl.hidden ? '0px' : `${Math.ceil(panelEl.getBoundingClientRect().height)}px`;
    if (root.style.getPropertyValue('--narration-height') !== height) {
      root.style.setProperty('--narration-height', height);
    }
    fitChrome();
  }

  const announce = message => { ui.status.textContent = message; };
  const clearCaption = () => { ui.caption.textContent = ''; };

  function renderCaption() {
    if (!clip || !captionsOn || audioFailed || audio.seeking) { clearCaption(); return; }
    const cue = cueList.find(item => audio.currentTime >= item.start && audio.currentTime < item.end);
    const text = cue ? cue.text : '';
    if (ui.caption.textContent !== text) ui.caption.textContent = text;
  }

  function updateTime() {
    const duration = Number.isFinite(audio.duration) ? audio.duration : (clip ? clip.duration : 0) || 0;
    ui.seek.max = String(duration);
    ui.seek.disabled = !duration || audioFailed;
    ui.seek.value = String(Math.min(audio.currentTime || 0, duration));
    ui.seek.setAttribute('aria-valuetext', `${clock(audio.currentTime)} of ${clock(duration)}`);
    ui.time.textContent = `${clock(audio.currentTime)} / ${clock(duration)}`;
    renderCaption();
  }

  function tick() {
    updateTime();
    if (!audio.paused && !audio.ended) frame = requestAnimationFrame(tick);
  }

  function updatePlaying() {
    const playing = Boolean(advanceTimer) || (!audio.paused && !audio.ended);
    ui.play.textContent = audioFailed ? 'Retry audio' : playing ? 'Ⅱ Pause' : '▶ Play';
    ui.play.setAttribute('aria-label', audioFailed ? 'Retry narration audio' : playing ? 'Pause narration' : 'Play narration');
    if (els.start) {
      els.start.textContent = playing ? 'Ⅱ Pause narration' : '▶ Play narration';
      els.start.setAttribute('aria-pressed', String(playing));
    }
    cancelAnimationFrame(frame);
    if (playing && !advanceTimer) frame = requestAnimationFrame(tick);
  }

  /* ---------------------------------------------------------------- slides */

  function goTo(nextIndex, options = {}) {
    const clamped = Math.max(0, Math.min(slides.length - 1, nextIndex));
    stop();
    cancelAdvance();
    index = clamped;
    const reading = body.classList.contains('reading-view');
    slides.forEach((slide, i) => {
      slide.hidden = reading ? false : i !== index;
      if (i === index) {
        slide.setAttribute('aria-current', 'true');
        const title = slide.querySelector('h1, h2, h3')?.textContent?.trim()
          || `Slide ${index + 1}`;
        els.status.textContent = `Slide ${index + 1} of ${slides.length} — ${title}`;
      } else {
        slide.removeAttribute('aria-current');
      }
    });
    if (els.picker) els.picker.value = slides[index].id;
    if (options.scroll !== false) {
      const heading = slides[index].querySelector('h1, h2, h3');
      (heading || slides[index]).focus?.({ preventScroll: true });
      window.scrollTo({ top: 0, behavior: reduceMotion.matches ? 'auto' : 'smooth' });
    }
    try {
      history.replaceState(null, '', `#${slides[index].id}`);
      localStorage.setItem(progressKey, JSON.stringify({ slide: slides[index].id }));
    } catch (_) { /* private mode: navigation still works */ }
    recordUnit();
    loadClip();
  }

  // Unit progress: reaching the last slide of a unit marks it complete in the shared store, and
  // every slide records "where you left off" for the course home. Labs and knowledge checks are
  // completed on their own pages, not by reading their slide.
  let units = [];
  try { units = JSON.parse(body.dataset.units || '[]'); } catch (_) { units = []; }
  function recordUnit() {
    const P = window.APSProgress;
    if (!P) return;
    const n = index + 1;
    const unit = units.find(u => n >= u.first && n <= u.last);
    const where = `${deckId}.html#${slides[index].id}`;
    if (unit) {
      if (n === unit.last && unit.id !== 'lab' && unit.id !== 'quiz') P.setUnit(`${deckId}:${unit.id}`, true);
      P.setLast(where, `${body.dataset.deckLabel || deckId} — ${unit.label} (slide ${n} of ${slides.length})`);
    } else {
      P.setLast(where, `${body.dataset.deckLabel || deckId} — slide ${n} of ${slides.length}`);
    }
  }

  const move = delta => goTo(index + delta);

  function loadClip() {
    const slide = slides[index];
    clipVersion += 1;
    cueList = [];
    clearCaption();
    audio.removeAttribute('src');
    audio.load();
    audioFailed = false;
    clip = entries[slide.id] && entries[slide.id].audio && entries[slide.id].captions
      ? entries[slide.id] : null;
    // The panel is the only place captions, the transcript and playback controls live, so it must
    // be visible whenever a recording exists. It starts hidden to avoid an empty bar on load.
    ui.panel.hidden = !clip;
    reservePanelHeight();
    requestAnimationFrame(reservePanelHeight);
    const hasCaptions = Boolean(clip);
    ui.transcript.hidden = !(clip && clip.transcript);
    ui.retry.hidden = true;
    ui.cc.disabled = !hasCaptions;
    ui.play.disabled = !clip;
    if (!clip) {
      els.message.textContent = entries && Object.keys(entries).length
        ? 'This slide has no recording. Use the slide controls, or press Play on a narrated slide.'
        : '';
      updatePlaying();
      updateTime();
      return;
    }
    els.message.textContent = '';
    // No source is attached until the learner presses Play. A 233-slide site should not open a
    // media request per slide the reader never listens to, and a pending load also makes headless
    // verification non-deterministic.
    updatePlaying();
    updateTime();
    announce('Narration ready · Press Play to listen.');
    loadCaptions(clip, clipVersion);
  }

  async function loadCaptions(entry, version) {
    cueList = [];
    clearCaption();
    ui.retry.hidden = true;
    try {
      const url = assetURL(entry.captions);
      if (!url) throw new Error('bad caption url');
      const response = await fetch(url);
      if (!response.ok) throw new Error('caption request failed');
      const parsed = window.APSNarrationMedia.parseCaptions(await response.text());
      if (version !== clipVersion) return;
      cueList = parsed;
      ui.cc.disabled = false;
      renderCaption();
      if (!audioFailed) announce('Narration with synchronized captions.');
    } catch (error) {
      if (version !== clipVersion) return;
      ui.retry.hidden = false;
      announce('Captions could not load. Retry, or read the transcript.');
    }
  }

  /* ---------------------------------------------------------------- playback */

  function ensureSource() {
    if (!clip || audio.getAttribute('src')) return;
    audio.src = assetURL(clip.audio);
    audio.playbackRate = Number(ui.speed.value);
    updateTime();
  }

  function play() {
    if (!clip || document.hidden) return;
    if (pendingAdvance) { window.APSNarrationMedia.claim(audio); beginAdvance(); return; }
    if (audioFailed) { audioFailed = false; audio.removeAttribute('src'); }
    ensureSource();
    if (audio.ended) audio.currentTime = 0;
    const version = clipVersion;
    window.APSNarrationMedia.play(audio).catch(error => {
      if (version !== clipVersion || error.name === 'AbortError') return;
      updatePlaying();
      announce(audio.error ? 'Audio could not load. Select Retry audio to try again.'
                           : 'Playback was paused by your browser. Select Play to continue.');
    });
  }

  function stop() {
    cancelAdvance();
    audio.pause();
    cancelAnimationFrame(frame);
    updatePlaying();
  }

  function cancelAdvance() {
    clearTimeout(advanceTimer);
    advanceTimer = 0;
    pendingAdvance = null;
  }

  function beginAdvance() {
    if (!pendingAdvance || advanceTimer) return;   // one timer only, ever
    advanceTimer = setTimeout(() => {
      const expected = pendingAdvance;
      advanceTimer = 0;
      pendingAdvance = null;
      if (!expected || !window.APSNarrationMedia.owns(audio) || index !== expected.index
          || document.hidden || document.querySelector('dialog[open]') || !ui.auto.checked) {
        updatePlaying();
        return;
      }
      goTo(expected.index + 1, { scroll: true });
      if (entries[slides[index].id]) play();
    }, pendingAdvance.remaining);
    updatePlaying();
  }

  function pausePlayback() {
    if (advanceTimer) {
      clearTimeout(advanceTimer);
      advanceTimer = 0;
      pendingAdvance = null;
      updatePlaying();
      announce('Paused between slides.');
    } else {
      stop();
    }
  }

  function onEnded() {
    const nextIndex = index + 1;
    if (nextIndex >= slides.length) {
      announce('End of deck. Select a slide to review, or press Replay.');
      updatePlaying();
      try { localStorage.setItem(progressKey, JSON.stringify({ slide: slides[index].id, done: true })); } catch (_) {}
      return;
    }
    const gap = reduceMotion.matches ? 700 : 2000;
    pendingAdvance = { index, remaining: gap };
    beginAdvance();
  }

  /* ---------------------------------------------------------------- wiring */

  audio.addEventListener('loadedmetadata', updateTime);
  audio.addEventListener('durationchange', updateTime);
  audio.addEventListener('timeupdate', updateTime);
  audio.addEventListener('seeked', updateTime);
  audio.addEventListener('seeking', clearCaption);
  audio.addEventListener('play', () => { updatePlaying(); announce('Playing narration.'); });
  audio.addEventListener('pause', updatePlaying);
  audio.addEventListener('ended', onEnded);
  audio.addEventListener('error', () => {
    if (!audio.getAttribute('src')) return;
    audioFailed = true;
    updatePlaying();
    announce('Audio could not load. Select Retry audio to try again.');
  });

  els.prev?.addEventListener('click', () => move(-1));
  els.next?.addEventListener('click', () => move(1));
  els.picker?.addEventListener('change', event => {
    const target = slides.findIndex(slide => slide.id === event.target.value);
    if (target >= 0) goTo(target);
  });
  els.start?.addEventListener('click', () => {
    if (advanceTimer || (!audio.paused && !audio.ended)) { pausePlayback(); return; }
    play();
  });
  ui.play.addEventListener('click', () => (advanceTimer || (!audio.paused && !audio.ended)) ? pausePlayback() : play());
  ui.replay.addEventListener('click', () => {
    if (!clip) return;
    cancelAdvance();
    clearCaption();
    ensureSource();
    audio.currentTime = 0;
    play();
  });
  ui.seek.addEventListener('input', () => {
    cancelAdvance();
    clearCaption();
    ensureSource();
    audio.currentTime = Number(ui.seek.value);
    updateTime();
    updatePlaying();
  });
  ui.speed.addEventListener('change', () => { audio.playbackRate = Number(ui.speed.value); });
  ui.cc.addEventListener('click', () => {
    captionsOn = !captionsOn;
    ui.cc.setAttribute('aria-pressed', String(captionsOn));
    renderCaption();
  });
  ui.retry.addEventListener('click', () => {
    if (!clip) return;
    if (audioFailed) { audioFailed = false; audio.removeAttribute('src'); ensureSource(); }
    loadCaptions(clip, clipVersion);
  });
  ui.auto.addEventListener('change', () => {
    if (!ui.auto.checked && pendingAdvance) { cancelAdvance(); updatePlaying(); announce('Auto-next off.'); }
  });
  ui.transcript.addEventListener('click', () => {
    if (!clip) return;
    stop();
    const dialog = document.createElement('dialog');
    dialog.className = 'narration-transcript';
    dialog.setAttribute('aria-label', 'Slide narration transcript');
    const heading = document.createElement('h2');
    heading.textContent = 'Narration transcript';
    const meta = document.createElement('p');
    meta.className = 'narration-provenance';
    meta.textContent = [clip.voice, clip.caption_method].filter(Boolean).join(' · ');
    const text = document.createElement('p');
    text.className = 'narration-text';
    text.textContent = clip.transcript || 'No transcript recorded for this slide.';
    const close = document.createElement('button');
    close.type = 'button';
    close.textContent = 'Close transcript';
    close.addEventListener('click', () => dialog.close());
    dialog.addEventListener('close', () => { dialog.remove(); ui.transcript.focus(); });
    dialog.append(heading, meta, text, close);
    document.body.append(dialog);
    dialog.showModal();
  });

  /* ------------------------------------------------- present, read, notes */

  // Presentation mode: full screen, chrome trimmed, the slide centred. The frame maths in the
  // stylesheet already give back the narration panel's height, so the slide stays 16:9 either way.
  async function enterPresentation() {
    body.classList.add('presentation-mode');
    if (els.present) els.present.setAttribute('aria-pressed', 'true');
    requestAnimationFrame(reservePanelHeight);
    try {
      if (!document.fullscreenElement && document.documentElement.requestFullscreen) {
        await document.documentElement.requestFullscreen();
      }
    } catch (_) { /* full screen is a bonus; the mode still applies without it */ }
    announce('Presentation mode. Press Escape to leave.');
  }

  function leavePresentation() {
    body.classList.remove('presentation-mode');
    if (els.present) els.present.setAttribute('aria-pressed', 'false');
    requestAnimationFrame(reservePanelHeight);
  }

  function togglePresentation() {
    if (body.classList.contains('presentation-mode')) leavePresentation(); else enterPresentation();
  }

  if (els.present) els.present.addEventListener('click', togglePresentation);
  window.addEventListener('resize', () => requestAnimationFrame(reservePanelHeight));
  document.addEventListener('fullscreenchange', () => {
    // Leaving full screen with Esc must not strand the page in presentation styling.
    if (!document.fullscreenElement) leavePresentation();
  });

  function setReading(on) {
    body.classList.toggle('reading-view', on);
    if (els.reading) els.reading.setAttribute('aria-pressed', String(on));
    goTo(index, { scroll: false });
    announce(on ? 'Reading view: every slide is shown.' : 'One slide at a time.');
  }

  if (els.reading) els.reading.addEventListener('click', () => setReading(!body.classList.contains('reading-view')));

  function openNotes() {
    if (!els.drawer || !slides[index]) return;
    const slide = slides[index];
    const source = slide.querySelector('.slide-notes-source');
    const notes = source ? source.textContent.trim() : '';
    if (els.drawerMeta) {
      const heading = slide.querySelector('h2');
      els.drawerMeta.textContent = [heading && heading.textContent.trim(),
                                    `Slide ${index + 1} of ${slides.length}`]
        .filter(Boolean).join(' · ');
    }
    if (els.drawerNotes) {
      els.drawerNotes.textContent = notes || 'No speaker notes for this slide.';
      els.drawerNotes.classList.toggle('drawer-empty', !notes);
    }
    els.drawer.showModal();
  }

  if (els.notes) els.notes.addEventListener('click', openNotes);
  if (els.closeDrawer) els.closeDrawer.addEventListener('click', () => els.drawer.close());

  document.addEventListener('keydown', event => {
    if (document.querySelector('dialog[open]')) return;
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    const tag = (event.target.tagName || '').toLowerCase();
    if (['input', 'select', 'textarea', 'button', 'a'].includes(tag)) return;
    if (event.key === 'ArrowRight' || event.key === 'PageDown' || event.key === ' ') { move(1); event.preventDefault(); }
    else if (event.key === 'ArrowLeft' || event.key === 'PageUp') { move(-1); event.preventDefault(); }
    else if (event.key === 'Home') { goTo(0); event.preventDefault(); }
    else if (event.key === 'End') { goTo(slides.length - 1); event.preventDefault(); }
    else if (event.key === 'p' || event.key === 'P') { togglePresentation(); event.preventDefault(); }
    else if (event.key === 'n' || event.key === 'N') { openNotes(); event.preventDefault(); }
    else if (event.key === 'Escape') { leavePresentation(); }
  });

  window.addEventListener('beforeprint', () => slides.forEach(slide => { slide.hidden = false; }));
  window.addEventListener('afterprint', () => goTo(index, { scroll: false }));

  /* ---------------------------------------------------------------- start */

  function start() {
    body.classList.add('deck-ready');
    let resumeNote = '';
    try {
      const raw = localStorage.getItem(progressKey);
      if (raw) {
        const saved = JSON.parse(raw);
        const savedIndex = slides.findIndex(slide => slide.id === saved.slide);
        if (savedIndex > 0) {
          if (!saved.done) resumeNote = `Resuming at slide ${savedIndex + 1}. Use Previous to go back.`;
          goTo(savedIndex, { scroll: false });
          // Set the note after goTo/loadClip, which clears the message for a narrated slide.
          if (resumeNote) els.message.textContent = resumeNote;
          return;
        }
      }
    } catch (_) { /* no saved progress */ }
    const hashIndex = slides.findIndex(slide => `#${slide.id}` === location.hash);
    goTo(hashIndex >= 0 ? hashIndex : 0, { scroll: false });
  }

  fetch(assetURL(manifestPath))
    .then(response => (response.ok ? response.json() : Promise.reject(new Error('manifest'))))
    .then(manifest => {
      const deck = (manifest.decks || {})[deckId];
      entries = (deck && deck.slides) || {};
      if (els.start) {
        const hasEntries = Object.keys(entries).length > 0;
        els.start.hidden = !hasEntries;
        els.start.disabled = !hasEntries;
        els.start.title = hasEntries
          ? 'Play this deck with narration; captions and transcript are available'
          : 'No recordings are published with this copy';
      }
      start();
    })
    .catch(() => {
      // No manifest: the deck is still fully readable and navigable.
      entries = {};
      if (els.start) els.start.hidden = true;
      start();
      els.message.textContent = 'Narration data is unavailable, so this deck is text-only.';
    });
})();
