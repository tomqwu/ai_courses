/* Learner progress — one store, every page.
 *
 * Progress lives in this browser (localStorage) behind a small interface, so a server-backed
 * store can replace it later without touching the pages that read it. The shape:
 *
 *   { v: 2,
 *     units:   { "m03:M3.1": <ms>, "m03:lab": <ms>, ... },   // unit id → completed at
 *     quizzes: { "m03": { score: 7, total: 8, at: <ms> } },   // best score per module
 *     labs:    { "m03": { checks: { "m03-lab-1": true }, evidence: {...}, at: <ms> } },
 *     last:    { href: "m03.html#slide-5", label: "...", at: <ms> } }
 *
 * The learner owns it: export and import are plain JSON, and nothing is uploaded — the
 * course's evidence discipline applied to the learner's own record.
 */
(function () {
  'use strict';
  var KEY = 'aps.progress.v2';
  var LEGACY = 'aps.progress.v1';
  var state = null;

  function empty() { return { v: 2, units: {}, quizzes: {}, labs: {}, last: null }; }

  function load() {
    if (state) return state;
    try {
      var raw = localStorage.getItem(KEY);
      state = raw ? JSON.parse(raw) : null;
    } catch (e) { state = null; }
    if (!state || state.v !== 2) {
      state = empty();
      // v1 stored unit checkboxes only: { "m00:intro": 1 }
      try {
        var old = JSON.parse(localStorage.getItem(LEGACY) || 'null');
        if (old && typeof old === 'object') {
          Object.keys(old).forEach(function (k) { if (old[k]) state.units[k] = Date.now(); });
        }
      } catch (e) { /* no legacy data */ }
      save();
    }
    return state;
  }

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* private mode */ }
    document.dispatchEvent(new CustomEvent('aps:progress', { detail: state }));
  }

  var api = {
    get: function () { return load(); },
    unitDone: function (id) { return !!load().units[id]; },
    setUnit: function (id, done) {
      var s = load();
      if (done) s.units[id] = s.units[id] || Date.now(); else delete s.units[id];
      save();
    },
    moduleUnits: function (deck) {
      var s = load(); return Object.keys(s.units).filter(function (k) { return k.indexOf(deck + ':') === 0; });
    },
    quiz: function (deck) { return load().quizzes[deck] || null; },
    setQuiz: function (deck, score, total) {
      var s = load(); var prev = s.quizzes[deck];
      if (!prev || score >= prev.score) s.quizzes[deck] = { score: score, total: total, at: Date.now() };
      if (total && score / total >= 0.75) s.units[deck + ':quiz'] = s.units[deck + ':quiz'] || Date.now();
      save();
    },
    lab: function (deck) { var s = load(); return s.labs[deck] || { checks: {}, evidence: {} }; },
    setLabCheck: function (deck, id, on, total) {
      var s = load(); var lab = s.labs[deck] || (s.labs[deck] = { checks: {}, evidence: {} });
      if (on) lab.checks[id] = true; else delete lab.checks[id];
      lab.at = Date.now();
      var n = Object.keys(lab.checks).length;
      if (total && n >= total) s.units[deck + ':lab'] = s.units[deck + ':lab'] || Date.now();
      else if (total && n < total) delete s.units[deck + ':lab'];
      save();
    },
    setLabEvidence: function (deck, fields) {
      var s = load(); var lab = s.labs[deck] || (s.labs[deck] = { checks: {}, evidence: {} });
      lab.evidence = fields; lab.at = Date.now(); save();
    },
    setLast: function (href, label) {
      var s = load(); s.last = { href: href, label: label, at: Date.now() }; save();
    },
    exportJSON: function () { return JSON.stringify(load(), null, 2); },
    importJSON: function (text) {
      var data = JSON.parse(text);
      if (!data || data.v !== 2 || typeof data.units !== 'object') throw new Error('not an AI Product Studio progress file');
      state = { v: 2, units: data.units || {}, quizzes: data.quizzes || {}, labs: data.labs || {}, last: data.last || null };
      save();
    },
    reset: function () { state = empty(); save(); }
  };
  window.APSProgress = api;

  /* ---------------------------------------------------------- generic bindings */

  // Progress rings: any element with data-ring="deck" or data-ring-units="a,b,c" and data-ring-total.
  function ring(el) {
    var s = load();
    var total = parseInt(el.getAttribute('data-ring-total') || '0', 10);
    var ids = (el.getAttribute('data-ring-units') || '').split(',').filter(Boolean);
    var done = ids.filter(function (id) { return !!s.units[id]; }).length;
    if (!total) total = ids.length;
    var pct = total ? Math.round(done / total * 100) : 0;
    el.style.setProperty('--pct', pct);
    el.setAttribute('aria-label', done + ' of ' + total + ' units complete');
    var label = el.querySelector('[data-ring-label]');
    if (label) label.textContent = pct + '%';
    el.classList.toggle('is-complete', total > 0 && done >= total);
    el.classList.toggle('is-started', done > 0);
    var text = el.parentElement && el.parentElement.querySelector('[data-ring-text]');
    if (text) text.textContent = done ? (done + ' of ' + total + ' units') : '';
  }

  // "Continue where you left off" — any element with data-continue.
  function continueLink() {
    var s = load();
    document.querySelectorAll('[data-continue]').forEach(function (el) {
      if (s.last && s.last.href) {
        el.hidden = false;
        var a = el.querySelector('a');
        if (a) { a.href = s.last.href; }
        var l = el.querySelector('[data-continue-label]');
        if (l) l.textContent = s.last.label || s.last.href;
      } else {
        el.hidden = true;
      }
    });
  }

  function render() {
    document.querySelectorAll('[data-ring-units]').forEach(ring);
    continueLink();
    // unit checkboxes (module pages)
    var s = load();
    document.querySelectorAll('[data-progress]').forEach(function (box) {
      var on = !!s.units[box.getAttribute('data-progress')];
      box.checked = on;
      var row = box.closest('.unit');
      if (row) row.classList.toggle('is-done', on);
    });
    var boxes = document.querySelectorAll('[data-progress]');
    if (boxes.length) {
      var n = 0; boxes.forEach(function (b) { if (b.checked) n++; });
      var count = document.getElementById('progress-count');
      var bar = document.querySelector('.progress-bar');
      var fill = document.getElementById('progress-fill');
      if (count) count.textContent = n + ' of ' + boxes.length;
      if (bar) bar.setAttribute('aria-valuenow', String(n));
      if (fill) fill.style.width = (boxes.length ? (n / boxes.length * 100) : 0) + '%';
    }
    // quiz / lab badges on cards
    document.querySelectorAll('[data-quiz-badge]').forEach(function (el) {
      var q = s.quizzes[el.getAttribute('data-quiz-badge')];
      el.hidden = !q;
      if (q) el.textContent = 'knowledge check ' + q.score + '/' + q.total;
    });
  }

  document.addEventListener('change', function (e) {
    var box = e.target;
    if (box && box.matches && box.matches('[data-progress]')) {
      api.setUnit(box.getAttribute('data-progress'), box.checked);
    }
  });
  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('[data-progress-export],[data-progress-import],[data-progress-reset]') : null;
    if (!t) return;
    if (t.hasAttribute('data-progress-export')) {
      var blob = new Blob([api.exportJSON()], { type: 'application/json' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = 'aps-progress.json'; a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    } else if (t.hasAttribute('data-progress-import')) {
      var input = document.createElement('input'); input.type = 'file'; input.accept = 'application/json';
      input.addEventListener('change', function () {
        var f = input.files && input.files[0]; if (!f) return;
        f.text().then(function (text) { api.importJSON(text); render(); })
          .catch(function (err) { alert(err.message); });
      });
      input.click();
    } else if (t.hasAttribute('data-progress-reset')) {
      if (confirm('Clear all progress stored in this browser?')) { api.reset(); render(); }
    }
  });
  document.addEventListener('aps:progress', render);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render); else render();
})();
