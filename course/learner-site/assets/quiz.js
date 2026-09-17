/* Knowledge check — the module quiz, playable.
 *
 * Multiple choice: pick, check, see the rationale and the objective it maps to. Short answer: write
 * first, then reveal the model answer — never before an attempt, because a model answer read first
 * is recall, not application (the assessment standard's own rule). The score feeds progress;
 * 75% is the certificate threshold, so that is what "checked" means here.
 */
(function () {
  'use strict';
  var root = document.querySelector('[data-quiz]');
  if (!root) return;
  var deck = root.getAttribute('data-quiz');
  var questions = Array.prototype.slice.call(root.querySelectorAll('.qq'));
  var total = questions.length;
  var state = {};   // n → { answered: bool, correct: bool|null }
  var summary = document.querySelector('[data-quiz-summary]');
  var scoreEl = document.querySelector('[data-quiz-score]');

  function announce(el, text) {
    var live = el.querySelector('[data-feedback]');
    if (live) { live.textContent = text; }
  }

  function update() {
    var answered = 0, correct = 0, graded = 0;
    questions.forEach(function (q) {
      var s = state[q.getAttribute('data-n')];
      if (!s || !s.answered) return;
      answered++;
      if (s.correct !== null) { graded++; if (s.correct) correct++; }
    });
    if (scoreEl) scoreEl.textContent = correct + ' / ' + graded + ' multiple-choice correct · ' + answered + ' of ' + total + ' answered';
    if (answered === total && summary) {
      var mc = questions.filter(function (q) { return q.classList.contains('is-mc'); }).length;
      var pct = mc ? Math.round(correct / mc * 100) : 0;
      summary.hidden = false;
      summary.querySelector('[data-summary-text]').textContent =
        correct + ' of ' + mc + ' multiple-choice correct (' + pct + '%). ' +
        (pct >= 75 ? 'That clears the 75% certificate threshold for this module.' : 'The certificate threshold is a 75% average — reread the objectives named next to the questions you missed and try again.');
      if (window.APSProgress) window.APSProgress.setQuiz(deck, correct, mc);
    }
  }

  questions.forEach(function (q) {
    var n = q.getAttribute('data-n');
    var key = q.getAttribute('data-answer');
    var explain = q.querySelector('.q-explain');
    if (q.classList.contains('is-mc')) {
      var options = Array.prototype.slice.call(q.querySelectorAll('.q-option'));
      var check = q.querySelector('[data-check]');
      var chosen = null;
      options.forEach(function (o) {
        o.addEventListener('click', function () {
          if (state[n] && state[n].answered) return;
          chosen = o.getAttribute('data-letter');
          options.forEach(function (x) { x.setAttribute('aria-checked', String(x === o)); x.classList.toggle('is-chosen', x === o); });
          check.disabled = false;
        });
      });
      check.addEventListener('click', function () {
        if (chosen === null) return;
        var correct = chosen === key;
        state[n] = { answered: true, correct: correct };
        q.classList.add(correct ? 'is-correct' : 'is-wrong');
        options.forEach(function (x) {
          var l = x.getAttribute('data-letter');
          x.disabled = true;
          if (l === key) x.classList.add('is-key');
          if (l === chosen && !correct) x.classList.add('is-miss');
        });
        check.disabled = true;
        explain.hidden = false;
        announce(q, correct ? 'Correct.' : 'Not quite — the keyed answer is ' + key.toUpperCase() + '.');
        update();
      });
    } else {
      var area = q.querySelector('textarea');
      var reveal = q.querySelector('[data-reveal]');
      area.addEventListener('input', function () { reveal.disabled = area.value.trim().length < 20; });
      reveal.addEventListener('click', function () {
        state[n] = { answered: true, correct: null };
        explain.hidden = false;
        reveal.disabled = true;
        area.readOnly = true;
        q.classList.add('is-revealed');
        announce(q, 'Model answer shown. Compare it with what you wrote.');
        update();
      });
    }
  });

  var again = document.querySelector('[data-quiz-again]');
  if (again) again.addEventListener('click', function () { location.reload(); });
  update();
})();
