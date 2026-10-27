/* Learner progress — one store, every page.
 *
 * Progress lives in this browser (localStorage) behind a small interface, so a server-backed
 * store (#42) can replace it later without touching the pages that read it.
 *
 * Progress is recorded from what the learner does, never ticked by hand (#84). The history is a
 * list of events, and a unit is done once it has one:
 *
 *   watched    the narration played through the unit's last slide
 *   read       the learner read to the end of the unit's section in Read (the lesson)
 *   passed     the knowledge check scored at least 75%
 *   completed  the lab's checklist is complete and its evidence entry filled in and exported
 *   migrated   carried over from an earlier store, where units were ticked
 *
 *   { v: 3,
 *     events:  [ { unit: "m03:M3.1", kind: "watched", at: <ms> }, ... ],
 *     units:   { "m03:M3.1": <ms>, ... },                     // derived: unit → first completion
 *     quizzes: { "m03": { score: 7, total: 8, at: <ms> } },   // best score per module
 *     quizAnswers: { "m03": { "1": { answered, correct, chosen } } },
 *     labs:    { "m03": { checks: {...}, evidence: {...}, exportedAt: <ms>, steps: {...} } },
 *     last:    { href: "m03.html#slide-5", label: "...", at: <ms> },
 *     path:    "on-device-app" }                              // the path the outline shows
 *
 * The learner owns it: export and import are plain JSON, and nothing is uploaded — the
 * course's evidence discipline applied to the learner's own record.
 */
(function () {
  'use strict';
  var KEY = 'aps.progress.v3';
  var OLDER = ['aps.progress.v2', 'aps.progress.v1'];
  var REQUIRED = ['project', 'commands', 'environment', 'revision'];   // a filled-in evidence entry
  var state = null;

  function empty() {
    return { v: 3, events: [], units: {}, quizzes: {}, quizAnswers: {}, labs: {}, last: null, path: null };
  }

  function derive(s) {
    s.units = {};
    (s.events || []).forEach(function (e) { if (!s.units[e.unit]) s.units[e.unit] = e.at; });
    return s;
  }

  // Earlier stores held ticked units ({ "m00:intro": <ms> } in v2, { "m00:intro": 1 } in v1). They
  // come over as history, marked as migrated rather than dressed up as watching or reading.
  function upgrade(old) {
    var s = empty();
    if (!old || typeof old !== 'object') return s;
    var units = old.v === 2 ? (old.units || {}) : old;
    Object.keys(units).forEach(function (k) {
      if (units[k] && k.indexOf(':') > 0) s.events.push({ unit: k, kind: 'migrated', at: typeof units[k] === 'number' && units[k] > 1 ? units[k] : Date.now() });
    });
    if (old.v === 2) {
      s.quizzes = old.quizzes || {}; s.quizAnswers = old.quizAnswers || {}; s.labs = old.labs || {};
      s.last = old.last || null; s.path = old.path || null;
    }
    return derive(s);
  }

  function load() {
    if (state) return state;
    try {
      var raw = localStorage.getItem(KEY);
      state = raw ? JSON.parse(raw) : null;
    } catch (e) { state = null; }
    if (!state || state.v !== 3) {
      state = empty();
      for (var i = 0; i < OLDER.length; i++) {
        try {
          var old = JSON.parse(localStorage.getItem(OLDER[i]) || 'null');
          if (old) { state = upgrade(old); break; }
        } catch (e) { /* nothing stored under that key */ }
      }
      save();
    }
    return derive(state);
  }

  function save() {
    derive(state);
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* private mode */ }
    document.dispatchEvent(new CustomEvent('aps:progress', { detail: state }));
  }

  function record(unit, kind) {
    var s = load();
    var seen = s.events.some(function (e) { return e.unit === unit && e.kind === kind; });
    if (!seen) { s.events.push({ unit: unit, kind: kind, at: Date.now() }); save(); }
  }

  function filled(evidence) {
    return REQUIRED.every(function (k) { return ((evidence || {})[k] || '').trim(); });
  }

  // A lab is complete when its checklist is complete and its evidence entry has been filled in and
  // exported: the checklist is the learner's claim, the exported entry is the proof.
  function settleLab(deck, total) {
    var lab = load().labs[deck];
    if (!lab || !total) return;
    if (Object.keys(lab.checks || {}).length >= total && lab.exportedAt && filled(lab.evidence)) {
      record(deck + ':lab', 'completed');
    }
  }

  var api = {
    get: function () { return load(); },
    events: function () { return load().events.slice(); },
    record: record,
    unitDone: function (id) { return !!load().units[id]; },
    moduleUnits: function (deck) {
      var s = load(); return Object.keys(s.units).filter(function (k) { return k.indexOf(deck + ':') === 0; });
    },
    evidenceFilled: filled,
    quiz: function (deck) { return load().quizzes[deck] || null; },
    setQuiz: function (deck, score, total) {
      var s = load(); var prev = s.quizzes[deck];
      if (!prev || score >= prev.score) s.quizzes[deck] = { score: score, total: total, at: Date.now() };
      save();
      if (total && score / total >= 0.75) record(deck + ':quiz', 'passed');
    },
    // Each answer as it is given (#78), so a check survives a reload; cleared by "Try again".
    quizAnswers: function (deck) { return (load().quizAnswers || {})[deck] || {}; },
    setQuizAnswer: function (deck, n, record) {
      var s = load(); s.quizAnswers = s.quizAnswers || {};
      var a = s.quizAnswers[deck] || (s.quizAnswers[deck] = {});
      a[n] = record; save();
    },
    clearQuizAnswers: function (deck) {
      var s = load(); if (s.quizAnswers) delete s.quizAnswers[deck]; save();
    },
    lab: function (deck) { var s = load(); return s.labs[deck] || { checks: {}, evidence: {} }; },
    setLabCheck: function (deck, id, on, total) {
      var s = load(); var lab = s.labs[deck] || (s.labs[deck] = { checks: {}, evidence: {} });
      if (on) lab.checks[id] = true; else delete lab.checks[id];
      lab.at = Date.now();
      save();
      settleLab(deck, total);
    },
    // The workspace's steps (#77): which are done, and which one the learner is on.
    setLabSteps: function (deck, current, done) {
      var s = load(); var lab = s.labs[deck] || (s.labs[deck] = { checks: {}, evidence: {} });
      lab.step = current; lab.steps = done; lab.at = Date.now(); save();
    },
    setLabEvidence: function (deck, fields) {
      var s = load(); var lab = s.labs[deck] || (s.labs[deck] = { checks: {}, evidence: {} });
      lab.evidence = fields; lab.at = Date.now(); save();
    },
    // The evidence entry was copied or downloaded. Only a filled-in entry counts as exported.
    setLabExported: function (deck, total) {
      var s = load(); var lab = s.labs[deck] || (s.labs[deck] = { checks: {}, evidence: {} });
      if (!filled(lab.evidence)) return false;
      lab.exportedAt = Date.now(); save();
      settleLab(deck, total);
      return true;
    },
    setLast: function (href, label) {
      var s = load(); s.last = { href: href, label: label, at: Date.now() }; save();
    },
    path: function () { return load().path || null; },
    setPath: function (slug) {
      var s = load(); if (s.path !== slug) { s.path = slug; save(); }
    },
    // The evidence entry in the Module 1 format — one formatter, used by the lab page and by the
    // evidence log, so the two can never disagree about what an entry looks like.
    evidenceMarkdown: function (v, labTitle) {
      v = v || {};
      var get = function (k) { return (v[k] || '').trim(); };
      var today = new Date().toISOString().slice(0, 10);
      var lines = ['## Evidence — ' + (get('project') || '<project>') + ' — ' + labTitle + ' — ' + (get('date') || today),
        'Commands (with results):'];
      get('commands').split('\n').filter(function (l) { return l.trim(); }).forEach(function (l) { lines.push('- ' + l.trim()); });
      if (!get('commands')) lines.push('- <command> → <result>');
      lines.push('Environment: ' + (get('environment') || '<OS, Python version, daemon state>'));
      lines.push('Revision: ' + (get('revision') || '<git rev-parse HEAD>'));
      lines.push('Limitations / not verified:');
      get('limitations').split('\n').filter(function (l) { return l.trim(); }).forEach(function (l) { lines.push('- ' + l.trim()); });
      if (!get('limitations')) lines.push('- <what this run does not prove>');
      return lines.join('\n');
    },
    exportJSON: function () { return JSON.stringify(load(), null, 2); },
    importJSON: function (text) {
      var data = JSON.parse(text);
      if (data && data.v === 3 && Array.isArray(data.events)) {
        state = { v: 3, events: data.events, units: {}, quizzes: data.quizzes || {}, labs: data.labs || {},
                  last: data.last || null, path: data.path || null, quizAnswers: data.quizAnswers || {} };
      } else if (data && data.v === 2 && typeof data.units === 'object') {
        state = upgrade(data);
      } else {
        throw new Error('not an AI Product Studio progress file');
      }
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
        var a = el.querySelector('[data-continue-link]');
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
    var s = load();
    // quiz / lab badges on cards
    document.querySelectorAll('[data-quiz-badge]').forEach(function (el) {
      var q = s.quizzes[el.getAttribute('data-quiz-badge')];
      el.hidden = !q;
      if (q) el.textContent = 'knowledge check ' + q.score + '/' + q.total;
    });
  }


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
