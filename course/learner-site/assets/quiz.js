/* Check — the module's knowledge check, one question at a time (#78).
 *
 * Multiple choice: pick a card, check it, and the cards say which is the correct answer and which
 * was yours — in words as well as colour — with the key's explanation and a Rewatch link to the
 * segment that teaches it. Short answer: write first, then reveal the model answer — never before an
 * attempt, because a model answer read first is recall, not application (the assessment standard's
 * own rule). Every answer is saved as it is given, so a check survives a reload. The score feeds
 * progress; 75% is the certificate threshold, so that is what "checked" means here.
 */
(function () {
  'use strict';
  var root = document.querySelector('[data-quiz]');
  if (!root) return;
  var deck = root.getAttribute('data-quiz');
  var P = window.APSProgress;
  var questions = Array.prototype.slice.call(root.querySelectorAll('.qq'));
  var total = questions.length;
  var state = {};   // n → { answered, correct: bool|null, chosen, text }
  var summary = root.querySelector('[data-quiz-summary]');
  var scoreEl = root.querySelector('[data-quiz-score]');
  var countEl = root.querySelector('[data-q-count]');
  var objectiveEl = root.querySelector('[data-q-objective]');
  var dots = Array.prototype.slice.call(root.querySelectorAll('.q-dots li'));
  var current = 0;

  function mcCount() { return questions.filter(function (q) { return q.classList.contains('is-mc'); }).length; }

  function tally() {
    var answered = 0, correct = 0, graded = 0;
    questions.forEach(function (q) {
      var s = state[q.getAttribute('data-n')];
      if (!s || !s.answered) return;
      answered++;
      if (s.correct !== null) { graded++; if (s.correct) correct++; }
    });
    return { answered: answered, correct: correct, graded: graded };
  }

  function paintDots() {
    dots.forEach(function (d, i) {
      var s = state[questions[i].getAttribute('data-n')];
      d.className = (i === current ? 'is-current ' : '') + (!s || !s.answered ? '' : s.correct === false ? 'is-wrong' : 'is-done');
    });
  }

  function show(i, focus) {
    current = Math.max(0, Math.min(total - 1, i));
    questions.forEach(function (q, n) { q.hidden = n !== current; });
    if (summary) summary.hidden = true;
    var q = questions[current];
    countEl.textContent = 'Question ' + (current + 1) + ' of ' + total;
    var objective = q.getAttribute('data-objective');
    objectiveEl.textContent = objective ? 'Objective: ' + objective : '';
    paintDots();
    if (focus) {
      var stem = q.querySelector('.q-stem');
      stem.setAttribute('tabindex', '-1');
      stem.focus({ preventScroll: true });
      var top = root.getBoundingClientRect().top + window.scrollY - 80;
      if (window.scrollY > top) window.scrollTo({ top: top });
    }
  }

  function finish() {
    var t = tally();
    var mc = mcCount();
    var pct = mc ? Math.round(t.correct / mc * 100) : 0;
    questions.forEach(function (q) { q.hidden = true; });
    countEl.textContent = 'Result';
    objectiveEl.textContent = '';
    summary.hidden = false;
    summary.querySelector('[data-summary-text]').textContent =
      t.correct + ' of ' + mc + ' multiple-choice correct (' + pct + '%). ' +
      (pct >= 75 ? 'That clears the 75% certificate threshold for this module.'
                 : 'The certificate threshold is 75% — revisit the objectives below and try again.');
    // The objectives behind the multiple-choice answers that missed, each with its Rewatch link.
    var list = summary.querySelector('[data-revisit-list]');
    list.textContent = '';
    questions.forEach(function (q, i) {
      var s = state[q.getAttribute('data-n')];
      if (!s || s.correct !== false) return;
      var li = document.createElement('li');
      var href = q.getAttribute('data-rewatch');
      var label = 'Question ' + (i + 1) + ' — ' + (q.getAttribute('data-objective') || 'its objective');
      if (href) { var a = document.createElement('a'); a.href = href; a.textContent = label + ' · rewatch'; li.append(a); }
      else li.textContent = label;
      list.append(li);
    });
    summary.querySelector('[data-revisit]').hidden = !list.children.length;
    if (P) P.setQuiz(deck, t.correct, mc);
    paintDots();
    var h = summary.querySelector('h2');
    if (h) h.focus({ preventScroll: true });
  }

  function update() {
    var t = tally();
    if (scoreEl) scoreEl.textContent = t.correct + ' / ' + t.graded + ' multiple-choice correct · ' + t.answered + ' of ' + total + ' answered';
    paintDots();
  }

  function save(n, record) {
    state[n] = record;
    if (P && P.setQuizAnswer) P.setQuizAnswer(deck, n, record);
    update();
  }

  questions.forEach(function (q, index) {
    var n = q.getAttribute('data-n');
    var key = q.getAttribute('data-answer');
    var explain = q.querySelector('.q-explain');
    var feedback = q.querySelector('[data-feedback]');
    var next = q.querySelector('[data-next]');
    var prev = q.querySelector('[data-prev]');
    next.addEventListener('click', function () { if (index === total - 1) finish(); else show(index + 1, true); });
    prev.addEventListener('click', function () { show(index - 1, true); });

    if (q.classList.contains('is-mc')) {
      var options = Array.prototype.slice.call(q.querySelectorAll('.q-option'));
      var check = q.querySelector('[data-check]');
      var chosen = null;
      q.addEventListener('change', function (e) {
        if (!e.target.matches('input[type="radio"]') || (state[n] && state[n].answered)) return;
        chosen = e.target.value;
        options.forEach(function (o) { o.classList.toggle('is-chosen', o.getAttribute('data-letter') === chosen); });
        check.disabled = false;
      });
      var settle = function (pick, announce) {
        var correct = pick === key;
        q.classList.add(correct ? 'is-correct' : 'is-wrong');
        options.forEach(function (o) {
          var l = o.getAttribute('data-letter');
          var input = o.querySelector('input');
          input.disabled = true;
          if (l === pick) input.checked = true;
          var mark = o.querySelector('[data-mark]');
          if (l === key) { o.classList.add('is-key'); mark.textContent = l === pick ? 'Correct answer · yours' : 'Correct answer'; }
          else if (l === pick) { o.classList.add('is-miss'); mark.textContent = 'Your answer'; }
        });
        check.disabled = true;
        check.hidden = true;
        explain.hidden = false;
        next.disabled = false;
        if (announce) feedback.textContent = correct ? 'Correct.' : 'Not quite — the keyed answer is ' + key.toUpperCase() + '.';
        else feedback.textContent = correct ? 'Answered: correct.' : 'Answered — the keyed answer is ' + key.toUpperCase() + '.';
      };
      check.addEventListener('click', function () {
        if (chosen === null) return;
        settle(chosen, true);
        save(n, { answered: true, correct: chosen === key, chosen: chosen });
      });
      q._restore = function (s) { settle(s.chosen, false); };
    } else {
      var area = q.querySelector('textarea');
      var reveal = q.querySelector('[data-reveal]');
      area.addEventListener('input', function () { reveal.disabled = area.value.trim().length < 20; });
      var open = function () {
        explain.hidden = false;
        reveal.disabled = true;
        reveal.hidden = true;
        area.readOnly = true;
        next.disabled = false;
        q.classList.add('is-revealed');
      };
      reveal.addEventListener('click', function () {
        open();
        feedback.textContent = 'Model answer shown. Compare it with what you wrote.';
        save(n, { answered: true, correct: null, text: area.value });
      });
      q._restore = function (s) { area.value = s.text || ''; open(); feedback.textContent = 'Model answer shown.'; };
    }
  });

  // Answers already given in this browser come back, and the check resumes at the first open question.
  var saved = P && P.quizAnswers ? P.quizAnswers(deck) : {};
  var firstOpen = -1;
  questions.forEach(function (q, i) {
    var s = saved[q.getAttribute('data-n')];
    if (s && s.answered && q._restore) { state[q.getAttribute('data-n')] = s; q._restore(s); }
    else if (firstOpen < 0) firstOpen = i;
  });
  update();
  if (firstOpen < 0 && total) finish(); else show(Math.max(0, firstOpen), false);

  var again = root.querySelector('[data-quiz-again]');
  if (again) again.addEventListener('click', function () {
    if (P && P.clearQuizAnswers) P.clearQuizAnswers(deck);
    location.reload();
  });
})();
