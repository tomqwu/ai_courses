/* Lab page — the acceptance checklist you can tick, and the evidence entry you can export.
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
      var today = new Date().toISOString().slice(0, 10);
      var lines = ['## Evidence — ' + (v.project || '<project>') + ' — ' + root.getAttribute('data-lab-title') + ' — ' + (v.date || today), 'Commands (with results):'];
      (v.commands || '').split('\n').filter(function (l) { return l.trim(); }).forEach(function (l) { lines.push('- ' + l.trim()); });
      if (!(v.commands || '').trim()) lines.push('- <command> → <result>');
      lines.push('Environment: ' + (v.environment || '<OS, Python version, daemon state>'));
      lines.push('Revision: ' + (v.revision || '<git rev-parse HEAD>'));
      lines.push('Limitations / not verified:');
      (v.limitations || '').split('\n').filter(function (l) { return l.trim(); }).forEach(function (l) { lines.push('- ' + l.trim()); });
      if (!(v.limitations || '').trim()) lines.push('- <what this run does not prove>');
      out.value = lines.join('\n');
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
  restore();
})();
