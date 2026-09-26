/* Lab page — the workspace (#77): the steps one at a time, the acceptance checklist you can tick
 * beside them, and the evidence entry you can export.
 *
 * Steps: the list on the left says done, current or to do (a shape and a word); "Mark done, next
 * step" records the step and moves on, and the state persists like the checklist does. A deep link
 * to a step, or to anything inside one, opens that step.
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
    if (done) done.hidden = !(boxes.length && n === boxes.length);
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
    var copy = form.querySelector('[data-evidence-copy]');
    if (copy) copy.addEventListener('click', function () {
      build();
      navigator.clipboard.writeText(out.value).then(function () { copy.textContent = 'Copied to clipboard'; setTimeout(function () { copy.textContent = 'Copy evidence entry'; }, 1500); });
    });
    var dl = form.querySelector('[data-evidence-download]');
    if (dl) dl.addEventListener('click', function () {
      build();
      var blob = new Blob([out.value + '\n'], { type: 'text/markdown' });
      var a = document.createElement('a'); a.href = URL.createObjectURL(blob);
      a.download = 'evidence-' + deck + '.md'; a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    });
    build();
  }
  /* ---------------------------------------------------------- steps */
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
  }

  function show(i, focus) {
    if (!views.length) return;
    current = Math.max(0, Math.min(views.length - 1, i));
    views.forEach(function (v, n) { v.hidden = n !== current; });
    paint();
    if (P && P.setLabSteps) P.setLabSteps(deck, current, done);
    if (focus) {
      // Only the learner's own navigation writes the hash. Written during load, it becomes the
      // fragment the browser scrolls to and starts keyboard focus from, skipping the skip link.
      try { history.replaceState(null, '', '#' + views[current].id); } catch (e) { /* file:// */ }
      var h = views[current].querySelector('h2');
      if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
      var top = root.querySelector('.lab-workspace').getBoundingClientRect().top + window.scrollY - 80;
      if (window.scrollY > top) window.scrollTo({ top: top });
    }
  }

  // The step a hash names: the step itself, or the step holding the element.
  function stepFor(hash) {
    if (!hash || hash.length < 2) return -1;
    var el = document.getElementById(decodeURIComponent(hash.slice(1)));
    var step = el && el.closest ? el.closest('.lab-step') : null;
    return step ? views.indexOf(step) : -1;
  }

  if (views.length) {
    var saved = P ? P.lab(deck) : {};
    done = saved.steps || {};
    var fromHash = stepFor(location.hash);
    var firstOpen = 0;
    while (done[firstOpen] && firstOpen < views.length - 1) firstOpen++;
    show(fromHash >= 0 ? fromHash : (typeof saved.step === 'number' ? saved.step : firstOpen), false);
    if (fromHash >= 0) {
      var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (target && target !== views[fromHash]) target.scrollIntoView();
    }
    links.forEach(function (a, i) {
      a.addEventListener('click', function (ev) { ev.preventDefault(); show(i, true); });
    });
    root.addEventListener('click', function (ev) {
      if (ev.target.closest('[data-step-prev]')) { show(current - 1, true); return; }
      if (ev.target.closest('[data-step-next]')) {
        done[current] = true;
        if (current < views.length - 1) { show(current + 1, true); return; }
        show(current, false);
        var panel = root.querySelector('.lab-panel');
        var first = panel && panel.querySelector('[data-check]');
        if (first) first.focus();
      }
      var jump = ev.target.closest('[data-evidence-jump]');
      if (jump) {
        var field = root.querySelector('[data-evidence="project"]');
        if (field) { ev.preventDefault(); field.scrollIntoView({ block: 'center' }); field.focus(); }
      }
    });
    window.addEventListener('hashchange', function () {
      var n = stepFor(location.hash);
      if (n >= 0 && n !== current) show(n, true);
    });
  }

  restore();
})();
