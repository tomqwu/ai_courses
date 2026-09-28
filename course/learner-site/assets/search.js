/* Search as a command palette (#80) — slides and their narration, lesson and handout sections, lab
 * steps, glossary terms, from anywhere.
 *
 * Open it with ⌘K / Ctrl+K or "/", or any search button. It is a modal dialog (the rest of the page is
 * inert while it is open); ↑ ↓ move through the results, ↵ opens one, Esc closes. Results are grouped
 * by kind — Learn, Glossary, Lesson text, Labs — with the group holding the best match first, and the
 * matched words are highlighted. A slide found by a sentence of its narration opens the player at
 * the moment that sentence is spoken, when the copy publishes its captions.
 *
 * The index is built at build time (search.json); this is a small client-side matcher with no
 * service behind it, so the site stays static. The ranking keeps #39's rules: a whole-query title
 * match wins, and stop words ("vs.") do not block a match.
 */
(function () {
  'use strict';
  var base = (document.body.getAttribute('data-site-base') || '.').replace(/\/$/, '');
  var index = null, loading = null;
  var GROUPS = [
    { key: 'slides', label: 'Learn', kinds: ['slide'] },
    { key: 'glossary', label: 'Glossary', kinds: ['term'] },
    { key: 'lessons', label: 'Lesson text', kinds: ['lesson', 'lesson-heading', 'handout', 'handout-heading'] },
    { key: 'labs', label: 'Labs', kinds: ['lab', 'lab-heading'] },
    { key: 'other', label: 'Units, checks and pages', kinds: ['unit', 'quiz', 'quiz-heading', 'glossary', 'glossary-heading'] }
  ];
  var PER_GROUP = 6;

  var dialog = document.createElement('dialog');
  dialog.className = 'search-dialog';
  dialog.setAttribute('aria-label', 'Search the course');
  dialog.innerHTML =
    '<form class="search-form" role="search" onsubmit="return false">' +
    '<label class="search-field"><span class="search-field-label">Search</span>' +
    '<input id="aps-search-input" type="search" autocomplete="off" spellcheck="false" role="combobox"' +
    ' aria-expanded="false" aria-controls="aps-search-results" aria-autocomplete="list"' +
    ' placeholder="Parts, narration, lessons, labs, terms…"></label>' +
    '<button type="button" class="search-esc" data-search-close aria-label="Close search">esc</button></form>' +
    '<p class="search-hint" data-search-hint>Type at least two characters. Results open the slide, section, step or term directly.</p>' +
    '<div class="search-results" id="aps-search-results" data-search-results role="listbox" aria-label="Results"></div>' +
    '<p class="search-keys"><span><kbd>↑</kbd> <kbd>↓</kbd> move</span><span><kbd>↵</kbd> open</span>' +
    '<span><kbd>⌘K</kbd> anywhere</span><span>Searches slides, narration, lessons, labs and the glossary</span></p>';
  document.body.appendChild(dialog);
  var input = dialog.querySelector('input');
  var results = dialog.querySelector('[data-search-results]');
  var hint = dialog.querySelector('[data-search-hint]');
  var active = -1;

  function load() {
    if (index) return Promise.resolve(index);
    if (!loading) {
      loading = fetch(base + '/search.json').then(function (r) { return r.ok ? r.json() : []; })
        .then(function (data) {
          data.forEach(function (it) { it._s = (it.s || []).join(' '); });
          index = data; return data;
        })
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
    active = -1;
    input.setAttribute('aria-expanded', 'false');
    setTimeout(function () { input.focus(); }, 0);
  }
  function close() { if (dialog.open) dialog.close(); }

  function escapeHtml(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  // Words a query can carry without meaning: "Validate vs. Prove" should find the slides that say
  // validate and prove, not only the ones that also print "vs.".
  var STOP = ['vs', 'of', 'the', 'an', 'and', 'or', 'to', 'in', 'on', 'for', 'is'];

  function tokens(query) {
    return query.toLowerCase().split(/[\s()"“”‘’`]+/)
      // letters in any script: a Chinese term name (#116) is a word too
      .map(function (w) { return w.replace(/^[^\p{L}\p{N}_:]+|[^\p{L}\p{N}_]+$/gu, ''); })
      .filter(function (w) { return w.length >= 2 && STOP.indexOf(w) < 0; });
  }

  function score(item, terms, full) {
    var t = item.t.toLowerCase(), x = ((item.x || '') + ' ' + (item._s || '')).toLowerCase(), m = (item.m || '').toLowerCase();
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
    // The whole query naming an item outright beats its words scattered across others: a search
    // for "contract test" should open on the glossary entry, not on the slides that mention it.
    if (full && t === full) s += 60;
    else if (full && terms.length > 1 && t.indexOf(full) === 0) s += 15;
    if (item.k === 'term') s += 6;
    if (item.k === 'unit' || item.k === 'lesson' || item.k === 'lab' || item.k === 'quiz') s += 3;
    return s;
  }

  // Every matched word marked, in text that is escaped first.
  function mark(text, terms) {
    var out = escapeHtml(text);
    terms.slice().sort(function (a, b) { return b.length - a.length; }).forEach(function (q) {
      var rx = new RegExp('(' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
      out = out.replace(/(^|>)([^<]*)(?=<|$)/g, function (m, lead, body) { return lead + body.replace(rx, '<mark>$1</mark>'); });
    });
    return out;
  }

  function excerpt(text, terms) {
    var lower = text.toLowerCase();
    var i = -1;
    for (var k = 0; k < terms.length && i < 0; k++) i = lower.indexOf(terms[k]);
    if (i < 0) return text.slice(0, 140);
    var start = Math.max(0, i - 50), end = Math.min(text.length, i + 100);
    return (start ? '…' : '') + text.slice(start, end) + (end < text.length ? '…' : '');
  }

  // A slide: the narration sentence that holds the match (and when it is spoken), else its text.
  function slideHit(it, terms) {
    var sentences = it.s || [];
    for (var i = 0; i < sentences.length; i++) {
      var low = sentences[i].toLowerCase();
      if (terms.some(function (q) { return low.indexOf(q) >= 0; })) {
        var t = it.ts ? it.ts[i] : null;
        var href = it.h;
        if (t !== null && t !== undefined) href = it.h.replace('#', '?t=' + t + '#');
        return { href: href, quote: '“' + excerpt(sentences[i], terms) + '”', at: t };
      }
    }
    return { href: it.h, quote: excerpt(it.x || '', terms), at: null };
  }

  function query(q) {
    var terms = tokens(q);
    var full = q.toLowerCase().replace(/[`\s]+/g, ' ').trim();
    if (!terms.length || !index) return { terms: terms, groups: [] };
    var hits = [];
    for (var i = 0; i < index.length; i++) {
      var s = score(index[i], terms, full);
      if (s > 0) hits.push({ s: s, it: index[i] });
    }
    hits.sort(function (a, b) { return b.s - a.s; });
    var groups = GROUPS.map(function (g) {
      var mine = hits.filter(function (h) { return g.kinds.indexOf(h.it.k) >= 0; });
      return { key: g.key, label: g.label, best: mine.length ? mine[0].s : 0, count: mine.length, items: mine.slice(0, PER_GROUP) };
    }).filter(function (g) { return g.items.length; });
    groups.sort(function (a, b) { return b.best - a.best; });
    return { terms: terms, groups: groups };
  }

  function clock(t) { t = Math.floor(t); return Math.floor(t / 60) + ':' + String(t % 60).padStart(2, '0'); }

  function where(it) {
    var mod = it.d ? 'M' + parseInt(it.d.slice(1), 10) : 'Course';
    if (it.k === 'slide') return mod + ' · part ' + it.n;
    if (it.k === 'term') return mod + ' glossary';
    return mod + ' · ' + (it.m || '');
  }

  function render(q) {
    var found = query(q);
    var terms = found.terms;
    active = -1;
    input.removeAttribute('aria-activedescendant');
    if (!terms.length) { results.innerHTML = ''; hint.hidden = false; input.setAttribute('aria-expanded', 'false'); return; }
    hint.hidden = true;
    input.setAttribute('aria-expanded', 'true');
    if (!found.groups.length) { results.innerHTML = '<p class="search-empty">No matches. Try a shorter word, or a term from the glossary.</p>'; return; }
    var n = 0;
    results.innerHTML = found.groups.map(function (g) {
      return '<section class="search-group" data-group="' + g.key + '" role="group" aria-label="' + g.label + '">' +
        '<h3>' + g.label + (g.count > g.items.length ? ' <span>· ' + g.count + '</span>' : '') + '</h3>' +
        g.items.map(function (h) {
          var it = h.it, id = 'sr-' + (n++);
          var link = it.h, quote = it.x ? excerpt(it.x, terms) : '', thumb = '', title = it.t;
          if (it.k === 'slide') {
            var sh = slideHit(it, terms);
            link = sh.href; quote = sh.quote;
            // The slide's own title; its module and number are on the line below.
            title = it.t.split(' — ').slice(1).join(' — ') || it.t;
            thumb = '<span class="search-thumb" aria-hidden="true"><span>' + escapeHtml('M' + parseInt(it.d.slice(1), 10)) + '</span><span>' + it.n + '</span></span>';
            if (sh.at !== null) quote += ' · spoken at ' + clock(sh.at);
          }
          return '<a class="search-hit" role="option" id="' + id + '" href="' + base + '/' + link + '" data-kind="' + it.k + '">' + thumb +
            '<span class="search-main"><span class="search-title">' + mark(title, terms) + '</span>' +
            '<span class="search-where">' + escapeHtml(where(it)) + '</span>' +
            (quote ? '<span class="search-snippet">' + mark(quote, terms) + '</span>' : '') + '</span></a>';
        }).join('') + '</section>';
    }).join('');
  }

  function options() { return Array.prototype.slice.call(results.querySelectorAll('.search-hit')); }
  function highlight(i) {
    var all = options();
    if (!all.length) return;
    active = (i + all.length) % all.length;
    all.forEach(function (a, k) { a.classList.toggle('is-active', k === active); a.setAttribute('aria-selected', String(k === active)); });
    input.setAttribute('aria-activedescendant', all[active].id);
    all[active].scrollIntoView({ block: 'nearest' });
  }

  var timer = 0;
  input.addEventListener('input', function () {
    clearTimeout(timer);
    var q = input.value;
    timer = setTimeout(function () { load().then(function () { render(q); }); }, 60);
  });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') { highlight(active + 1); e.preventDefault(); }
    else if (e.key === 'ArrowUp') { highlight(active - 1); e.preventDefault(); }
    else if (e.key === 'Enter') {
      var all = options();
      var pick = all[active >= 0 ? active : 0];
      if (pick) { e.preventDefault(); close(); location.href = pick.href; }
    }
  });
  dialog.querySelector('[data-search-close]').addEventListener('click', close);
  dialog.addEventListener('click', function (e) { if (e.target === dialog) close(); });
  // Following a hit to the page already open (another slide of this deck) closes the palette.
  results.addEventListener('click', function () { close(); });

  document.addEventListener('keydown', function (e) {
    // ⌘K / Ctrl+K, the palette convention, works even from inside a field.
    if ((e.metaKey || e.ctrlKey) && !e.altKey && (e.key === 'k' || e.key === 'K')) {
      if (document.querySelector('dialog[open]') && !dialog.open) return;
      e.preventDefault(); if (dialog.open) close(); else open();
      return;
    }
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
  window.APSSearch = {
    open: open, close: close,
    // The ranked results for a query, as data — what the palette shows, for checks and tools.
    query: function (q) { return load().then(function () { return query(q); }); }
  };
})();
