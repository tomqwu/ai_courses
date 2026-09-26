/* The course outline (#73) — every page's left column.
 *
 * The outline is rendered at build time; this script only colours it from the learner's stored
 * progress (APSProgress) and keeps it honest as they work:
 *
 *   done         every unit of it recorded complete
 *   in progress  something recorded — a unit done, a checklist ticked, a score kept, or the last
 *                slide the learner stopped on is inside it
 *   not started  nothing recorded yet
 *
 * Each state is a different shape and a word (the visually hidden status text), never a colour
 * alone. On a deck page it follows the player from slide to slide (the `aps:slide` event), and
 * below 1024px it is a drawer the top bar opens.
 */
(function () {
  'use strict';
  var nav = document.querySelector('[data-outline]');
  if (!nav) return;
  var P = window.APSProgress;
  var WORD = { done: 'done', progress: 'in progress', todo: 'not started' };
  var tracks = [];
  try { tracks = JSON.parse(nav.getAttribute('data-tracks') || '[]'); } catch (e) { tracks = []; }

  function mark(el, status) {
    el.classList.remove('is-done', 'is-progress', 'is-todo');
    el.classList.add('is-' + status);
    var word = el.querySelector('[data-status-text]');
    if (word) word.textContent = WORD[status];
  }

  // Where the learner stopped: "m02.html#slide-9" → { deck: "m02", n: 9 }.
  function lastSlide(s) {
    var m = s.last && /^(m\d+)\.html#slide-(\d+)/.exec(s.last.href || '');
    return m ? { deck: m[1], n: parseInt(m[2], 10) } : null;
  }

  function unitStatus(s, id, first, last) {
    if (s.units[id]) return 'done';
    var deck = id.split(':')[0], kind = id.split(':')[1];
    if (kind === 'lab') {
      var lab = s.labs[deck];
      return lab && Object.keys(lab.checks || {}).length ? 'progress' : 'todo';
    }
    if (kind === 'quiz') return s.quizzes[deck] ? 'progress' : 'todo';
    var at = lastSlide(s);
    return at && at.deck === deck && at.n >= first && at.n <= last ? 'progress' : 'todo';
  }

  function moduleStatus(s, deck, ids) {
    var done = ids.filter(function (id) { return !!s.units[id]; }).length;
    if (ids.length && done === ids.length) return 'done';
    var at = lastSlide(s);
    var lab = s.labs[deck];
    if (done || (at && at.deck === deck) || s.quizzes[deck] ||
        (lab && Object.keys(lab.checks || {}).length)) return 'progress';
    return 'todo';
  }

  function currentTrack(s) {
    var slug = (P && P.path && P.path()) || 'aps';
    for (var i = 0; i < tracks.length; i++) if (tracks[i].slug === slug) return tracks[i];
    for (var j = 0; j < tracks.length; j++) if (tracks[j].slug === 'aps') return tracks[j];
    return tracks[0] || null;
  }

  function renderPath(s) {
    var box = nav.querySelector('[data-outline-path]');
    var track = currentTrack(s);
    if (!box || !track) return;
    var title = box.querySelector('[data-path-title]');
    if (title) { title.textContent = track.title; title.setAttribute('href', base() + '/' + track.href); }
    var list = box.querySelector('[data-path-segments]');
    var complete = 0;
    var html = track.modules.map(function (entry) {
      var deck = entry[0], ids = entry[1];
      var done = ids.filter(function (id) { return !!s.units[id]; }).length;
      var status = ids.length && done === ids.length ? 'done' : (done ? 'progress' : 'todo');
      if (status === 'done') complete++;
      return '<li data-seg="' + deck + '" class="is-' + status + '"></li>';
    }).join('');
    if (list) list.innerHTML = html;
    var count = box.querySelector('[data-path-count]');
    if (count) count.textContent = complete + ' of ' + track.modules.length + ' modules complete';
  }

  // The module page's start point (#74): "Resume · slide N" once the learner has stopped inside the
  // deck past its cover; otherwise the build's "Start module".
  function renderStart(s) {
    document.querySelectorAll('[data-module-start]').forEach(function (box) {
      var link = box.querySelector('[data-start-link]');
      var label = box.querySelector('[data-start-label]');
      var note = box.querySelector('[data-start-note]');
      if (!link.hasAttribute('data-start-href')) {
        link.setAttribute('data-start-href', link.getAttribute('href'));
        if (note) note.setAttribute('data-start-text', note.textContent);
      }
      var at = lastSlide(s);
      if (at && at.deck === box.getAttribute('data-module-start') && at.n > 1) {
        link.setAttribute('href', base() + '/' + s.last.href);
        label.textContent = 'Resume · slide ' + at.n;
        if (note) note.textContent = 'Where you stopped: ' + (s.last.label || 'slide ' + at.n) + '.';
      } else {
        link.setAttribute('href', link.getAttribute('data-start-href'));
        label.textContent = 'Start module';
        if (note) note.textContent = note.getAttribute('data-start-text');
      }
    });
  }

  function base() {
    return (document.body.getAttribute('data-site-base') || '.').replace(/\/$/, '');
  }

  function render() {
    if (!P) return;
    var s = P.get();
    nav.querySelectorAll('[data-module]').forEach(function (row) {
      var ids = (row.getAttribute('data-module-units') || '').split(',').filter(Boolean);
      var link = row.querySelector(':scope > a');
      if (link) mark(link, moduleStatus(s, row.getAttribute('data-module'), ids));
    });
    nav.querySelectorAll('[data-unit]').forEach(function (a) {
      mark(a, unitStatus(s, a.getAttribute('data-unit'),
        parseInt(a.getAttribute('data-first'), 10), parseInt(a.getAttribute('data-last'), 10)));
    });
    renderPath(s);
    renderStart(s);
  }

  // The deck page: the unit holding the current slide is "you are here".
  function follow(n) {
    nav.querySelectorAll('[data-unit]').forEach(function (a) {
      var kind = a.getAttribute('data-unit').split(':')[1];
      if (kind === 'lab' || kind === 'quiz') return;       // those units are their own pages
      var here = n >= parseInt(a.getAttribute('data-first'), 10) && n <= parseInt(a.getAttribute('data-last'), 10);
      if (here) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
    });
  }
  document.addEventListener('aps:slide', function (e) { follow(e.detail.n); });

  // A path page sets the learner's path; the outline shows that path from then on.
  var path = document.body.getAttribute('data-path');
  if (path && P && P.setPath) P.setPath(path);

  /* ---------------------------------------------------------- the drawer, below 1024px */
  var toggle = document.querySelector('[data-outline-toggle]');
  var backdrop = document.querySelector('[data-outline-backdrop]');
  var closeBtn = nav.querySelector('[data-outline-close]');
  var narrow = window.matchMedia('(max-width: 1023.98px)');

  function setOpen(open, restoreFocus) {
    document.body.classList.toggle('outline-open', open);
    if (toggle) toggle.setAttribute('aria-expanded', String(open));
    if (backdrop) backdrop.hidden = !open;
    if (open) {
      var here = nav.querySelector('[aria-current]') || nav.querySelector('a, button');
      if (here) here.focus();
    } else if (restoreFocus && toggle) {
      toggle.focus();
    }
  }
  if (toggle) toggle.addEventListener('click', function () {
    setOpen(!document.body.classList.contains('outline-open'), false);
  });
  if (closeBtn) closeBtn.addEventListener('click', function () { setOpen(false, true); });
  if (backdrop) backdrop.addEventListener('click', function () { setOpen(false, true); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && document.body.classList.contains('outline-open') && narrow.matches) {
      setOpen(false, true);
    }
  });
  // Opening a search from the drawer, or widening the window, closes it.
  nav.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('[data-search-open]') && narrow.matches) setOpen(false, false);
  });
  var onWidth = function () { if (!narrow.matches) setOpen(false, false); };
  if (narrow.addEventListener) narrow.addEventListener('change', onWidth);

  document.addEventListener('aps:progress', render);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render); else render();
})();
