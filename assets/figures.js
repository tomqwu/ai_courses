/* System diagrams (#115): the arrows between components.
 *
 * The build lays the components out as HTML (layers of boxes that wrap and stack like any other text)
 * and lists the connections. This draws each connection as an arrow from where its two boxes actually
 * are: out of the side that faces the other box, a gentle curve, an arrowhead, and the label as an
 * HTML chip at its middle (so it wraps and is contrast-audited like every other line). It redraws
 * whenever the diagram changes size, so a phone's stacked layout gets arrows that fit it.
 * Build-in steps carry over: an edge's data-step is copied to its arrow and label, so the Learn
 * player's build (which toggles every [data-step] inside the figure) reveals them with their sentence.
 * Without JavaScript the connections list is the diagram's text.
 */
(function () {
  'use strict';
  var SVG = 'http://www.w3.org/2000/svg';
  var NARROW = 560;   // px: below this the connections are a list, not arrows

  // Which side of box `a` faces box `b`: boxes that share a row connect side to side; boxes in
  // different rows connect bottom to top (or top to bottom), never through a box's flank.
  function facing(a, b) {
    var sameRow = a.top < b.top + b.height && b.top < a.top + a.height;
    if (sameRow) return (b.left + b.width / 2) > (a.left + a.width / 2) ? 'right' : 'left';
    return (b.top + b.height / 2) > (a.top + a.height / 2) ? 'bottom' : 'top';
  }
  // The point on that side, spread when several arrows share it (k of n), and its outward normal.
  function anchor(r, sideName, k, n) {
    var t = (k + 1) / (n + 1), span = 0.6;
    var f = 0.5 + (t - 0.5) * span * 2 * 0.5;
    if (sideName === 'bottom') return { x: r.left + r.width * f, y: r.top + r.height, nx: 0, ny: 1 };
    if (sideName === 'top') return { x: r.left + r.width * f, y: r.top, nx: 0, ny: -1 };
    if (sideName === 'right') return { x: r.left + r.width, y: r.top + r.height * f, nx: 1, ny: 0 };
    return { x: r.left, y: r.top + r.height * f, nx: -1, ny: 0 };
  }

  function draw(sys) {
    var fig = sys.closest('.fig');
    var list = fig && fig.querySelector('.fig-edges');
    if (!list) return;
    var box = sys.getBoundingClientRect();
    var old = sys.querySelector('.fig-wires');
    if (old) old.remove();
    Array.prototype.forEach.call(sys.querySelectorAll('.fig-wire-label'), function (l) { l.remove(); });
    // Too narrow for a wiring diagram (a phone): the components stack and the connections are read
    // as their list instead of drawn as arrows that would cross every box.
    if (box.width < NARROW) {
      fig.classList.remove('is-drawn');
      list.classList.remove('sr-only');
      return;
    }
    var svg = document.createElementNS(SVG, 'svg');
    svg.setAttribute('class', 'fig-wires');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('width', box.width);
    svg.setAttribute('height', box.height);
    var defs = document.createElementNS(SVG, 'defs');
    defs.innerHTML = '<marker id="fig-head-' + (sys.dataset.sysId) + '" viewBox="0 0 10 10" refX="9" refY="5"' +
      ' markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 1L9 5L0 9z" class="fig-wire-head"/></marker>';
    svg.appendChild(defs);
    var rel = function (el) {
      var r = el.getBoundingClientRect();
      return { left: r.left - box.left, top: r.top - box.top, width: r.width, height: r.height };
    };
    // First pass: which side each end uses, so arrows sharing a side can be spread along it.
    var edges = [], slots = {};
    Array.prototype.forEach.call(list.querySelectorAll('.fig-edge'), function (li) {
      var a = sys.querySelector('[data-node="' + li.getAttribute('data-from') + '"]');
      var b = sys.querySelector('[data-node="' + li.getAttribute('data-to') + '"]');
      if (!a || !b) return;
      var ra = rel(a), rb = rel(b), sa = facing(ra, rb), sb = facing(rb, ra);
      var e = { li: li, ra: ra, rb: rb, ka: li.getAttribute('data-from') + ':' + sa, kb: li.getAttribute('data-to') + ':' + sb, sa: sa, sb: sb };
      e.ia = (slots[e.ka] = (slots[e.ka] || 0) + 1) - 1;
      e.ib = (slots[e.kb] = (slots[e.kb] || 0) + 1) - 1;
      edges.push(e);
    });
    var rects = Array.prototype.map.call(sys.querySelectorAll('[data-node]'), rel);
    var placed = [];
    edges.forEach(function (e) {
      var li = e.li;
      var p, q;
      // Same row, but another box between them: leave from the tops and arc over the row.
      var cx = function (r) { return r.left + r.width / 2; };
      var lo = Math.min(cx(e.ra), cx(e.rb)), hi = Math.max(cx(e.ra), cx(e.rb));
      var between = (e.sa === 'left' || e.sa === 'right') && rects.some(function (r) {
        var sameRow = r.top < e.ra.top + e.ra.height && e.ra.top < r.top + r.height;
        return sameRow && cx(r) > lo + 1 && cx(r) < hi - 1;
      });
      if (between) {
        p = anchor(e.ra, 'top', 0, 1); q = anchor(e.rb, 'top', 0, 1);
      } else {
        p = anchor(e.ra, e.sa, e.ia, slots[e.ka]); q = anchor(e.rb, e.sb, e.ib, slots[e.kb]);
      }
      var bend = between ? Math.max(40, Math.abs(q.x - p.x) / 4)
        : Math.max(18, Math.min(60, Math.hypot(q.x - p.x, q.y - p.y) / 3));
      var d = 'M' + p.x + ' ' + p.y + ' C' + (p.x + p.nx * bend) + ' ' + (p.y + p.ny * bend) + ' ' +
        (q.x + q.nx * bend) + ' ' + (q.y + q.ny * bend) + ' ' + q.x + ' ' + q.y;
      var path = document.createElementNS(SVG, 'path');
      path.setAttribute('d', d);
      path.setAttribute('class', 'fig-wire' + (li.classList.contains('is-hl') ? ' is-hl' : '') +
        (li.classList.contains('is-seam') ? ' is-seam' : ''));
      path.setAttribute('marker-end', 'url(#fig-head-' + sys.dataset.sysId + ')');
      var step = li.getAttribute('data-step');
      if (step !== null) path.setAttribute('data-step', step);
      if (li.classList.contains('is-pending')) path.classList.add('is-pending');
      svg.appendChild(path);
      var text = li.querySelector('.fig-edge-label');
      if (text) {
        var chip = document.createElement('span');
        chip.className = 'fig-wire-label' + (li.classList.contains('is-hl') ? ' is-hl' : '');
        chip.innerHTML = text.innerHTML;
        if (step !== null) chip.setAttribute('data-step', step);
        sys.appendChild(chip);
        // Place the label on its arrow where it covers no box and no other label: try the middle
        // first, then points either side of it, and keep the least-covered spot.
        var len = path.getTotalLength(), best = null;
        var cw = chip.offsetWidth, ch = chip.offsetHeight;
        // On the arrow first; then just beside it (above/below a sideways arrow, left/right of an
        // up/down one), since a short arrow between neighbours has no room along its length.
        var sideways = p.nx !== 0 && !between;
        var rowBottom = Math.max(e.ra.top + e.ra.height, e.rb.top + e.rb.height);
        var rowTop = Math.min(e.ra.top, e.rb.top);
        var mid0 = path.getPointAtLength(len / 2);
        var offsets = sideways
          // beside a sideways arrow means clear of the row: in the band below it, else above it
          ? [[0, 0], [0, rowBottom + ch / 2 + 6 - mid0.y], [0, rowTop - ch / 2 - 6 - mid0.y]]
          : [[0, 0], [cw / 2 + 7, 0], [-(cw / 2 + 7), 0]];
        var tries = [];
        offsets.forEach(function (o) { [0.5, 0.4, 0.6, 0.3, 0.7, 0.22, 0.78].forEach(function (t) { tries.push([t, o[0], o[1]]); }); });
        tries.some(function (tr) {
          var pt = path.getPointAtLength(len * tr[0]);
          var x = pt.x + tr[1], y = pt.y + tr[2];
          chip.style.left = x + 'px';
          chip.style.top = y + 'px';
          var c = rel(chip), cover = 0;
          rects.concat(placed).forEach(function (r) {
            var w = Math.min(c.left + c.width, r.left + r.width) - Math.max(c.left, r.left);
            var h = Math.min(c.top + c.height, r.top + r.height) - Math.max(c.top, r.top);
            if (w > 0 && h > 0) cover += w * h;
          });
          if (!best || cover < best.cover) best = { cover: cover, x: x, y: y };
          return cover === 0;
        });
        chip.style.left = best.x + 'px';
        chip.style.top = best.y + 'px';
        placed.push(rel(chip));
      }
    });
    sys.insertBefore(svg, sys.firstChild);
    fig.classList.add('is-drawn');
    list.classList.add('sr-only');   // drawn: the list is for screen readers; without JS it is the diagram's text
  }

  var systems = Array.prototype.slice.call(document.querySelectorAll('[data-sys]'));
  systems.forEach(function (sys, i) {
    sys.dataset.sysId = String(i);
    var frame = 0;
    var redraw = function () { cancelAnimationFrame(frame); frame = requestAnimationFrame(function () { draw(sys); }); };
    if (window.ResizeObserver) new ResizeObserver(redraw).observe(sys);
    window.addEventListener('load', redraw);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(redraw);
    draw(sys);
  });
})();
