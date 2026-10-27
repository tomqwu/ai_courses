/* EN / 中文 (#116, #121): two editions of the same site — English at the root, Chinese in `zh/`.
 *
 * The switch in the top bar opens this same page (and part) in the other edition, and the choice
 * is remembered: an English page opened by someone who chose 中文 goes straight to its Chinese
 * copy, before it paints. The Chinese pages are written in Chinese by the build; what is left here
 * is the handful of labels the page's own scripts write later (the player, the quiz, the lab),
 * changed with the same table the build uses (ui-zh.json, loaded as assets/ui-zh.js).
 * This file loads in <head> without `defer`.
 */
(function () {
  'use strict';
  var KEY = 'aps-lang';
  var root = document.documentElement;
  var editions = (root.getAttribute('data-editions') || 'en').split(' ');
  var here = root.getAttribute('lang') === 'zh-Hans' ? 'zh' : 'en';
  var chosen = null;
  try { chosen = localStorage.getItem(KEY); } catch (e) { /* storage blocked */ }

  // The same page in the other edition: `…/zh/lab-m05.html#step-2` ⇄ `…/lab-m05.html#step-2`.
  function counterpart(lang) {
    var u = new URL(location.href);
    if (lang === 'zh' && here === 'en') u.pathname = u.pathname.replace(/\/([^\/]*)$/, '/zh/$1');
    else if (lang === 'en' && here === 'zh') u.pathname = u.pathname.replace(/\/zh\/([^\/]*)$/, '/$1');
    return u.href;
  }
  if (chosen === 'zh' && here === 'en' && editions.indexOf('zh') >= 0) {
    location.replace(counterpart('zh'));
    return;
  }

  // ── labels the page's scripts write after load (Chinese edition only) ──────────────────────
  var T = window.APSUiZh || { exact: {}, patterns: [] };
  var PATTERNS = (T.patterns || []).map(function (p) { return [new RegExp(p[0]), p[1]]; });
  function one(t) {
    if (Object.prototype.hasOwnProperty.call(T.exact, t)) return T.exact[t];
    for (var i = 0; i < PATTERNS.length; i++) {
      if (PATTERNS[i][0].test(t)) return t.replace(PATTERNS[i][0], PATTERNS[i][1]);
    }
    return null;
  }
  function label(text) {
    var t = (text || '').trim();
    if (!t) return null;
    var whole = one(t);
    if (whole !== null) return text.replace(t, whole);
    var seps = [' · ', ' — '];
    for (var s = 0; s < seps.length; s++) {
      if (t.indexOf(seps[s]) < 0) continue;
      var changed = false;
      var joined = t.split(seps[s]).map(function (piece) {
        var zh = one(piece);
        if (zh === null) return piece;
        changed = true;
        return zh;
      }).join(seps[s]);
      if (changed) return text.replace(t, joined);
    }
    return null;
  }
  var NEVER = 'script,style,pre,code,kbd,textarea';
  function fix(node) {
    if (node.nodeType === 3) {
      var zh = node.parentElement && !node.parentElement.closest(NEVER) && label(node.nodeValue);
      if (zh) node.nodeValue = zh;
      return;
    }
    if (node.nodeType !== 1 || node.closest(NEVER)) return;
    var walk = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
    var n;
    while ((n = walk.nextNode())) fix(n);
    [node].concat(Array.prototype.slice.call(node.querySelectorAll('[aria-label],[title]'))).forEach(function (el) {
      ['aria-label', 'title'].forEach(function (a) {
        var v = el.getAttribute && el.getAttribute(a);
        var zh = v && label(v);
        if (zh) el.setAttribute(a, zh);
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    Array.prototype.forEach.call(document.querySelectorAll('.lang-switch [data-lang]'), function (a) {
      var lang = a.getAttribute('data-lang');
      if (lang !== here) a.setAttribute('href', counterpart(lang));
      a.addEventListener('click', function () {
        try { localStorage.setItem(KEY, lang); } catch (e) { /* not remembered */ }
        // the part in view, not only the page: the hash follows what is on screen now
        if (lang !== here) a.setAttribute('href', counterpart(lang));
      });
    });
    if (here !== 'zh') return;
    fix(document.body);
    if (window.MutationObserver) {
      new MutationObserver(function (records) {
        records.forEach(function (r) {
          if (r.type === 'characterData') fix(r.target);
          else Array.prototype.forEach.call(r.addedNodes, fix);
        });
      }).observe(document.body, { childList: true, characterData: true, subtree: true });
    }
  });
  window.APSLocale = { lang: here, label: label, counterpart: counterpart };
})();
