/* Site search — every unit, slide, lesson heading, lab, knowledge check and glossary term.
 *
 * The index is built at build time (search.json); this is a small client-side matcher with no
 * service behind it, so the site stays static. Press "/" anywhere, or use the search button.
 * Results are grouped by module and deep-link to the slide, heading or term.
 */
(function () {
  'use strict';
  var base = (document.body.getAttribute('data-site-base') || '.').replace(/\/$/, '');
  var index = null, loading = null;
  var KIND = { slide: 'Slide', unit: 'Unit', lesson: 'Lesson', 'lesson-heading': 'Lesson §', handout: 'Handout',
    'handout-heading': 'Handout §', glossary: 'Glossary', term: 'Term', lab: 'Lab', 'lab-heading': 'Lab §',
    quiz: 'Knowledge check', 'quiz-heading': 'Question' };

  var dialog = document.createElement('dialog');
  dialog.className = 'search-dialog';
  dialog.setAttribute('aria-label', 'Search the course');
  dialog.innerHTML =
    '<form class="search-form" role="search" onsubmit="return false">' +
    '<label class="sr-only" for="aps-search-input">Search the course</label>' +
    '<input id="aps-search-input" type="search" autocomplete="off" placeholder="Search units, slides, lessons, labs, terms…  (Esc closes)">' +
    '<button type="button" data-search-close aria-label="Close search">Close ×</button></form>' +
    '<p class="search-hint" data-search-hint>Type at least two characters. Results open the slide, heading or term directly.</p>' +
    '<div class="search-results" data-search-results role="listbox" aria-label="Results"></div>';
  document.body.appendChild(dialog);
  var input = dialog.querySelector('input');
  var results = dialog.querySelector('[data-search-results]');
  var hint = dialog.querySelector('[data-search-hint]');

  function load() {
    if (index) return Promise.resolve(index);
    if (!loading) {
      loading = fetch(base + '/search.json').then(function (r) { return r.ok ? r.json() : []; })
        .then(function (data) { index = data; return data; })
        .catch(function () { index = []; return index; });
    }
    return loading;
  }

  function open() {
    load();
    if (!dialog.open) dialog.showModal();
    input.value = '';
    results.innerHTML = '';
    hint.hidden = false;
    setTimeout(function () { input.focus(); }, 0);
  }
  function close() { if (dialog.open) dialog.close(); }

  function escapeHtml(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function score(item, terms) {
    var t = item.t.toLowerCase(), x = (item.x || '').toLowerCase(), m = (item.m || '').toLowerCase();
    var s = 0;
    for (var i = 0; i < terms.length; i++) {
      var q = terms[i];
      if (!q) continue;
      if (t === q) s += 40;
      else if (t.indexOf(q) === 0) s += 20;
      else if (t.indexOf(q) >= 0) s += 12;
      else if (m.indexOf(q) >= 0) s += 4;
      else if (x.indexOf(q) >= 0) s += 3;
      else return 0;
    }
    if (item.k === 'term') s += 6;
    if (item.k === 'unit' || item.k === 'lesson' || item.k === 'lab' || item.k === 'quiz') s += 3;
    return s;
  }

  function snippet(item, terms) {
    var x = item.x || '';
    var q = terms[0] || '';
    var i = q ? x.toLowerCase().indexOf(q) : -1;
    if (i < 0) return escapeHtml(x.slice(0, 120));
    var start = Math.max(0, i - 50), end = Math.min(x.length, i + 90);
    var out = (start ? '…' : '') + escapeHtml(x.slice(start, i)) + '<mark>' + escapeHtml(x.slice(i, i + q.length)) + '</mark>' + escapeHtml(x.slice(i + q.length, end)) + (end < x.length ? '…' : '');
    return out;
  }

  function render(query) {
    var terms = query.toLowerCase().split(/\s+/).filter(function (w) { return w.length >= 2; });
    if (!terms.length) { results.innerHTML = ''; hint.hidden = false; return; }
    hint.hidden = true;
    load().then(function (data) {
      var hits = [];
      for (var i = 0; i < data.length; i++) {
        var s = score(data[i], terms);
        if (s > 0) hits.push({ s: s, it: data[i] });
      }
      hits.sort(function (a, b) { return b.s - a.s; });
      hits = hits.slice(0, 40);
      if (!hits.length) { results.innerHTML = '<p class="search-empty">No matches. Try a shorter word, or a term from the glossary.</p>'; return; }
      var groups = {};
      var order = [];
      hits.forEach(function (h) {
        var d = h.it.d || 'course';
        if (!groups[d]) { groups[d] = []; order.push(d); }
        groups[d].push(h.it);
      });
      results.innerHTML = order.map(function (d) {
        var label = d === 'course' ? 'Course' : ('Module ' + parseInt(d.slice(1), 10));
        return '<section class="search-group"><h3>' + label + '</h3>' + groups[d].map(function (it) {
          return '<a class="search-hit" role="option" href="' + base + '/' + it.h + '">' +
            '<span class="search-kind">' + (KIND[it.k] || it.k) + '</span>' +
            '<span class="search-title">' + escapeHtml(it.t) + '</span>' +
            (it.x ? '<span class="search-snippet">' + snippet(it, terms) + '</span>' : '') + '</a>';
        }).join('') + '</section>';
      }).join('');
    });
  }

  var timer = 0;
  input.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(function () { render(input.value); }, 80); });
  dialog.querySelector('[data-search-close]').addEventListener('click', close);
  dialog.addEventListener('click', function (e) { if (e.target === dialog) close(); });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') { var first = results.querySelector('.search-hit'); if (first) { first.focus(); e.preventDefault(); } }
  });
  results.addEventListener('keydown', function (e) {
    var hitsEls = Array.prototype.slice.call(results.querySelectorAll('.search-hit'));
    var i = hitsEls.indexOf(document.activeElement);
    if (e.key === 'ArrowDown' && i < hitsEls.length - 1) { hitsEls[i + 1].focus(); e.preventDefault(); }
    else if (e.key === 'ArrowUp') { if (i > 0) hitsEls[i - 1].focus(); else input.focus(); e.preventDefault(); }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && !e.metaKey && !e.ctrlKey && !e.altKey) {
      var tag = (e.target.tagName || '').toLowerCase();
      if (['input', 'textarea', 'select'].indexOf(tag) >= 0) return;
      if (document.querySelector('dialog[open]') && !dialog.open) return;
      e.preventDefault(); open();
    }
  });
  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('[data-search-open]') : null;
    if (t) { e.preventDefault(); open(); }
  });
  window.APSSearch = { open: open, close: close };
})();
