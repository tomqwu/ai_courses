/* Lab page: one page read top to bottom — every step, the acceptance checklist you tick, and the
 * evidence entry you export.
 *
 * Steps: every step is on the page, in order. Each has a "Mark step N done" toggle that persists
 * like the checklist; the sticky list beside them says done, current (the step in view) or to do.
 *
 * The checklist is persisted per module; ticking every box marks the lab unit complete. The
 * evidence form produces the Markdown block the rubrics expect (commands, counts, date,
 * environment, limitations, head SHA), so what the learner pastes into their evidence log or a
 * cohort thread is the format Module 1 teaches, not a screenshot.
 */
(function () {
  'use strict';
  var root = document.querySelector('[data-lab]');
  if (!root) return;
  var deck = root.getAttribute('data-lab');
  var total = parseInt(root.getAttribute('data-lab-checks') || '0', 10);
  var P = window.APSProgress;

  function restore() {
    if (!P) return;
    var lab = P.lab(deck);
    root.querySelectorAll('[data-check]').forEach(function (box) {
      box.checked = !!lab.checks[box.getAttribute('data-check')];
      box.closest('.check-item').classList.toggle('is-done', box.checked);
    });
    Object.keys(lab.evidence || {}).forEach(function (k) {
      var f = root.querySelector('[data-evidence="' + k + '"]');
      if (f) f.value = lab.evidence[k];
    });
    count();
  }

  function count() {
    var boxes = root.querySelectorAll('[data-check]');
    var n = 0; boxes.forEach(function (b) { if (b.checked) n++; });
    var el = root.querySelector('[data-check-count]');
    if (el) el.textContent = n + ' of ' + boxes.length + ' checked';
    var bar = root.querySelector('[data-check-fill]');
    if (bar) bar.style.width = (boxes.length ? n / boxes.length * 100 : 0) + '%';
    var done = root.querySelector('[data-lab-done]');
    var complete = root.querySelector('[data-lab-complete]');
    var finished = P && P.unitDone(deck + ':lab');
    if (done) done.hidden = !(boxes.length && n === boxes.length) || finished;
    if (complete) complete.hidden = !finished;
  }

  root.addEventListener('change', function (e) {
    var box = e.target;
    if (box.matches('[data-check]')) {
      box.closest('.check-item').classList.toggle('is-done', box.checked);
      if (P) P.setLabCheck(deck, box.getAttribute('data-check'), box.checked, total);
      count();
    }
  });

  // copy buttons on code blocks
  root.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-copy]');
    if (!btn) return;
    var code = btn.parentElement.querySelector('code');
    if (!code) return;
    navigator.clipboard.writeText(code.textContent).then(function () {
      btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = 'Copy'; }, 1500);
    }, function () { btn.textContent = 'Select and copy'; });
  });

  // evidence form
  var form = root.querySelector('[data-evidence-form]');
  if (form) {
    var fields = Array.prototype.slice.call(form.querySelectorAll('[data-evidence]'));
    var out = form.querySelector('[data-evidence-out]');
    function build() {
      var v = {};
      fields.forEach(function (f) { v[f.getAttribute('data-evidence')] = f.value.trim(); });
      out.value = P ? P.evidenceMarkdown(v, root.getAttribute('data-lab-title')) : '';
      return v;
    }
    fields.forEach(function (f) { f.addEventListener('input', function () { var v = build(); if (P) P.setLabEvidence(deck, v); }); });
    // Exporting a filled-in entry is what completes the lab (#84), together with the checklist.
    var status = form.querySelector('[data-evidence-status]');
    function exported() {
      var ok = P && P.setLabExported ? P.setLabExported(deck, total) : false;
      if (status) status.textContent = ok ? 'Exported.' : 'Fill in the project, commands, environment and revision first — only a filled-in entry counts.';
      count();
    }
    var copy = form.querySelector('[data-evidence-copy]');
    if (copy) copy.addEventListener('click', function () {
      build();
      exported();
      navigator.clipboard.writeText(out.value).then(function () { copy.textContent = 'Copied to clipboard'; setTimeout(function () { copy.textContent = 'Copy evidence entry'; }, 1500); });
    });
    var dl = form.querySelector('[data-evidence-download]');
    if (dl) dl.addEventListener('click', function () {
      build();
      exported();
      var blob = new Blob([out.value + '\n'], { type: 'text/markdown' });
      var a = document.createElement('a'); a.href = URL.createObjectURL(blob);
      a.download = 'evidence-' + deck + '.md'; a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    });
    build();
  }
  /* ---------------------------------------------------------- steps */
  // Every step is on the page. Each has its own "done" toggle, persisted like the checklist; the
  // step list beside them shows done / current / to do, and "current" follows the step in view.
  var views = Array.prototype.slice.call(root.querySelectorAll('.lab-step'));
  var links = Array.prototype.slice.call(root.querySelectorAll('[data-step-go]'));
  var current = 0;
  var done = {};

  function paint() {
    links.forEach(function (a, i) {
      var state = done[i] ? 'done' : i === current ? 'current' : 'todo';
      a.classList.remove('is-done', 'is-current', 'is-todo');
      a.classList.add('is-' + state);
      if (i === current) a.setAttribute('aria-current', 'step'); else a.removeAttribute('aria-current');
      var word = a.querySelector('[data-step-state]');
      if (word) word.textContent = state === 'todo' ? 'to do' : state;
    });
    views.forEach(function (v, i) {
      var btn = v.querySelector('[data-step-done]');
      if (!btn) return;
      btn.setAttribute('aria-pressed', done[i] ? 'true' : 'false');
      v.classList.toggle('is-done', !!done[i]);
      var label = btn.querySelector('[data-step-done-label]');
      if (label) label.textContent = done[i] ? 'Done' : label.getAttribute('data-todo') || label.textContent;
    });
  }

  if (views.length) {
    views.forEach(function (v) {
      var label = v.querySelector('[data-step-done-label]');
      if (label) label.setAttribute('data-todo', label.textContent);
    });
    var saved = P ? P.lab(deck) : {};
    done = saved.steps || {};
    paint();
    root.addEventListener('click', function (ev) {
      var btn = ev.target.closest('[data-step-done]');
      if (btn) {
        var i = views.indexOf(btn.closest('.lab-step'));
        done[i] = !done[i];
        if (!done[i]) delete done[i];
        paint();
        if (P && P.setLabSteps) P.setLabSteps(deck, current, done);
        return;
      }
      var jump = ev.target.closest('[data-evidence-jump]');
      if (jump) {
        var field = root.querySelector('[data-evidence="project"]');
        if (field) { ev.preventDefault(); field.scrollIntoView({ block: 'center' }); field.focus(); }
      }
    });
    // The step in view is "current": the last step whose top has passed the upper third of the screen.
    var spy = function () {
      var line = window.innerHeight / 3, n = 0;
      views.forEach(function (v, i) { if (v.getBoundingClientRect().top <= line) n = i; });
      if (n !== current) { current = n; paint(); }
    };
    window.addEventListener('scroll', spy, { passive: true });
    spy();
  }

  restore();
})();
