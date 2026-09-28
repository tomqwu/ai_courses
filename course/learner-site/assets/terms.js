/* Terms explained where they are used (#term-links).
 *
 * A term's first use in a part is a link to its glossary entry, carrying its plain meaning. Hover
 * (or keyboard focus) shows a card with that meaning; on a touch screen the first tap shows the card
 * and a tap on "Full entry" (or the term again) opens the glossary. Esc or a tap elsewhere closes it.
 */
(function () {
  'use strict';
  var zh = document.documentElement.lang === 'zh-Hans';
  var card = document.createElement('div');
  card.className = 'term-card';
  card.setAttribute('role', 'tooltip');
  card.id = 'term-card';
  card.hidden = true;
  document.body.appendChild(card);
  var current = null, hideTimer = 0;
  // A finger has no hover: the first tap on a term shows its card, the next follows the link. The
  // mouse events a tap also fires are ignored, or they would open the card before the tap lands.
  var lastPointer = window.matchMedia('(hover: none)').matches ? 'touch' : 'mouse';
  var openAtDown = null;    // the term whose card was already open when this tap began
  document.addEventListener('pointerdown', function (e) {
    lastPointer = e.pointerType || 'mouse';
    openAtDown = current;
  }, true);
  var touch = { get matches() { return lastPointer === 'touch'; } };

  function show(a) {
    clearTimeout(hideTimer);
    current = a;
    card.textContent = '';
    var t = document.createElement('p'); t.className = 'term-card-title'; t.textContent = a.getAttribute('data-term-title');
    var p = document.createElement('p'); p.className = 'term-card-plain'; p.textContent = a.getAttribute('data-term-plain');
    card.appendChild(t); card.appendChild(p);
    var e = a.getAttribute('data-term-everyday');
    if (e) { var q = document.createElement('p'); q.className = 'term-card-everyday'; q.textContent = e; card.appendChild(q); }
    var more = document.createElement('a'); more.className = 'term-card-more'; more.href = a.href;
    more.textContent = zh ? '在术语表中查看完整条目 →' : 'Full entry in the glossary →';
    card.appendChild(more);
    card.hidden = false;
    a.setAttribute('aria-describedby', 'term-card');
    var r = a.getBoundingClientRect();
    var w = card.offsetWidth, h = card.offsetHeight;
    var left = Math.min(Math.max(8, r.left + window.scrollX), window.scrollX + document.documentElement.clientWidth - w - 8);
    var top = r.bottom + window.scrollY + 6;
    if (r.bottom + h + 12 > window.innerHeight && r.top > h + 12) top = r.top + window.scrollY - h - 6;
    card.style.left = left + 'px';
    card.style.top = top + 'px';
  }
  function hide(now) {
    clearTimeout(hideTimer);
    var go = function () { card.hidden = true; if (current) current.removeAttribute('aria-describedby'); current = null; };
    if (now) go(); else hideTimer = setTimeout(go, 180);
  }

  document.addEventListener('mouseover', function (e) {
    var a = e.target.closest && e.target.closest('a.term');
    if (a && !touch.matches) show(a);
    else if (!(e.target.closest && e.target.closest('.term-card')) && current && !touch.matches) hide(false);
  });
  card.addEventListener('mouseover', function () { clearTimeout(hideTimer); });
  document.addEventListener('focusin', function (e) {
    var a = e.target.closest && e.target.closest('a.term');
    if (a) show(a); else if (!(e.target.closest && e.target.closest('.term-card'))) hide(true);
  });
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a.term');
    if (a && touch.matches && openAtDown !== a) { e.preventDefault(); show(a); return; }
    if (!a && !(e.target.closest && e.target.closest('.term-card'))) hide(true);
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && current) hide(true); });
  window.addEventListener('scroll', function () { if (current && touch.matches) hide(true); }, { passive: true });
})();
