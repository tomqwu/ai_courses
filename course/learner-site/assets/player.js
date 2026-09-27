/* Watch — the lesson player (#75): one slide at a time, one control bar, a transcript that follows.
 *
 * Deliberate behaviour, each for a reason:
 *   - Narration NEVER autoplays. Pressing Play starts the current narrated slide and then continues.
 *   - Auto-next waits a short wall-clock beat between slides so the learner can read, and that beat
 *     is shortened for prefers-reduced-motion (ai_qe has no such branch; this is our addition).
 *   - audio.currentTime is the only clock: the caption line, the transcript highlight and the time
 *     readout all derive from it, so nothing can drift.
 *   - One bar owns every control. The stage and the bar are sized together, so the controls are
 *     on screen whatever the slide: the bar's height is reserved in the frame maths.
 *   - The transcript panel lists the approved narration a sentence per line. With captions loaded
 *     each line is a cue: it is highlighted while spoken, and clicking it seeks there.
 *   - A slide with no recording still navigates; the transcript and the sources still show.
 *   - Progress is remembered per deck in localStorage and offered back on return; a deep link wins.
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
  const $ = sel => document.querySelector(sel);

  const els = {
    bar: $('.player-bar'),
    prev: $('[data-nav="prev"]'),
    next: $('[data-nav="next"]'),
    status: $('.slide-status'),
    present: $('[data-present]'),
    segments: Array.from(document.querySelectorAll('.tl-seg')),
    lines: $('[data-transcript-lines]'),
    sources: $('[data-source-list]'),
    sourcesEmpty: $('[data-sources-empty]'),
    notes: $('[data-drawer-notes]'),
    tabs: Array.from(document.querySelectorAll('.panel-tabs [role="tab"]')),
    upNext: $('[data-up-next]'),
  };
  const ui = {
    play: $('[data-play]'), time: $('[data-time]'), speed: $('[data-speed]'), cc: $('[data-cc]'),
    auto: $('[data-auto]'), caption: $('[data-caption]'), status: $('[data-status]'), retry: $('[data-retry]'),
    replay: $('[data-fig-replay]'),
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
  let activeCue = -1;
  let rows = [];                   // transcript rows: whole sentences built from the caption cues
  let startAt = null;              // ?t= from a search hit on a spoken sentence (#80)

  const audio = document.createElement('audio');
  audio.preload = 'none';
  audio.setAttribute('aria-label', 'Slide narration');
  audio.dataset.narrationAudio = '';
  els.bar.append(audio);

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

  /* ---------------------------------------------------------------- frame */

  // The stage and the bar are one unit that must fit the viewport, so the controls are always on
  // screen. Everything above the stage (the top bar, the padding) is measured into --chrome-height,
  // and the bar's own height into --narration-height; the stylesheet gives both back from the 16:9
  // frame. Measured rather than assumed, because the bar's height changes with its content.
  function fitFrame() {
    const root = document.documentElement;
    const stage = $('.slides');
    const top = stage ? stage.getBoundingClientRect().top + window.scrollY : 0;
    const gap = parseFloat(getComputedStyle(root).getPropertyValue('--narration-gap')) || 12;
    const chrome = `${Math.ceil(top + gap)}px`;
    const bar = `${Math.ceil(els.bar.getBoundingClientRect().height)}px`;
    if (root.style.getPropertyValue('--chrome-height') !== chrome) root.style.setProperty('--chrome-height', chrome);
    if (root.style.getPropertyValue('--narration-height') !== bar) root.style.setProperty('--narration-height', bar);
  }
  let resizeFrame = 0;
  const refit = () => { cancelAnimationFrame(resizeFrame); resizeFrame = requestAnimationFrame(fitFrame); };
  if (window.ResizeObserver) new ResizeObserver(refit).observe(els.bar);
  window.addEventListener('resize', refit);

  const announce = message => { ui.status.textContent = message; };
  const clearCaption = () => { ui.caption.textContent = ''; };

  /* ---------------------------------------------------------------- transcript + captions */

  function currentCueIndex() {
    return cueList.findIndex(item => audio.currentTime >= item.start && audio.currentTime < item.end);
  }

  // Caption cues are sized to be read in two lines, so they break mid-sentence and a sentence can
  // start mid-cue. The transcript rows are the approved script's sentences instead, timed from the
  // cues: each word gets a time by its place in its cue, and a sentence runs from its first word to
  // the next sentence's first word. The gate proves captions and script match word for word, so the
  // word counts line up.
  function sentenceRows(cues) {
    const source = slides[index].querySelector('.slide-script-source');
    const sentences = Array.from(source ? source.content.children : []).map(li => li.textContent);
    if (!cues.length || !sentences.length) return [];
    const words = t => t.split(/\s+/).filter(Boolean);
    const at = [];
    cues.forEach(cue => {
      const ws = words(cue.text);
      ws.forEach((_, k) => at.push(cue.start + (cue.end - cue.start) * k / ws.length));
    });
    const last = cues[cues.length - 1].end;
    let w = 0;
    return sentences.map(text => {
      const start = at[Math.min(w, at.length - 1)] || 0;
      w += words(text).length;
      return { start, end: w < at.length ? at[w] : last, text };
    });
  }

  function highlight(i) {
    if (i === activeCue) return;
    activeCue = i;
    Array.from(els.lines.children).forEach((li, n) => {
      const on = n === i;
      li.classList.toggle('is-active', on);
      const target = li.querySelector('button') || li;
      if (on) target.setAttribute('aria-current', 'true'); else target.removeAttribute('aria-current');
    });
    // Keep the spoken line in view inside the panel, without scrolling the page.
    const line = els.lines.children[i];
    const box = els.lines;
    if (line && box.scrollHeight > box.clientHeight) {
      const top = line.offsetTop - box.offsetTop;
      if (top < box.scrollTop || top + line.offsetHeight > box.scrollTop + box.clientHeight) {
        box.scrollTop = Math.max(0, top - box.clientHeight / 3);
      }
    }
  }

  function renderCaption() {
    const live = clip && !audioFailed && !audio.seeking;
    const row = live ? rows.findIndex(r => audio.currentTime >= r.start && audio.currentTime < r.end) : -1;
    highlight(row);
    followBuild(row);
    const i = live ? currentCueIndex() : -1;
    if (!clip || !captionsOn || audioFailed || audio.seeking) { clearCaption(); return; }
    const text = i >= 0 ? cueList[i].text : '';
    if (ui.caption.textContent !== text) ui.caption.textContent = text;
  }

  // The panel's rows: the caption cues once they are loaded (each a button that seeks to its
  // start), otherwise the approved script a sentence per line — the same words either way.
  function renderLines() {
    activeCue = -1;
    els.lines.textContent = '';
    rows = sentenceRows(cueList);
    if (rows.length) {
      rows.forEach(cue => {
        const li = document.createElement('li');
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'line-seek';
        button.dataset.start = String(cue.start);
        button.textContent = cue.text;
        button.setAttribute('aria-label', `${clock(cue.start)} — ${cue.text}`);
        li.append(button);
        els.lines.append(li);
      });
      renderCaption();
      return;
    }
    const source = slides[index].querySelector('.slide-script-source');
    Array.from(source ? source.content.children : []).forEach(item => {
      const li = document.createElement('li');
      li.textContent = item.textContent;
      els.lines.append(li);
    });
    if (!els.lines.children.length) {
      const li = document.createElement('li');
      li.className = 'panel-empty';
      li.textContent = 'This slide has no narration.';
      els.lines.append(li);
    }
  }

  function renderSources() {
    const slide = slides[index];
    const list = slide.querySelector('.slide-sources-source');
    els.sources.textContent = '';
    if (list) els.sources.append(list.content.cloneNode(true));
    els.sourcesEmpty.hidden = els.sources.children.length > 0;
    const notes = (slide.querySelector('.slide-notes-source')?.textContent || '').trim();
    els.notes.textContent = notes || 'No speaker notes for this slide.';
    els.notes.classList.toggle('drawer-empty', !notes);
  }

  function selectTab(name, focus) {
    els.tabs.forEach(tab => {
      const on = tab.dataset.tab === name;
      tab.setAttribute('aria-selected', String(on));
      tab.tabIndex = on ? 0 : -1;
      document.getElementById(tab.getAttribute('aria-controls')).hidden = !on;
      if (on && focus) tab.focus();
    });
  }
  els.tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => selectTab(tab.dataset.tab, false));
    tab.addEventListener('keydown', event => {
      if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') return;
      const next = els.tabs[(i + (event.key === 'ArrowRight' ? 1 : els.tabs.length - 1)) % els.tabs.length];
      selectTab(next.dataset.tab, true);
      event.preventDefault();
    });
  });

  /* ---------------------------------------------------------------- figure build-ins (#99) */

  // A figure's parts may carry data-step: the index of the narration sentence at which they arrive.
  // While the narration plays, each part appears as its sentence is spoken; paused, the build stays
  // where it is. Otherwise — no recording, reduced motion, the narration over, a slide just opened —
  // the figure is complete. Replay (the button, or ".") re-runs the build without the audio.
  let buildTimer = 0;
  let buildAt = Infinity;
  const buildParts = () => Array.from(slides[index].querySelectorAll('.fig [data-step]'));

  function showBuild(n) {
    buildAt = n;
    buildParts().forEach(part => {
      const on = Number(part.dataset.step) <= n;
      part.classList.toggle('is-shown', on);
      part.classList.toggle('is-pending', !on);
    });
  }

  function resetBuild() {
    clearTimeout(buildTimer);
    buildTimer = 0;
    showBuild(Infinity);
    if (ui.replay) ui.replay.hidden = !buildParts().length;
  }

  function followBuild(row) {
    if (buildTimer || audio.paused || row < 0 || reduceMotion.matches || row === buildAt) return;
    if (buildParts().length) showBuild(row);
  }

  function replayBuild() {
    const parts = buildParts();
    if (!parts.length) return;
    clearTimeout(buildTimer);
    buildTimer = 0;
    if (reduceMotion.matches) { showBuild(Infinity); return; }
    const steps = Array.from(new Set(parts.map(part => Number(part.dataset.step)))).sort((a, b) => a - b);
    let k = -1;
    showBuild(-1);
    const next = () => {
      k += 1;
      if (k >= steps.length) { buildTimer = 0; showBuild(Infinity); return; }
      showBuild(steps[k]);
      buildTimer = setTimeout(next, 900);
    };
    buildTimer = setTimeout(next, 400);
  }

  /* ---------------------------------------------------------------- the bar */

  function updateTime() {
    if (!clip) {
      ui.time.textContent = `${index + 1} / ${slides.length}`;
      renderCaption();
      return;
    }
    const duration = Number.isFinite(audio.duration) ? audio.duration : (clip ? clip.duration : 0) || 0;
    ui.time.textContent = `${clock(audio.currentTime)} / ${clock(duration)}`;
    renderCaption();
  }

  function tick() {
    updateTime();
    if (!audio.paused && !audio.ended) frame = requestAnimationFrame(tick);
  }

  function updatePlaying() {
    const playing = Boolean(advanceTimer) || (!audio.paused && !audio.ended);
    ui.play.classList.toggle('is-playing', playing);
    ui.play.setAttribute('aria-label', audioFailed ? 'Retry narration audio' : playing ? 'Pause narration' : 'Play narration');
    ui.play.setAttribute('aria-pressed', String(playing));
    cancelAnimationFrame(frame);
    if (playing && !advanceTimer) frame = requestAnimationFrame(tick);
  }

  // Units behind the current slide are filled; the current one is filled up to the slide.
  function renderTimeline() {
    const n = index + 1;
    els.segments.forEach(seg => {
      const first = Number(seg.dataset.first), last = Number(seg.dataset.last);
      const fill = seg.querySelector('.tl-fill');
      const here = n >= first && n <= last;
      const pct = n > last ? 100 : here ? Math.round((n - first + 1) / (last - first + 1) * 100) : 0;
      fill.style.width = `${pct}%`;
      seg.classList.toggle('is-current', here);
      if (here) seg.setAttribute('aria-current', 'step'); else seg.removeAttribute('aria-current');
    });
  }

  /* ---------------------------------------------------------------- up next */

  let units = [];
  try { units = JSON.parse(body.dataset.units || '[]'); } catch (_) { units = []; }
  const unitAt = n => units.find(u => n >= u.first && n <= u.last);

  function renderUpNext() {
    const n = index + 1;
    const here = unitAt(n);
    const card = els.upNext;
    const set = (kind, title, meta, href) => {
      card.querySelector('[data-up-kind]').textContent = kind;
      card.querySelector('[data-up-title]').textContent = title;
      card.querySelector('[data-up-meta]').textContent = meta;
      card.setAttribute('href', href);
    };
    const titleOf = i => slides[i].querySelector('h2')?.textContent.trim() || `Slide ${i + 1}`;
    if (n >= slides.length) {
      set('Next module', 'Continue the course', 'The next module’s overview', body.dataset.nextModule || 'index.html');
      return;
    }
    const upcoming = unitAt(n + 1);
    if (upcoming && upcoming !== here) {
      if (upcoming.kind === 'lab') { set('Lab', upcoming.name, upcoming.meta, upcoming.href); return; }
      if (upcoming.kind === 'quiz') { set('Knowledge check', upcoming.name, upcoming.meta, upcoming.href); return; }
      const count = upcoming.last - upcoming.first + 1;
      set('Next section', upcoming.name, `Slide ${upcoming.first} · ${count} slide${count === 1 ? '' : 's'} in this section`,
        `#slide-${upcoming.first}`);
      return;
    }
    set('Next slide', titleOf(n), `Slide ${n + 1}`, `#slide-${n + 1}`);
  }

  /* ---------------------------------------------------------------- slides */

  function goTo(nextIndex, options = {}) {
    if (!options.keepStart) startAt = null;
    const clamped = Math.max(0, Math.min(slides.length - 1, nextIndex));
    stop();
    cancelAdvance();
    index = clamped;
    slides.forEach((slide, i) => {
      slide.hidden = i !== index;
      if (i === index) {
        slide.setAttribute('aria-current', 'true');
        const title = slide.querySelector('h1, h2, h3')?.textContent?.trim() || `Slide ${index + 1}`;
        els.status.textContent = `Slide ${index + 1} of ${slides.length} — ${title}`;
      } else {
        slide.removeAttribute('aria-current');
      }
    });
    if (options.scroll !== false) {
      const heading = slides[index].querySelector('h1, h2, h3');
      (heading || slides[index]).focus?.({ preventScroll: true });
    }
    try {
      // Arriving writes no hash: set during load, it becomes the fragment the browser scrolls to and
      // starts keyboard focus from. Every move after that keeps the URL on the slide.
      if (options.scroll !== false || location.hash) history.replaceState(null, '', `#${slides[index].id}`);
      localStorage.setItem(progressKey, JSON.stringify({ slide: slides[index].id }));
    } catch (_) { /* private mode: navigation still works */ }
    recordUnit();
    // The course outline follows the player (#73): it marks the unit this slide belongs to.
    document.dispatchEvent(new CustomEvent('aps:slide', { detail: { deck: deckId, n: index + 1 } }));
    els.prev.disabled = index === 0;
    els.next.disabled = index === slides.length - 1;
    renderTimeline();
    renderSources();
    renderUpNext();
    resetBuild();
    loadClip();
  }

  // Every slide records "where you left off" for the course home. Reaching a slide completes
  // nothing (#84): a unit is watched when the narration plays through its last slide (onEnded), or
  // read to the end in Read. Labs and knowledge checks are completed on their own pages.
  function recordUnit() {
    const P = window.APSProgress;
    if (!P) return;
    const n = index + 1;
    const unit = unitAt(n);
    const where = `${deckId}.html#${slides[index].id}`;
    if (unit) {
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
    ui.retry.hidden = true;
    ui.cc.disabled = !clip;
    ui.play.disabled = !clip;
    ui.speed.disabled = !clip;
    ui.caption.hidden = !clip;
    renderLines();
    refit();
    if (!clip) {
      announce(entries && Object.keys(entries).length
        ? 'This slide has no recording. Read its transcript below, or move on.' : '');
      updatePlaying();
      updateTime();
      return;
    }
    // No source is attached until the learner presses Play. A 258-slide site should not open a
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
      renderLines();
      if (startAt !== null) {
        // Opened from a search hit on a spoken sentence: that sentence is marked, and Play starts there.
        highlight(rows.findIndex(r => startAt >= r.start && startAt < r.end));
        announce(`Starts at ${clock(startAt)}, where the match is spoken · Press Play.`);
      } else if (!audioFailed) announce('Narration with synchronized captions.');
    } catch (error) {
      if (version !== clipVersion) return;
      ui.retry.hidden = false;
      announce('Captions could not load. Retry, or read the transcript below.');
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
    if (startAt !== null) { audio.currentTime = startAt; startAt = null; }
    const version = clipVersion;
    window.APSNarrationMedia.play(audio).catch(error => {
      if (version !== clipVersion || error.name === 'AbortError') return;
      updatePlaying();
      announce(audio.error ? 'Audio could not load. Press Play to try again.'
                           : 'Playback was paused by your browser. Press Play to continue.');
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

  const togglePlay = () => ((advanceTimer || (!audio.paused && !audio.ended)) ? pausePlayback() : play());

  function onEnded() {
    showBuild(Infinity);
    // The narration played through: on a unit's last slide, that unit is watched.
    const unit = unitAt(index + 1);
    if (clip && unit && unit.last === index + 1 && unit.kind !== 'lab' && unit.kind !== 'quiz'
        && window.APSProgress) window.APSProgress.record(`${deckId}:${unit.id}`, 'watched');
    const nextIndex = index + 1;
    if (nextIndex >= slides.length) {
      announce('End of the module. Up next is below.');
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
    announce('Audio could not load. Press Play to try again.');
  });

  els.prev.addEventListener('click', () => move(-1));
  if (ui.replay) ui.replay.addEventListener('click', replayBuild);
  els.next.addEventListener('click', () => move(1));
  ui.play.addEventListener('click', togglePlay);
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
  els.segments.forEach(seg => seg.addEventListener('click', () => goTo(Number(seg.dataset.first) - 1)));
  // Click-to-seek: a transcript line starts the narration from that sentence.
  els.lines.addEventListener('click', event => {
    const line = event.target.closest('[data-start]');
    if (!line || !clip) return;
    cancelAdvance();
    ensureSource();
    audio.currentTime = Number(line.dataset.start) + 0.01;
    updateTime();
    play();
  });

  /* ------------------------------------------------- present */

  // Presentation mode: full screen, the app chrome and the panels hidden, the stage and its bar
  // centred. The frame maths already give back the bar's height, so the slide stays 16:9 either way.
  async function enterPresentation() {
    body.classList.add('presentation-mode');
    els.present.setAttribute('aria-pressed', 'true');
    refit();
    try {
      if (!document.fullscreenElement && document.documentElement.requestFullscreen) {
        await document.documentElement.requestFullscreen();
      }
    } catch (_) { /* full screen is a bonus; the mode still applies without it */ }
    announce('Presentation mode. Press Escape to leave.');
  }

  function leavePresentation() {
    body.classList.remove('presentation-mode');
    els.present.setAttribute('aria-pressed', 'false');
    refit();
  }

  function togglePresentation() {
    if (body.classList.contains('presentation-mode')) leavePresentation(); else enterPresentation();
  }

  els.present.addEventListener('click', togglePresentation);
  document.addEventListener('fullscreenchange', () => {
    // Leaving full screen with Esc must not strand the page in presentation styling.
    if (!document.fullscreenElement) leavePresentation();
  });

  document.addEventListener('keydown', event => {
    if (document.querySelector('dialog[open]')) return;
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    const tag = (event.target.tagName || '').toLowerCase();
    if (['input', 'select', 'textarea', 'button', 'a'].includes(tag)) return;
    const key = event.key;
    if (key === 'ArrowRight' || key === 'PageDown') { move(1); event.preventDefault(); }
    else if (key === 'ArrowLeft' || key === 'PageUp') { move(-1); event.preventDefault(); }
    else if (key === ' ') { if (clip) togglePlay(); else move(1); event.preventDefault(); }
    else if (key === 'Home') { goTo(0); event.preventDefault(); }
    else if (key === 'End') { goTo(slides.length - 1); event.preventDefault(); }
    else if (key === 'f' || key === 'F' || key === 'p' || key === 'P') { togglePresentation(); event.preventDefault(); }
    else if (key === 't' || key === 'T') { selectTab('transcript', true); event.preventDefault(); }
    else if (key === '.') { replayBuild(); event.preventDefault(); }
    else if (key === 'n' || key === 'N') { selectTab('sources', true); event.preventDefault(); }
    else if (key === 'Escape') { leavePresentation(); }
  });

  window.addEventListener('beforeprint', () => slides.forEach(slide => { slide.hidden = false; }));
  window.addEventListener('afterprint', () => goTo(index, { scroll: false }));

  /* ---------------------------------------------------------------- start */

  function start() {
    body.classList.add('deck-ready');
    fitFrame();
    // A deep link makes the browser scroll to the slide's anchor, which tucks the top of the stage
    // under the sticky top bar. The stage and its bar are sized to fit from the top of the page.
    window.scrollTo(0, 0);
    // A deep link names a slide on purpose — an outline unit, a search hit, a transcript heading — so
    // it wins over the saved resume point. Resuming is for arriving at the deck with no slide named.
    const hashIndex = slides.findIndex(slide => `#${slide.id}` === location.hash);
    const t = parseFloat(new URLSearchParams(location.search).get('t'));
    if (hashIndex >= 0 && Number.isFinite(t) && t > 0) startAt = t;
    if (hashIndex >= 0) { goTo(hashIndex, { scroll: false, keepStart: true }); return; }
    try {
      const raw = localStorage.getItem(progressKey);
      if (raw) {
        const saved = JSON.parse(raw);
        const savedIndex = slides.findIndex(slide => slide.id === saved.slide);
        if (savedIndex > 0) {
          goTo(savedIndex, { scroll: false });
          // Set the note after goTo/loadClip, which replaces the status for a narrated slide.
          if (!saved.done) announce(`Resumed at slide ${savedIndex + 1}. Previous goes back.`);
          return;
        }
      }
    } catch (_) { /* no saved progress */ }
    goTo(0, { scroll: false });
  }

  // Following a link to another slide of this same deck (the outline's units, Up next) changes only
  // the hash; goTo itself uses replaceState, which fires no hashchange, so this never loops.
  window.addEventListener('hashchange', () => {
    const target = slides.findIndex(slide => `#${slide.id}` === location.hash);
    if (target >= 0 && target !== index) goTo(target);
  });

  fetch(assetURL(manifestPath))
    .then(response => (response.ok ? response.json() : Promise.reject(new Error('manifest'))))
    .then(manifest => {
      const deck = (manifest.decks || {})[deckId];
      entries = (deck && deck.slides) || {};
      start();
    })
    .catch(() => {
      // No manifest: the deck is still fully readable and navigable.
      entries = {};
      start();
      announce('Narration data is unavailable, so this deck is text-only.');
    });
})();
