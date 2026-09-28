/* Home (#79) — where a returning learner was, and what is next.
 *
 * The build writes both states of the page; this shows the one that fits. A learner with a stored
 * position sees the resume card (the slide they stopped on, the unit and module, their place in the
 * deck, Resume and "Read this segment instead") and the next units of that module: the next lesson
 * unit not yet recorded, the lab with its time, the check with its size. A first-time visitor sees the
 * pitch and the first-win start. Everything shown is read from the progress store and the build's
 * own data (the module units, and search.json for the slide's title) — nothing is guessed.
 */
(function () {
  'use strict';
  var root = document.querySelector('[data-home]');
  var P = window.APSProgress;
  if (!root || !P) return;
  var data = {};
  try { data = JSON.parse(root.getAttribute('data-home') || '{}'); } catch (e) { data = {}; }
  var base = (document.body.getAttribute('data-site-base') || '.').replace(/\/$/, '');
  var slideInfo = {};   // "m02.html#slide-9" → { kicker, title }

  function set(sel, text) { var el = root.querySelector(sel); if (el) el.textContent = text; }

  function pathTitle() {
    var nav = document.querySelector('[data-outline]');
    var tracks = [];
    try { tracks = JSON.parse(nav.getAttribute('data-tracks') || '[]'); } catch (e) { tracks = []; }
    var slug = (P.path && P.path()) || 'aps';
    var t = tracks.filter(function (x) { return x.slug === slug; })[0] || tracks.filter(function (x) { return x.slug === 'aps'; })[0];
    return t ? t.title : '';
  }

  function row(kind, title, meta, href) {
    return '<li><a href="' + href + '"><span class="next-kind">' + kind + '</span><span class="next-title"></span>'
      + '<span class="next-meta">' + meta + '</span></a></li>';
  }

  function render() {
    var s = P.get();
    var m = s.last && /^(m\d+)\.html#slide-(\d+)/.exec(s.last.href || '');
    var mod = m && (data.modules || {})[m[1]];
    var back = !!mod;
    root.hidden = !back;
    document.querySelectorAll('[data-home-new]').forEach(function (el) { el.hidden = back; });
    if (!back) return;
    var deck = m[1], n = parseInt(m[2], 10);
    var unit = mod.units.filter(function (u) { return n >= u.first && n <= u.last; })[0] || mod.units[0];
    var info = slideInfo[s.last.href] || {};
    var watching = unit.kind !== 'lab' && unit.kind !== 'quiz';

    set('[data-home-path]', pathTitle());
    set('[data-resume-where]', 'Module ' + mod.number + ' · ' + mod.title);
    set('[data-resume-unit]', unit.kind === 'segment' ? unit.id + ' — ' + unit.label : unit.name);
    set('[data-resume-slide]', 'Part ' + n + ' of ' + mod.slides + (info.title ? ' · ' + info.title : ''));
    set('[data-resume-count]', n + ' of ' + mod.slides + ' parts');
    set('[data-thumb-kicker]', info.kicker || ('M' + mod.number));
    set('[data-thumb-title]', info.title || unit.name);
    var fill = root.querySelector('[data-resume-fill]');
    if (fill) fill.style.width = Math.round(n / mod.slides * 100) + '%';
    var resume = root.querySelector('[data-resume-link]');
    resume.setAttribute('href', base + '/' + s.last.href);
    var read = root.querySelector('[data-resume-read]');
    read.hidden = !watching;
    read.setAttribute('href', base + '/lesson-' + deck + '.html' + (unit.read ? '#' + unit.read : ''));

    // Next in this module: the next lesson unit not yet recorded, then the lab and the check.
    set('[data-next-title]', 'Next in Module ' + mod.number);
    var here = mod.units.indexOf(unit);
    var next = mod.units.filter(function (u, i) {
      return i > here && u.kind !== 'lab' && u.kind !== 'quiz' && !s.units[deck + ':' + u.id];
    })[0];
    var lab = mod.units.filter(function (u) { return u.kind === 'lab'; })[0];
    var quiz = mod.units.filter(function (u) { return u.kind === 'quiz'; })[0];
    var items = [];
    if (next) items.push([ 'Learn', next.name, (next.last - next.first + 1) + ' parts', base + '/' + next.href ]);
    if (lab) items.push([ 'Lab', lab.name, mod.lab + (s.units[deck + ':lab'] ? ' · done' : ''), base + '/' + lab.href ]);
    if (quiz) items.push([ 'Check', 'Knowledge check', mod.questions + ' questions' + (s.units[deck + ':quiz'] ? ' · passed' : ''), base + '/' + quiz.href ]);
    var list = root.querySelector('[data-next-list]');
    list.innerHTML = items.map(function (it) { return row(it[0], it[1], it[2], it[3]); }).join('');
    // Titles are set as text, never as markup.
    Array.prototype.forEach.call(list.querySelectorAll('.next-title'), function (el, i) { el.textContent = items[i][1]; });
  }

  document.addEventListener('aps:progress', render);
  render();
  // The slide's own title and kicker, for the resume card's thumbnail: from the search index the
  // build already writes, fetched only when there is a position to resume.
  if (!root.hidden) {
    fetch(base + '/search.json').then(function (r) { return r.ok ? r.json() : []; }).then(function (idx) {
      idx.forEach(function (it) {
        if (it.k !== 'slide') return;
        var parts = it.t.split(' — ');
        slideInfo[it.h] = { kicker: parts.length > 1 ? parts[0] : '', title: parts.length > 1 ? parts.slice(1).join(' — ') : it.t };
      });
      render();
    }).catch(function () { /* the card stands without the slide's title */ });
  }
})();
