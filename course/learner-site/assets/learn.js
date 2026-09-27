/* Learn (#112): the module as one page, read aloud on request.
 *
 * Every part of the module is on the page; nothing is paged. Narration never autoplays. A part's
 * Listen button, a unit's "Listen to this unit" or the player's Play starts the narration, which then
 * continues part after part (unless Continue is off), scrolling each into view as it starts.
 *   - audio.currentTime is the only clock: the highlighted sentence, the figure's build and the time
 *     all derive from it. Sentences are timed from the caption cues, word by word (the gate proves
 *     captions and script match word for word).
 *   - A figure builds on the sentence that introduces each part while its narration plays, and is
 *     complete otherwise and under reduced motion.
 *   - A unit is watched when its narration plays through its last part; read when scrolled to its
 *     end (shell.js watches the .read-end markers). Where you are is remembered for the course home.
 *   - ?t= on a deep link (a search hit on a spoken sentence) marks that sentence; Play starts there.
 */
(function () {
  'use strict';
  var root = document.querySelector('[data-learn]');
  if (!root) return;
  var body = document.body;
  var deck = body.getAttribute('data-learn-deck');
  var base = body.getAttribute('data-site-base') || '.';
  var P = window.APSProgress;
  var M = window.APSNarrationMedia;
  var units = [];
  try { units = JSON.parse(body.getAttribute('data-units') || '[]'); } catch (e) { units = []; }
  var sections = Array.prototype.slice.call(root.querySelectorAll('.learn-section'));
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var player = document.querySelector('[data-learn-player]');

  function unitAt(n) {
    for (var i = 0; i < units.length; i++) if (n >= units[i].first && n <= units[i].last) return units[i];
    return null;
  }
  function numberOf(sec) { return parseInt(sec.getAttribute('data-number'), 10); }

  /* ---------------------------------------------------------- where you are (no audio needed) */
  var viewing = -1;
  var lastSaved = 0;
  function spy() {
    var line = window.innerHeight / 3, n = -1;
    sections.forEach(function (s, i) { if (s.getBoundingClientRect().top <= line) n = i; });
    if (n < 0) n = 0;
    if (n === viewing) return;
    viewing = n;
    var num = numberOf(sections[n]);
    document.dispatchEvent(new CustomEvent('aps:slide', { detail: { deck: deck, n: num } }));
    var now = Date.now();
    if (P && now - lastSaved > 800) {
      lastSaved = now;
      var u = unitAt(num);
      P.setLast(deck + '.html#' + sections[n].id,
        (body.getAttribute('data-deck-label') || deck) + (u ? ' — ' + u.name : ''));
    }
  }
  window.addEventListener('scroll', spy, { passive: true });
  window.addEventListener('load', function () { viewing = -1; spy(); });   // after the browser's own jump to a #hash
  window.addEventListener('hashchange', function () { viewing = -1; spy(); });
  spy();

  if (!player || !M) return;          // the text-first copy: a page to read, no audio

  /* ---------------------------------------------------------- the player */
  var ui = {
    play: player.querySelector('[data-lp-play]'), prev: player.querySelector('[data-lp-prev]'),
    next: player.querySelector('[data-lp-next]'), where: player.querySelector('[data-lp-where]'),
    time: player.querySelector('[data-lp-time]'), speed: player.querySelector('[data-lp-speed]'),
    auto: player.querySelector('[data-lp-auto]'), status: player.querySelector('[data-lp-status]'),
  };
  var audio = document.createElement('audio');
  audio.preload = 'none';
  audio.setAttribute('aria-label', 'Narration');
  audio.setAttribute('data-narration-audio', '');
  player.appendChild(audio);

  var cur = -1;            // the part whose narration is loaded
  var rows = [];           // its sentences, timed
  var version = 0;
  var startAt = null;      // ?t= from a search hit
  var said = -1;

  var voiced = sections.map(function (s, i) { return s.hasAttribute('data-audio') ? i : -1; })
    .filter(function (i) { return i >= 0; });

  function url(path) {
    var b = new URL(base.endsWith('/') ? base : base + '/', location.href);
    return new URL(String(path).replace(/^\//, ''), b).href;
  }
  function clock(s) {
    s = Math.max(0, Math.floor(s || 0));
    return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0');
  }
  function announce(msg) { if (ui.status) ui.status.textContent = msg; }

  function spans(i) { return Array.prototype.slice.call(sections[i].querySelectorAll('.said')); }

  // The approved sentences, timed from the cues: each word gets a time by its place in its cue.
  function timeRows(i, cues) {
    var texts = spans(i).map(function (s) { return s.textContent; });
    if (!cues.length || !texts.length) return [];
    var words = function (t) { return t.split(/\s+/).filter(Boolean); };
    var at = [];
    cues.forEach(function (c) {
      var ws = words(c.text);
      ws.forEach(function (_, k) { at.push(c.start + (c.end - c.start) * k / ws.length); });
    });
    var end = cues[cues.length - 1].end, w = 0;
    return texts.map(function (t) {
      var start = at[Math.min(w, at.length - 1)] || 0;
      w += words(t).length;
      return { start: start, end: w < at.length ? at[w] : end };
    });
  }

  function mark(i, r) {
    if (r === said && i === cur) return;
    said = r;
    sections.forEach(function (s, k) {
      spans(k).forEach(function (sp, n) { sp.classList.toggle('is-said', k === i && n === r); });
    });
  }

  /* figure build-ins: parts arrive on the sentence that introduces them */
  function build(i, r) {
    var parts = sections[i].querySelectorAll('.fig [data-step]');
    Array.prototype.forEach.call(parts, function (p) {
      var on = r === Infinity || reduce.matches || Number(p.getAttribute('data-step')) <= r;
      p.classList.toggle('is-shown', on);
      p.classList.toggle('is-pending', !on);
    });
  }

  function paint() {
    var playing = !audio.paused && !audio.ended;
    ui.play.classList.toggle('is-playing', playing);
    ui.play.setAttribute('aria-label', playing ? 'Pause narration' : 'Play narration');
    ui.play.setAttribute('aria-pressed', String(playing));
    sections.forEach(function (s, k) {
      s.classList.toggle('is-playing', k === cur && playing);
      var b = s.querySelector('[data-listen]');
      if (b) b.setAttribute('aria-label', k === cur && playing ? 'Pause this section' : 'Listen to this section');
    });
    if (cur >= 0) {
      var h = sections[cur].querySelector('h3');
      var u = unitAt(numberOf(sections[cur]));
      ui.where.textContent = (u ? u.name : '') + (h ? (u ? ' · ' : '') + h.textContent : '');
    }
  }

  function tick() {
    if (cur < 0) return;
    var t = audio.currentTime, r = -1;
    for (var k = 0; k < rows.length; k++) if (t >= rows[k].start && t < rows[k].end) { r = k; break; }
    if (r >= 0) { mark(cur, r); if (!audio.paused) build(cur, r); }
    var d = Number.isFinite(audio.duration) ? audio.duration : parseFloat(sections[cur].getAttribute('data-duration')) || 0;
    ui.time.textContent = clock(t) + ' / ' + clock(d);
  }

  function load(i) {
    version += 1;
    var v = version;
    cur = i;
    rows = [];
    said = -1;
    var s = sections[i];
    audio.src = url(s.getAttribute('data-audio'));
    audio.playbackRate = Number(ui.speed.value);
    return fetch(url(s.getAttribute('data-captions'))).then(function (res) {
      if (!res.ok) throw new Error('captions');
      return res.text();
    }).then(function (text) {
      if (v === version) rows = timeRows(i, M.parseCaptions(text));
    }).catch(function () { if (v === version) announce('Captions could not load; the narration still plays.'); });
  }

  function play(i, opts) {
    opts = opts || {};
    if (i < 0 || i >= sections.length || !sections[i].hasAttribute('data-audio')) return;
    var go = function () {
      if (startAt !== null && i === startIndex) { audio.currentTime = startAt; startAt = null; }
      build(i, -1);
      M.play(audio).catch(function (e) {
        if (e && e.name === 'AbortError') return;
        announce('Playback was paused by your browser. Press Play to continue.');
        paint();
      });
      if (opts.scroll) sections[i].scrollIntoView({ behavior: reduce.matches ? 'auto' : 'smooth', block: 'start' });
    };
    if (i === cur && audio.getAttribute('src')) { go(); return; }
    sections.forEach(function (_, k) { if (k !== i) build(k, Infinity); });
    load(i).then(go);
  }

  function toggle(i) {
    if (i === cur && !audio.paused) { audio.pause(); return; }
    play(i, {});
  }

  function nextVoiced(from, dir) {
    for (var k = from + dir; k >= 0 && k < sections.length; k += dir) if (sections[k].hasAttribute('data-audio')) return k;
    return -1;
  }

  audio.addEventListener('timeupdate', tick);
  audio.addEventListener('play', paint);
  audio.addEventListener('pause', paint);
  audio.addEventListener('ended', function () {
    var i = cur;
    build(i, Infinity);
    mark(i, -1);
    paint();
    var num = numberOf(sections[i]);
    var u = unitAt(num);
    // The narration played through: on a unit's last part, that unit is watched.
    if (u && u.last === num && u.kind !== 'lab' && u.kind !== 'quiz' && P) P.record(deck + ':' + u.id, 'watched');
    var n = nextVoiced(i, 1);
    if (ui.auto.checked && n >= 0) play(n, { scroll: true });
    else if (n < 0) announce('End of the module.');
  });
  audio.addEventListener('error', function () {
    if (audio.getAttribute('src')) announce('Audio could not load. Press Play to try again.');
    paint();
  });

  root.addEventListener('click', function (e) {
    var b = e.target.closest('[data-listen]');
    if (b) { toggle(sections.indexOf(b.closest('.learn-section'))); return; }
    var u = e.target.closest('[data-listen-unit]');
    if (u) {
      var unit = u.closest('.learn-unit');
      var first = sections.findIndex(function (s) { return unit.contains(s) && s.hasAttribute('data-audio'); });
      play(first, { scroll: true });
    }
  });
  ui.play.addEventListener('click', function () {
    if (cur >= 0 && !audio.paused) { audio.pause(); return; }
    if (cur >= 0) { play(cur, {}); return; }
    var from = startIndex >= 0 ? startIndex : viewing;
    var i = sections[from] && sections[from].hasAttribute('data-audio') ? from : nextVoiced(from, 1);
    play(i < 0 ? voiced[0] : i, { scroll: true });
  });
  ui.prev.addEventListener('click', function () { var k = nextVoiced(cur < 0 ? viewing : cur, -1); if (k >= 0) play(k, { scroll: true }); });
  ui.next.addEventListener('click', function () { var k = nextVoiced(cur < 0 ? viewing : cur, 1); if (k >= 0) play(k, { scroll: true }); });
  ui.speed.addEventListener('change', function () { audio.playbackRate = Number(ui.speed.value); });

  // A deep link from a search hit on a spoken sentence: mark it; Play starts there.
  var startIndex = -1;
  var hash = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
  var t = parseFloat(new URLSearchParams(location.search).get('t'));
  if (hash && hash.classList.contains('learn-section') && Number.isFinite(t) && t > 0 && hash.hasAttribute('data-audio')) {
    startIndex = sections.indexOf(hash);
    startAt = t;
    load(startIndex).then(function () {
      var r = rows.findIndex(function (row) { return t >= row.start && t < row.end; });
      if (r >= 0) { mark(startIndex, r); var sp = spans(startIndex)[r]; if (sp) sp.classList.add('is-found'); }
      ui.where.textContent = 'Starts at ' + clock(t) + ', where the match is spoken · press Play';
    });
  }
  paint();
})();
