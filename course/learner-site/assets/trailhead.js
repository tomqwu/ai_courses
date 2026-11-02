/* Trailhead home (Expedition). Reads the build's module data and the learner's local progress, and
 * paints the route map, the day trail and the field note. No progress is invented: an empty store
 * starts at Camp 0 with zero stamps and zero field notes. */
(function () {
  'use strict';
  var P = window.APSProgress;
  var root = document.querySelector('[data-home]');
  if (!P || !root) return;
  var data = {};
  try { data = JSON.parse(root.getAttribute('data-home') || '{}'); } catch (e) { data = {}; }
  var base = (document.body.getAttribute('data-page-base') || document.body.getAttribute('data-site-base') || '.').replace(/\/$/, '');
  var zh = document.body.getAttribute('data-lang') === 'zh';
  var NS = 'http://www.w3.org/2000/svg';
  var MODULES = Object.keys(data.modules || {}).map(function (id) { return data.modules[id]; })
    .sort(function (a, b) { return a.number - b.number; });
  if (!MODULES.length) return;
  var POS = {
    m00: [86, 120], m01: [258, 120], m02: [430, 120], m03: [602, 120], m04: [774, 120],
    m05: [774, 300], m06: [602, 300], m07: [430, 300], m08: [258, 300], m09: [86, 300]
  };
  var MAP_LABELS = {
    m00: ['Orientation', '导览'], m01: ['Operating system', '操作系统'], m02: ['On-device AI', '端侧 AI'],
    m03: ['Privacy & shipping', '隐私与发布'], m04: ['Spec-driven SaaS', '规格驱动 SaaS'],
    m05: ['Security & acceptance', '安全与验收'], m06: ['Expertise product', '专业知识产品'],
    m07: ['Monetize', '变现'], m08: ['Launch & capstone', '发布与毕业项目'], m09: ['GitHub Pages', 'GitHub Pages']
  };
  var NOTES = {
    m00: { q: 'Every claim on this page carries a file you can open — and the course checks its own claims every time it is built.', s: 'course/04-sales/landing-page.md', href: 'proof.html' },
    m01: { q: 'A change is done when it is merged to main with the three required checks green.', s: 'SignUpFlow/AGENTS.md:15-17', href: 'm01.html' },
    m02: { q: '“The newest segment always survives.” The context window keeps the most recent utterance even when the budget is full.', s: 'ListenToMe / ConversationStore.swift · 79–85 · a9bde8e', href: 'm02.html#slide-7' },
    m03: { q: 'Fail closed: a missing or remote model is rejected, never treated as local.', s: 'ListenToMe / ModelPrivacy.swift:15-24', href: 'm03.html' },
    m04: { q: 'The generated checklist reported “5xP1” while the spec marked six P1 stories.', s: 'SignUpFlow / specs/014-security-hardening/checklists/requirements.md', href: 'm04.html' },
    m05: { q: 'Five policy classes, 145 classified operations, checked against the live route table.', s: 'SignUpFlow / api/route_auth_policy.py', href: 'm05.html' },
    m06: { q: 'Four saving levels, each naming the evidence that can confirm it.', s: 'ai_qe / docs/principles.md', href: 'm06.html' },
    m07: { q: 'The comparator band comes from the 14-row competitor table, not from a feeling.', s: 'ListenToMe / docs/competition-analysis.md', href: 'm07.html' },
    m08: { q: 'The sales page measures 2,783 words total; the gate re-measures it after every edit.', s: 'course/04-sales/landing-page.md', href: 'm08.html' },
    m09: { q: 'Publishing can take up to ten minutes; the reusable file still says so in its text.', s: 'github.com/github/docs · twenty-minutes-to-publish.md', href: 'm09.html' }
  };
  var WEIGHT = { watched: 10, read: 10, passed: 40, completed: 100, migrated: 5 };

  function key(deck, unit) { return deck + ':' + unit.id; }
  function state() {
    var s = P.get();
    var units = {};
    MODULES.forEach(function (m) { m.units.forEach(function (u) { units[key(m.id, u)] = !!s.units[key(m.id, u)]; }); });
    var completed = MODULES.filter(function (m) { return m.units.every(function (u) { return units[key(m.id, u)]; }); });
    var partial = MODULES.filter(function (m) {
      var n = m.units.filter(function (u) { return units[key(m.id, u)]; }).length;
      return n > 0 && n < m.units.length;
    });
    var totalUnits = MODULES.reduce(function (n, m) { return n + m.units.length; }, 0);
    var doneUnits = Object.keys(units).filter(function (k) { return units[k]; }).length;
    // Where the learner actually is: the module of the last part they opened, not the first gap in
    // the course. A course can be read out of order; the map must not send them back.
    var last = /^([a-z]\d+)\.html#slide-(\d+)$/.exec((s.last && s.last.href) || '');
    var current = last ? last[1] : null;
    var start = 0;
    if (current) {
      start = MODULES.findIndex(function (m) { return m.id === current; });
      if (start < 0) { current = null; start = 0; }
    }
    if (!current) {
      var firstOpen = MODULES.filter(function (m) {
        return m.units.some(function (u) { return !units[key(m.id, u)]; });
      })[0];
      current = firstOpen ? firstOpen.id : MODULES[MODULES.length - 1].id;
      start = MODULES.findIndex(function (m) { return m.id === current; });
    }
    // The next leg is the first unfinished unit at or after the current camp, then anywhere.
    var order = MODULES.slice(start).concat(MODULES.slice(0, start));
    var next = null;
    order.forEach(function (m) {
      if (next) return;
      m.units.forEach(function (u) { if (!next && !units[key(m.id, u)]) next = { deck: m.id, unit: u, module: m }; });
    });
    if (!next && MODULES.every(function (m) { return m.units.every(function (u) { return units[key(m.id, u)]; }); })) {
      current = MODULES[MODULES.length - 1].id;
    } else if (next && MODULES.findIndex(function (m) { return m.id === next.deck; }) > MODULES.findIndex(function (m) { return m.id === current; })) {
      current = next.deck;
    }
    return { s: s, units: units, next: next, completed: completed, partial: partial, current: current,
             totalUnits: totalUnits, doneUnits: doneUnits, last: last };
  }

  function dayNumber(ms) {
    var d = new Date(ms);
    return Math.floor(new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime() / 86400000);
  }
  function trail(s) {
    var events = s.events || [];
    var days = {};
    events.forEach(function (e) { days[dayNumber(e.at)] = true; });
    var today = dayNumber(Date.now());
    var start = days[today] ? today : (days[today - 1] ? today - 1 : null);
    var streak = 0;
    if (start !== null) { while (days[start - streak]) streak++; }
    var notes = events.reduce(function (n, e) { return n + (WEIGHT[e.kind] || 0); }, 0);
    var todayCount = events.filter(function (e) { return dayNumber(e.at) === today; }).length;
    return { streak: streak, notes: notes, today: todayCount };
  }

  function arrow(mid, angle, cls) {
    var p = document.createElementNS(NS, 'path');
    p.setAttribute('d', 'M -4 -4 L 4 0 L -4 4 Z');
    p.setAttribute('transform', 'translate(' + mid[0] + ' ' + mid[1] + ') rotate(' + angle + ')');
    p.setAttribute('class', 'th-arrow ' + cls);
    return p;
  }

  function paintMap(svg, st) {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var g = document.createElementNS(NS, 'g');
    svg.appendChild(g);
    MODULES.forEach(function (m, i) {
      var n = MODULES[i + 1];
      if (!n || !POS[m.id] || !POS[n.id]) return;
      var a = POS[m.id], b = POS[n.id];
      var doneA = m.units.every(function (u) { return st.units[key(m.id, u)]; });
      var toDone = n.units.every(function (u) { return st.units[key(n.id, u)]; });
      var fromAny = m.units.some(function (u) { return st.units[key(m.id, u)]; });
      var mIndex = MODULES.findIndex(function (x) { return x.id === m.id; });
      var nIndex = MODULES.findIndex(function (x) { return x.id === n.id; });
      var cIndex = MODULES.findIndex(function (x) { return x.id === st.current; });
      var cls = toDone || (fromAny && nIndex <= cIndex) ? 'route-done' : (mIndex === cIndex ? 'route-live' : 'route-ahead');
      var path = document.createElementNS(NS, 'path');
      path.setAttribute('d', 'M' + a[0] + ' ' + a[1] + ' L' + b[0] + ' ' + b[1]);
      path.setAttribute('class', 'route ' + cls);
      g.appendChild(path);
      var mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
      var angle = Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI;
      g.appendChild(arrow(mid, angle, cls.replace('route-', 'is-')));
    });
    MODULES.forEach(function (m) {
      if (!POS[m.id]) return;
      var p = POS[m.id];
      var done = st.completed.some(function (c) { return c.id === m.id; });
      var partial = st.partial.some(function (c) { return c.id === m.id; });
      var current = m.id === st.current && !done;
      var link = document.createElementNS(NS, 'a');
      link.setAttribute('href', base + '/module-' + m.id + '.html');
      link.setAttribute('aria-label', m.tag + ' ' + MAP_LABELS[m.id][zh ? 1 : 0] + ' — ' + (done ? (zh ? '已盖章' : 'stamped') : current ? (zh ? '你在这里' : 'you are here') : partial ? (zh ? '进行中' : 'in progress') : (zh ? '在前方' : 'ahead')));
      var group = document.createElementNS(NS, 'g');
      group.setAttribute('class', 'camp ' + (done ? 'is-done' : current ? 'is-current' : 'is-partial'));
      if (current) {
        var halo = document.createElementNS(NS, 'circle');
        halo.setAttribute('cx', p[0]); halo.setAttribute('cy', p[1]); halo.setAttribute('r', 30);
        halo.setAttribute('class', 'halo');
        group.appendChild(halo);
      }
      var circle = document.createElementNS(NS, 'circle');
      circle.setAttribute('cx', p[0]); circle.setAttribute('cy', p[1]); circle.setAttribute('r', 22);
      circle.setAttribute('class', 'camp-circle');
      group.appendChild(circle);
      var tag = document.createElementNS(NS, 'text');
      tag.setAttribute('x', p[0]); tag.setAttribute('y', p[1] + 4); tag.setAttribute('text-anchor', 'middle');
      tag.setAttribute('class', 'camp-tag');
      tag.textContent = done ? '✓' : m.tag.replace('M', '');
      group.appendChild(tag);
      link.appendChild(group);
      [['camp-label', m.tag, 44], ['camp-title', MAP_LABELS[m.id][zh ? 1 : 0], 58],
       ['camp-state', done ? (zh ? '已盖章' : 'stamped') : current ? (zh ? '你在这里' : 'you are here') : partial ? (zh ? '进行中' : 'in progress') : (zh ? '在前方' : 'ahead'), 72]
      ].forEach(function (row) {
        var t = document.createElementNS(NS, 'text');
        t.setAttribute('x', p[0]); t.setAttribute('y', p[1] + row[2]); t.setAttribute('text-anchor', 'middle');
        t.setAttribute('class', row[0]); t.textContent = row[1];
        link.appendChild(t);
      });
      g.appendChild(link);
    });
  }

  function paintList(list, st) {
    while (list.firstChild) list.removeChild(list.firstChild);
    MODULES.forEach(function (m) {
      var done = st.completed.some(function (c) { return c.id === m.id; });
      var partial = st.partial.some(function (c) { return c.id === m.id; });
      var current = m.id === st.current && !done;
      var li = document.createElement('li');
      li.className = done ? 'is-done' : current ? 'is-current' : partial ? 'is-partial' : 'is-ahead';
      var a = document.createElement('a');
      a.href = base + '/module-' + m.id + '.html';
      a.innerHTML = '<span class="m-dot">' + (done ? '✓' : m.tag.replace('M', '')) + '</span>' +
        '<span class="m-tag">' + m.tag + '</span><span class="m-title">' + MAP_LABELS[m.id][zh ? 1 : 0] + '</span>' +
        '<span class="m-state">' + (done ? (zh ? '已盖章' : 'stamped') : current ? (zh ? '你在这里' : 'you are here') : partial ? (zh ? '进行中' : 'in progress') : (zh ? '在前方' : 'ahead')) + '</span>';
      li.appendChild(a);
      list.appendChild(li);
    });
  }

  function paint() {
    var st = state();
    var tr = trail(st.s);
    var totalCamps = MODULES.length;
    var camps = st.completed.length;
    var currentModule = MODULES.filter(function (m) { return m.id === st.current; })[0] || MODULES[0];
    var title = (zh ? '第 ' + currentModule.number + ' 营地 — ' + MAP_LABELS[currentModule.id][1]
      : 'Camp ' + currentModule.number + ' — ' + MAP_LABELS[currentModule.id][0]);
    document.querySelectorAll('[data-th-heading]').forEach(function (el) { el.textContent = title; });
    document.querySelectorAll('[data-th-camp]').forEach(function (el) { el.textContent = zh ? '第 ' + currentModule.number + ' 营地' : 'Camp ' + currentModule.number; });
    document.querySelectorAll('[data-th-lede]').forEach(function (el) {
      if (!st.s.events || !st.s.events.length) {
        var firstParts = st.next ? st.next.unit.last - st.next.unit.first + 1 : 0;
        el.textContent = zh
          ? '从第 0 营地开始。第一段是 ' + (st.next ? st.next.unit.name : '导论') + '，共 ' + firstParts + ' 个部分。'
          : 'Start at Camp 0. The first leg is ' + (st.next ? st.next.unit.name : 'the introduction') + ', ' + firstParts + ' part' + (firstParts === 1 ? '' : 's') + '.';
      } else if (st.next) {
        var parts = st.next.unit.last - st.next.unit.first + 1;
        el.textContent = zh
          ? '你在这里。下一段是 ' + st.next.unit.name + '，共 ' + parts + ' 个部分。'
          : 'You are here. The next leg is ' + st.next.unit.name + ', ' + parts + ' part' + (parts === 1 ? '' : 's') + '.';
      } else {
        el.textContent = zh ? '十个营地都已盖章。你的证据日志就是路线。' : 'Every camp is stamped. Your evidence log is the route now.';
      }
    });
    document.querySelectorAll('[data-route-meta]').forEach(function (el) {
      el.textContent = zh ? camps + ' / ' + totalCamps + ' 个营地 · ' + st.doneUnits + ' / ' + st.totalUnits + ' 段'
        : camps + ' of ' + totalCamps + ' camps · ' + st.doneUnits + ' of ' + st.totalUnits + ' legs';
    });
    document.querySelectorAll('[data-th-camps]').forEach(function (el) { el.textContent = String(camps); });
    document.querySelectorAll('[data-trail-streak]').forEach(function (el) { el.textContent = String(tr.streak); });
    document.querySelectorAll('[data-trail-notes]').forEach(function (el) { el.textContent = String(tr.notes); });
    document.querySelectorAll('[data-today-count]').forEach(function (el) { el.textContent = String(tr.today); });
    document.querySelectorAll('[data-goal]').forEach(function (el) { el.textContent = String(goal()); });
    document.querySelectorAll('[data-today-bar]').forEach(function (el) {
      el.style.width = Math.min(100, tr.today / goal() * 100) + '%';
      var bar = el.closest('[role="progressbar"]');
      if (bar) { bar.setAttribute('aria-valuemax', String(goal())); bar.setAttribute('aria-valuenow', String(Math.min(tr.today, goal()))); }
    });
    document.querySelectorAll('[data-pace]').forEach(function (el) { el.value = String(goal()); });
    var note = NOTES[currentModule.id] || NOTES.m00;
    document.querySelectorAll('[data-field-quote]').forEach(function (el) { el.textContent = note.q; });
    document.querySelectorAll('[data-field-source]').forEach(function (el) { el.textContent = note.s; });
    document.querySelectorAll('[data-field-link]').forEach(function (el) { el.setAttribute('href', base + '/' + note.href); });
    document.querySelectorAll('[data-route-map]').forEach(function (svg) { paintMap(svg, st); });
    document.querySelectorAll('[data-route-list]').forEach(function (list) { paintList(list, st); });
  }

  function goal() {
    try { return Math.max(1, parseInt(localStorage.getItem('aps.trail.goal') || '3', 10) || 3); } catch (e) { return 3; }
  }

  document.querySelectorAll('[data-pace]').forEach(function (sel) {
    sel.addEventListener('change', function () {
      try { localStorage.setItem('aps.trail.goal', sel.value); } catch (e) { /* private mode */ }
      paint();
    });
  });
  document.addEventListener('aps:progress', paint);
  paint();
})();
