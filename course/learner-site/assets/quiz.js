/* Check — one question at a time, then a result that carries the next leg (#78, #112).
 *
 * Multiple choice: pick one, check it, and the cards say which is the correct answer and which was
 * yours — in words as well as colour — with the key's explanation and a Rewatch link to the segment
 * that teaches it. Short answer: write first, then reveal the model answer; never before an attempt,
 * because a model answer read first is recall, not application. Every answer is saved as it is given;
 * a reload resumes at the first unanswered question, and a finished check reopens on its result.
 * The score feeds progress; 75% is the certificate threshold.
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
  var currentEl = root.querySelector('[data-check-current]');
  var answeredEl = root.querySelector('[data-check-answered]');
  var bar = root.querySelector('[data-check-bar]');
  var progress = root.querySelector('[data-check-progress]');
  var resultStamp = root.querySelector('[data-result-stamp]');
  var current = -1;
  var zh = document.body.getAttribute('data-lang') === 'zh';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

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

  function qAt(i) { return questions[i] || null; }
  function nextButton(q) { return q ? q.querySelector('[data-next-question]') : null; }
  function answered(q) {
    var s = state[q.getAttribute('data-n')];
    return !!(s && s.answered);
  }

  function updateProgress() {
    var t = tally();
    var shown = current >= 0 ? current + 1 : total;
    if (currentEl) currentEl.textContent = current >= 0
      ? (zh ? '第 ' + shown + ' 题 / 共 ' + total + ' 题' : 'Question ' + shown + ' of ' + total)
      : (zh ? '结果' : 'Result');
    if (answeredEl) answeredEl.textContent = zh ? t.answered + ' 已答' : t.answered + ' answered';
    if (bar) bar.style.width = (current >= 0 ? shown / total * 100 : 100) + '%';
    if (progress) {
      progress.setAttribute('aria-valuenow', String(current >= 0 ? shown : total));
      progress.setAttribute('aria-valuemax', String(total));
    }
  }

  // Keep every question in the page for a no-JS reader, but show one at a time once JS is running.
  function show(i, focus) {
    var q = qAt(i);
    if (!q) return;
    current = i;
    questions.forEach(function (item, k) {
      item.hidden = k !== i;
      item.classList.toggle('is-current', k === i);
    });
    if (summary) summary.hidden = true;
    updateProgress();
    var btn = nextButton(q);
    if (btn) {
      btn.hidden = !answered(q);
      btn.innerHTML = (i === total - 1 ? (zh ? '查看结果' : 'See result') : (zh ? '下一题' : 'Next question')) +
        ' <span aria-hidden="true">→</span>';
    }
    if (focus) {
      q.scrollIntoView({ behavior: reduce.matches ? 'auto' : 'smooth', block: 'start' });
      var target = q.querySelector('input[type="radio"]:not(:disabled), textarea');
      if (target) target.focus({ preventScroll: true });
    }
  }

  function showResult() {
    var t = tally();
    if (t.answered < total) return;
    questions.forEach(function (q) { q.hidden = true; q.classList.remove('is-current'); });
    current = -1;
    updateProgress();
    if (summary) {
      summary.hidden = false;
      var mc = mcCount();
      var pct = mc ? Math.round(t.correct / mc * 100) : 0;
      summary.classList.toggle('is-passed', pct >= 75);
      summary.classList.toggle('is-failed', pct < 75);
      if (resultStamp) resultStamp.hidden = false;
      var heading = summary.querySelector('h2');
      if (heading) heading.focus({ preventScroll: true });
      summary.scrollIntoView({ behavior: reduce.matches ? 'auto' : 'smooth', block: 'start' });
    }
  }

  // The result at the end of the page: a count while questions are open, the score once all are in.
  function finish() {
    var t = tally();
    var mc = mcCount();
    var pct = mc ? Math.round(t.correct / mc * 100) : 0;
    var text = summary && summary.querySelector('[data-summary-text]');
    if (t.answered < total) {
      if (text) text.textContent = t.answered + ' of ' + total + ' answered · ' + t.correct + ' of ' + t.graded +
        ' multiple-choice correct so far.';
      if (summary) summary.querySelector('[data-revisit]').hidden = true;
      return false;
    }
    if (text) {
      text.textContent =
        t.correct + ' of ' + mc + ' multiple-choice correct (' + pct + '%). ' +
        (pct >= 75 ? 'That clears the 75% certificate threshold for this module.'
                   : 'The certificate threshold is 75% — revisit the objectives below and try again.');
    }
    var list = summary && summary.querySelector('[data-revisit-list]');
    if (list) {
      list.textContent = '';
      questions.forEach(function (q, i) {
        var s = state[q.getAttribute('data-n')];
        if (!s || s.correct !== false) return;
        var li = document.createElement('li');
        var href = q.getAttribute('data-rewatch');
        var label = 'Question ' + (i + 1) + ' — ' + (q.getAttribute('data-objective') || 'its objective');
        if (href) { var a = document.createElement('a'); a.href = href; a.textContent = label + ' · revisit'; li.append(a); }
        else li.textContent = label;
        list.append(li);
      });
      summary.querySelector('[data-revisit]').hidden = !list.children.length;
    }
    if (P) P.setQuiz(deck, t.correct, mc);
    return true;
  }

  function update() {
    var t = tally();
    if (scoreEl) scoreEl.textContent = t.correct + ' / ' + t.graded + ' multiple-choice correct · ' + t.answered + ' of ' + total + ' answered';
    finish();
    updateProgress();
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

    function revealNext() {
      var btn = nextButton(q);
      if (btn) {
        btn.hidden = false;
        btn.innerHTML = (index === total - 1 ? (zh ? '查看结果' : 'See result') : (zh ? '下一题' : 'Next question')) +
          ' <span aria-hidden="true">→</span>';
      }
    }

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
        revealNext();
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
        q.classList.add('is-revealed');
        revealNext();
      };
      reveal.addEventListener('click', function () {
        open();
        feedback.textContent = 'Model answer shown. Compare it with what you wrote.';
        save(n, { answered: true, correct: null, text: area.value });
      });
      q._restore = function (s) { area.value = s.text || ''; open(); feedback.textContent = 'Model answer shown.'; };
    }

    var next = nextButton(q);
    if (next) next.addEventListener('click', function () {
      if (index + 1 < total) show(index + 1, true);
      else { finish(); showResult(); }
    });
  });

  // Answers already given in this browser come back; resume at the first unanswered question.
  var saved = P && P.quizAnswers ? P.quizAnswers(deck) : {};
  questions.forEach(function (q) {
    var s = saved[q.getAttribute('data-n')];
    if (s && s.answered && q._restore) { state[q.getAttribute('data-n')] = s; q._restore(s); }
  });
  update();
  var firstOpen = questions.findIndex(function (q) { return !answered(q); });
  if (firstOpen < 0) { finish(); showResult(); }
  else show(firstOpen, false);

  var again = root.querySelector('[data-quiz-again]');
  if (again) again.addEventListener('click', function () {
    if (P && P.clearQuizAnswers) P.clearQuizAnswers(deck);
    location.reload();
  });
})();
