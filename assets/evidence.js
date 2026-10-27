/* Your evidence log (#73) — every lab's evidence entry, from this browser's progress store.
 *
 * The entries are the ones written on each lab page, rendered by the same formatter the lab page
 * uses (APSProgress.evidenceMarkdown), so the log and the lab can never disagree about the format.
 */
(function () {
  'use strict';
  var root = document.querySelector('[data-evidence-log]');
  var P = window.APSProgress;
  if (!root || !P) return;
  var rows = Array.prototype.slice.call(document.querySelectorAll('[data-evidence-lab]'));

  function hasEntry(fields) {
    return Object.keys(fields || {}).some(function (k) { return (fields[k] || '').trim(); });
  }

  function entries() {
    var out = [];
    rows.forEach(function (row) {
      var deck = row.getAttribute('data-evidence-lab');
      var total = parseInt(row.getAttribute('data-lab-checks') || '0', 10);
      var lab = P.lab(deck);
      var ticked = Object.keys(lab.checks || {}).length;
      var number = 'Module ' + parseInt(deck.slice(1), 10);
      var state = row.querySelector('[data-evidence-state]');
      var pre = row.querySelector('[data-evidence-entry]');
      var checks = ticked + ' of ' + total + ' checklist items';
      if (hasEntry(lab.evidence)) {
        var text = P.evidenceMarkdown(lab.evidence, row.getAttribute('data-lab-title'));
        pre.textContent = text;
        pre.hidden = false;
        state.textContent = number + ' · ' + checks + ' · entry written';
        row.classList.add('has-entry');
        out.push(text);
      } else {
        pre.hidden = true;
        state.textContent = number + ' · ' + checks + ' · no entry yet';
        row.classList.remove('has-entry');
      }
    });
    return out;
  }

  function render() {
    var list = entries();
    var count = root.querySelector('[data-log-count]');
    if (count) count.textContent = list.length ? list.length + ' of ' + rows.length + ' labs have an entry'
      : 'No entries yet. Write one in the evidence form at the bottom of any lab page.';
    root.querySelectorAll('[data-log-copy],[data-log-download]').forEach(function (b) { b.disabled = !list.length; });
    return list;
  }

  function whole() {
    return '# Evidence log — AI Product Studio\n\n' + render().join('\n\n') + '\n';
  }

  root.addEventListener('click', function (e) {
    var copy = e.target.closest('[data-log-copy]');
    var dl = e.target.closest('[data-log-download]');
    if (copy) {
      navigator.clipboard.writeText(whole()).then(function () {
        copy.textContent = 'Copied to clipboard';
        setTimeout(function () { copy.textContent = 'Copy the whole log'; }, 1500);
      });
    } else if (dl) {
      var blob = new Blob([whole()], { type: 'text/markdown' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = 'evidence-log.md'; a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    }
  });
  document.addEventListener('aps:progress', render);
  render();
})();
