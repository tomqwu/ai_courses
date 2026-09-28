/* EN / 中文 (#116): the course stays in English; 中文 adds Chinese where a learner needs it.
 *
 * The switch in the top bar is remembered in this browser. In 中文:
 *  - a key term shows its Chinese name beside it the first time it appears in each part (a Learn
 *    part, a lesson section, a lab step, a question) — "tenant isolation（租户隔离）". The name is a
 *    CSS pseudo-element on a wrapper, so the words themselves never change: narration, search and
 *    the read-aloud voice see the same English text.
 *  - the glossaries show each term's Chinese name and a one-line Chinese definition (rendered by
 *    the build, shown by the `is-zh` class this sets before the page paints).
 *  - the site's own controls (modes, buttons, headings the site writes) read in Chinese.
 * Terms come from course/06-production/terms-zh.json (emitted as assets/terms-zh.js) and are named
 * on module pages only; a generic word (commit, contract, drift) only in the modules whose glossary
 * defines it, so it means on the page what the glossary says.
 * This file loads in <head> without `defer`, so the class is set before first paint.
 */
(function () {
  'use strict';
  var KEY = 'aps-lang';
  var root = document.documentElement;
  var lang = 'en';
  try { if (localStorage.getItem(KEY) === 'zh') lang = 'zh'; } catch (e) { /* storage blocked: English */ }
  if (lang === 'zh') root.classList.add('is-zh');

  // The site's own words. Exact labels first; then the few that carry a number.
  var UI = {
    'Learn': '学习', 'Read': '阅读', 'Lab': '实验', 'Check': '测验',
    'Lesson': '课文', 'Handout': '讲义', 'Glossary': '术语表', 'Course': '课程',
    'Home': '首页', 'Modules': '模块', 'Outline': '目录', 'Search the course': '搜索课程',
    'Your path': '你的路线', 'Change path': '更换路线', 'Paths': '学习路线',
    'On this page': '本页内容', 'Overview': '概览', 'Objective': '目标', 'Action step': '行动步骤',
    'Introduction': '导论', 'Summary': '总结', 'Recap': '回顾', 'Discussion prompt': '讨论题',
    'Knowledge check': '知识测验', 'By the end you can…': '学完后你能够…',
    'Terms people get wrong': '常被误解的术语', 'Curated resources': '精选资源',
    'Sources and speaker notes': '来源与讲者备注', 'Transcript': '文字稿',
    'Listen to this unit': '收听本单元', 'Listen to this section': '收听本节',
    'Play narration': '播放讲解', 'Pause narration': '暂停讲解', 'Pause this section': '暂停本节',
    'Narration': '讲解', 'Narration speed': '讲解语速',
    'Check answer': '核对答案', 'Reveal the model answer': '查看参考答案', 'Your answer': '你的答案',
    'Correct answer': '正确答案', 'Correct answer · yours': '正确答案 · 你的选择', 'Try again': '重新作答',
    'Write': '作答', 'Before you start': '开始之前', "You're done when…": '完成标准…',
    'Three gotchas': '三个易错点', 'Evidence': '证据', 'Evidence to record': '需记录的证据',
    'Copy': '复制', 'Copied': '已复制', 'Copy evidence entry': '复制证据条目', 'Download .md': '下载 .md',
    'Project': '项目', 'Date': '日期', 'Environment': '环境', 'Level': '等级',
    'Continue': '继续', 'Resume': '继续学习', 'Start': '开始', 'Start module': '开始本模块', 'Done': '已完成',
    'to do': '待完成', 'Unit': '单元', 'Skip to content': '跳到正文', 'Search': '搜索',
    'move': '移动', 'open': '打开', 'anywhere': '随处可用',
    'Searches slides, narration, lessons, labs and the glossary': '搜索讲解、课文、实验和术语表',
    'Your evidence log': '你的证据日志', 'Copy the whole log': '复制整份日志',
    'Download evidence-log.md': '下载 evidence-log.md', 'no entry yet': '尚无条目',
    'Master glossary': '总术语表', 'pass/fail': '通过/不通过', 'Pass gate': '通过关卡',
    'Acceptance checklist (all must be true)': '验收清单（必须全部满足）',
    'Write and export the evidence entry': '撰写并导出证据条目',
    'Commands, one per line, with results': '命令（每行一条）及结果',
    'Revision (git rev-parse HEAD)': '版本（git rev-parse HEAD）',
    'Limitations / not verified, one per line': '局限 / 未验证（每行一条）',
    'Evidence entry (Markdown)': '证据条目（Markdown）',
    'Back to the module →': '返回模块 →', 'Read →': '阅读 →', 'Read the transcript': '阅读文字稿',
    'Exercise': '练习', 'full module': '完整模块',
    'This module belongs to one path.': '本模块属于一条路线。',
    'Every unit of this module is in the path.': '本模块的每个单元都在这条路线中。',
    'Browse all modules →': '浏览全部模块 →', 'Open this path →': '打开这条路线 →',
    'Export progress': '导出进度', 'Import': '导入', 'Reset': '重置',
    'Your progress lives in this browser.': '你的进度保存在此浏览器中。',
    'How each number is checked': '每个数字如何核验', 'Read this segment instead': '改为阅读这一段',
    'Press play to listen from the start': '按播放键从头收听', 'Lab checks': '实验检查',
    'lab': '实验', 'knowledge check': '知识测验'
  };
  var PATTERNS = [
    [/^Unit (\d+) of (\d+)$/, '第 $1 单元 · 共 $2 单元'],
    [/^Section (\d+) of (\d+)$/, '第 $1 节 · 共 $2 节'],
    [/^Question (\d+) of (\d+)$/, '第 $1 题 · 共 $2 题'],
    [/^Mark step (\d+) done$/, '标记第 $1 步完成'],
    [/^Resume · part (\d+)$/, '继续 · 第 $1 部分'],
    [/^(\d+) of (\d+) modules complete$/, '已完成 $1 / $2 个模块'],
    [/^(\d+) of (\d+) checklist items$/, '清单 $1 / $2 项'],
    [/^(\d+) of (\d+) units$/, '第 $1 / $2 单元'],
    [/^Module (\d+)$/, '模块 $1'],
    [/^(\d+) units?$/, '$1 个单元'], [/^(\d+) parts?$/, '$1 个部分'], [/^(\d+) steps?$/, '$1 个步骤'],
    [/^(\d+) terms$/, '$1 个术语'], [/^(\d+) shared across modules$/, '$1 个跨模块共用'],
    [/^(\d+) questions$/, '$1 道题'],
    [/^([\d.]+) min narrated$/, '讲解 $1 分钟'], [/^([\d.]+) min$/, '$1 分钟'], [/^(\d+) sec$/, '$1 秒'],
    [/^(\d+) checks decide the grade$/, '$1 项检查决定成绩'],
    [/^(\d+) multiple choice \+ (\d+) short answer$/, '$1 道选择题 + $2 道简答题'],
    [/^Objective: (.+)$/, '目标：$1']
  ];
  function one(t) {
    if (Object.prototype.hasOwnProperty.call(UI, t)) return UI[t];
    for (var i = 0; i < PATTERNS.length; i++) {
      if (PATTERNS[i][0].test(t)) return t.replace(PATTERNS[i][0], PATTERNS[i][1]);
    }
    return null;
  }
  // A label, or a run of labels joined by " · " ("Module 5 · Lab · pass/fail"): each piece the
  // site wrote is changed; a piece it did not (a module's title) stays as written.
  function label(text) {
    var t = text.trim();
    if (!t) return null;
    var whole = one(t);
    if (whole !== null) return text.replace(t, whole);
    if (t.indexOf(' · ') < 0) return null;
    var changed = false;
    var joined = t.split(' · ').map(function (piece) {
      var zh = one(piece);
      if (zh === null) return piece;
      changed = true;
      return zh;
    }).join(' · ');
    return changed ? text.replace(t, joined) : null;
  }
  var NEVER = 'script,style,pre,code,kbd,textarea,.said,.learn-said,.lab-command,.term-zh';
  var original = [];   // [textNode, English] for every label changed, so EN puts it back
  function translate(node) {
    var walk = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
    var n;
    while ((n = walk.nextNode())) {
      if (!n.parentElement || n.parentElement.closest(NEVER)) continue;
      var zh = label(n.nodeValue);
      if (zh !== null) { original.push([n, n.nodeValue]); n.nodeValue = zh; }
    }
    // Labels a screen reader hears: aria-label and title on the site's controls.
    var els = node.querySelectorAll ? node.querySelectorAll('[aria-label],[title]') : [];
    Array.prototype.forEach.call(els, function (el) {
      ['aria-label', 'title'].forEach(function (a) {
        var v = el.getAttribute(a);
        var zh = v && label(v);
        if (zh) { original.push([el, v, a]); el.setAttribute(a, zh); }
      });
    });
  }
  function untranslate() {
    original.forEach(function (o) {
      if (o[2]) o[0].setAttribute(o[2], o[1]); else o[0].nodeValue = o[1];
    });
    original = [];
  }

  // ── terms: the first use in each part gets its Chinese name ────────────────────────────────
  var SCOPES = '.learn-section,.qq,.lab-step,.doc-article';
  var RESET = 'h2,h3';             // a lesson section starts a new part
  var SKIP = 'pre,code,a,h1,h2,h3,h4,figure,.fig,button,label,kbd,script,style,textarea,.sr-only,' +
             '.term-zh,.page-kicker,.q-option,dt,.glossary-all,.glossary-doc,.toc,.view-tabs';
  var termsDone = false;
  function termList() {
    var data = window.APSTermsZh;
    if (!data) return [];
    var deck = document.body.getAttribute('data-deck');
    return deck ? data.filter(function (t) { return !t.m || t.m.indexOf(deck) >= 0; }) : [];
  }
  function escapeRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function markTerms() {
    if (termsDone) return;
    termsDone = true;
    var list = termList();
    if (!list.length) return;
    list.sort(function (a, b) { return b.t.length - a.t.length; });   // longest first
    var byKey = {};
    var alts = list.map(function (t) {
      byKey[t.t.toLowerCase().replace(/[\s-]+/g, ' ')] = t;
      return escapeRe(t.t).replace(/(\\-|\s)+/g, '[\\s-]+');
    });
    var rx = new RegExp('(^|[^A-Za-z0-9_])(' + alts.join('|') + ')(?![A-Za-z0-9_])', 'i');
    var main = document.getElementById('content');
    if (!main) return;
    Array.prototype.forEach.call(main.querySelectorAll(SCOPES), function (scope) {
      if (scope.parentElement && scope.parentElement.closest(SCOPES) &&
          !scope.matches('.learn-section,.qq,.lab-step')) return;
      if (scope.matches('.doc-article') && scope.querySelector('.learn-section,.qq,.lab-step')) return;
      if (scope.matches('.glossary-doc,.glossary-all')) return;   // the glossary names every term itself
      var seen = {};
      var walk = document.createTreeWalker(scope, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, {
        acceptNode: function (n) {
          if (n.nodeType === 1) {
            if (n !== scope && n.matches('.learn-section,.qq,.lab-step')) return NodeFilter.FILTER_REJECT;
            if (n.matches(RESET)) { seen = {}; return NodeFilter.FILTER_SKIP; }
            return n.matches(SKIP) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_SKIP;
          }
          return NodeFilter.FILTER_ACCEPT;
        }
      });
      var nodes = [], n;
      while ((n = walk.nextNode())) nodes.push([n, seen]);
      nodes.forEach(function (pair) {
        var node = pair[0], seenHere = pair[1];
        var text = node.nodeValue, m, guard = 0;
        while (text && (m = rx.exec(text)) && guard++ < 20) {
          var start = m.index + m[1].length, word = m[2];
          var t = byKey[word.toLowerCase().replace(/[\s-]+/g, ' ')];
          if (!t || seenHere[t.t]) {
            // Already named in this part: look past it.
            var rest = node.splitText(start + word.length);
            node = rest; text = rest.nodeValue;
            continue;
          }
          seenHere[t.t] = true;
          var hit = node.splitText(start);
          var after = hit.splitText(word.length);
          var span = document.createElement('span');
          span.className = 'term-zh';
          span.setAttribute('data-zh', t.zh);
          span.setAttribute('title', t.zh);
          hit.parentNode.insertBefore(span, hit);
          span.appendChild(hit);
          node = after; text = after.nodeValue;
        }
      });
    });
  }

  var observer = null;
  function set(next, remember) {
    lang = next;
    root.classList.toggle('is-zh', lang === 'zh');
    if (remember) { try { localStorage.setItem(KEY, lang); } catch (e) { /* not remembered */ } }
    Array.prototype.forEach.call(document.querySelectorAll('[data-lang]'), function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-lang') === lang));
    });
    if (lang === 'zh') {
      markTerms();
      translate(document.body);
      // Labels the page's scripts write later (the player, the quiz, the lab) change too.
      if (!observer && window.MutationObserver) {
        observer = new MutationObserver(function (records) {
          records.forEach(function (r) {
            if (r.type === 'characterData') {
              var n = r.target, zh = n.parentElement && !n.parentElement.closest(NEVER) && label(n.nodeValue);
              if (zh) { original.push([n, n.nodeValue]); n.nodeValue = zh; }
            } else {
              Array.prototype.forEach.call(r.addedNodes, function (a) {
                if (a.nodeType === 3) {
                  var zh = a.parentElement && !a.parentElement.closest(NEVER) && label(a.nodeValue);
                  if (zh) { original.push([a, a.nodeValue]); a.nodeValue = zh; }
                } else if (a.nodeType === 1 && !a.closest(NEVER)) translate(a);
              });
            }
          });
        });
      }
      if (observer) observer.observe(document.body, { childList: true, characterData: true, subtree: true });
    } else {
      if (observer) observer.disconnect();
      untranslate();
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('click', function (e) {
      var b = e.target.closest && e.target.closest('[data-lang]');
      if (b && b.getAttribute('data-lang') !== lang) set(b.getAttribute('data-lang'), true);
    });
    set(lang, false);
  });
  window.APSLocale = { get: function () { return lang; }, set: function (l) { set(l, true); } };
})();
