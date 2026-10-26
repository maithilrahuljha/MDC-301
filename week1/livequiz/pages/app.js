(() => {
  "use strict";

  const QUIZZES = [
    {
      slug: "quiz1",
      name: "Quiz 1 · Before Lab 1 — Hour 1 Quick Checks",
      file: "before_lab1_questions.json",
      phase: "BEFORE LAB 1 — HOUR 1",
      slides: "5, 6, 9–12, 16–17",
      ids: Array.from({ length: 8 }, (_, index) => `Q${index + 1}`)
    },
    {
      slug: "quiz2",
      name: "Quiz 2 · Between Lab 1 and Lab 2 — Hour 2 Quick Checks",
      file: "between_lab1_and_lab2_questions.json",
      phase: "BETWEEN LAB 1 AND LAB 2 — HOUR 2",
      slides: "21, 23, 25–30, 33–37",
      ids: Array.from({ length: 12 }, (_, index) => `Q${index + 9}`)
    }
  ];
  const $ = (id) => document.getElementById(id);
  const ui = {
    setupPanel: $("setup-panel"), quizPanel: $("quiz-panel"), completionPanel: $("completion-panel"),
    mode: $("mode-select"), topic: $("topic-select"), sourceNote: $("topic-source-note"),
    sessionField: $("session-field"), aliasField: $("alias-field"), session: $("session-code"), alias: $("display-name"),
    collectionNote: $("collection-note"), start: $("start-button"), setupError: $("setup-error"),
    modeLabel: $("quiz-mode-label"), topicTitle: $("quiz-topic-title"), counter: $("question-counter"),
    progress: $("progress-bar"), chapter: $("chapter-label"), type: $("type-label"), prompt: $("question-prompt"),
    options: $("answer-options"), wordWrap: $("word-answer-wrap"), word: $("word-answer"), message: $("answer-message"),
    feedback: $("practice-feedback"), submit: $("submit-button"), retry: $("retry-upload-button"),
    reveal: $("reveal-button"), next: $("next-button"), exit: $("exit-button"), footnote: $("quiz-footnote"),
    completionTitle: $("completion-title"), summary: $("completion-summary"), again: $("again-button"), change: $("change-topic-button")
  };
  const state = {
    mode: "lecture", quiz: null, index: 0, selected: null, submitted: false,
    revealed: false, correct: 0, scored: 0, pending: false, response: null,
    session: "", alias: ""
  };

  function supabaseSettings() {
    const raw = window.MDC301_SUPABASE || {};
    const url = typeof raw.url === "string" ? raw.url.trim() : "";
    const key = typeof raw.anonKey === "string" ? raw.anonKey.trim() : "";
    if (!url || !key) return null;
    try {
      const parsed = new URL(url);
      if (parsed.protocol !== "https:" || !parsed.host || parsed.username || parsed.password || parsed.pathname !== "/" || parsed.search || parsed.hash) return null;
      return { url: parsed.origin, key };
    } catch (_error) { return null; }
  }
  function attemptedSupabaseSetup() {
    const raw = window.MDC301_SUPABASE || {};
    return Boolean((typeof raw.url === "string" && raw.url.trim()) || (typeof raw.anonKey === "string" && raw.anonKey.trim()));
  }
  function text(element, value) { element.textContent = value; }
  function currentQuestion() { return state.quiz.questions[state.index]; }
  function selectedQuiz() { return QUIZZES.find((quiz) => quiz.slug === ui.topic.value) || QUIZZES[0]; }

  function updateSetup() {
    const quiz = selectedQuiz();
    text(ui.sourceNote, `${quiz.phase} · lecture slides ${quiz.slides}`);
    const lecture = ui.mode.value === "lecture";
    ui.sessionField.hidden = !lecture;
    ui.aliasField.hidden = !lecture;
    if (!lecture) text(ui.collectionNote, "Practice answers are never uploaded. Try either Week 1 quiz as often as you like.");
    else if (supabaseSettings()) text(ui.collectionNote, "Lecture responses go to the configured Supabase table. Enter the instructor's session label; alias is optional.");
    else if (attemptedSupabaseSetup()) text(ui.collectionNote, "Supabase settings look incomplete or invalid. Lecture answers will not be collected; check config.js or clear both settings.");
    else text(ui.collectionNote, "Response collection is off. The quiz works without it; lecture answers are not saved or uploaded.");
  }
  function setupError(message) { text(ui.setupError, message); ui.setupError.hidden = !message; }

  function makeOption(label, index) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "option-button";
    button.dataset.optionIndex = String(index);
    button.setAttribute("aria-pressed", "false");
    const key = document.createElement("span"); key.className = "option-key"; key.textContent = String.fromCharCode(65 + index);
    const answer = document.createElement("span"); answer.textContent = label;
    button.append(key, answer);
    button.addEventListener("click", () => {
      if (state.submitted) return;
      state.selected = index;
      for (const other of ui.options.querySelectorAll(".option-button")) {
        const isSelected = other === button;
        other.classList.toggle("selected", isSelected);
        other.setAttribute("aria-pressed", String(isSelected));
      }
      ui.message.className = "answer-message";
      text(ui.message, "");
    });
    return button;
  }

  function renderQuestion() {
    const question = currentQuestion();
    const cloud = question.type === "word_cloud";
    state.selected = null; state.submitted = false; state.revealed = false; state.pending = false; state.response = null;
    text(ui.topicTitle, state.quiz.topic_name);
    text(ui.modeLabel, state.mode === "lecture" ? "LECTURE MODE · FOLLOW YOUR INSTRUCTOR" : "PRACTICE MODE · YOUR OWN PACE");
    text(ui.counter, `Question ${state.index + 1} of ${state.quiz.questions.length}`);
    ui.progress.style.width = `${((state.index + 1) / state.quiz.questions.length) * 100}%`;
    text(ui.chapter, `${question.phase} · Slide ${question.slide}`);
    text(ui.type, cloud ? "One-word response" : question.type === "true_false" ? "True or false" : "Multiple choice");
    text(ui.prompt, question.question);
    text(ui.message, ""); ui.message.className = "answer-message";
    text(ui.feedback, ""); ui.feedback.hidden = true; ui.feedback.className = "feedback";
    ui.options.replaceChildren(); ui.options.hidden = cloud; ui.wordWrap.hidden = !cloud;
    ui.word.value = ""; ui.word.disabled = false; ui.word.maxLength = Number(question.max_length || 35);
    ui.submit.hidden = false; ui.submit.disabled = false; ui.retry.hidden = true; ui.reveal.hidden = true; ui.next.hidden = true;
    if (!cloud) for (const [index, option] of question.options.entries()) ui.options.append(makeOption(option, index));
    if (state.mode === "lecture") {
      text(ui.footnote, "Answer when prompted. Wait for your instructor's cue to reveal feedback and move on; devices do not sync and there is no live results screen.");
      ui.reveal.textContent = cloud ? "Continue after instructor cue" : "Reveal after instructor cue";
    } else text(ui.footnote, "Submit to see the answer and explanation. Practice runs in this browser; answers are not uploaded.");
    ui.prompt.focus({ preventScroll: true });
  }

  async function fetchQuiz(quizDefinition) {
    const response = await fetch(`../${encodeURIComponent(quizDefinition.file)}`, { cache: "no-cache" });
    if (!response.ok) throw new Error(`Could not load ${quizDefinition.name} (HTTP ${response.status}).`);
    const payload = await response.json();
    if (!payload || payload.quiz_id !== quizDefinition.slug || !Array.isArray(payload.questions)) {
      throw new Error("This Week 1 quiz file is incomplete or does not match the selected quiz.");
    }
    const expectedCount = quizDefinition.ids.length;
    if (payload.questions.length !== expectedCount) throw new Error(`${quizDefinition.name} should contain ${expectedCount} questions.`);
    const questions = payload.questions.map((item, index) => {
      const expectedId = quizDefinition.ids[index];
      const keys = item && item.options && typeof item.options === "object" ? Object.keys(item.options) : [];
      const answerIndex = keys.indexOf(item.correct_option);
      if (!item || item.id !== expectedId || item.type !== "multiple_choice" ||
          typeof item.question !== "string" || !item.question.trim() ||
          keys.join(",") !== "A,B,C,D" || keys.some((key) => typeof item.options[key] !== "string") ||
          answerIndex < 0 || typeof item.explanation !== "string") {
        throw new Error(`Question ${expectedId} in ${quizDefinition.file} is invalid.`);
      }
      return {
        id: item.id,
        type: "multiple_choice",
        question: item.question,
        options: keys.map((key) => item.options[key]),
        correct: answerIndex,
        explanation: item.explanation,
        phase: item.phase,
        slide: item.slide
      };
    });
    return {
      topic_slug: quizDefinition.slug,
      topic_name: payload.title,
      chapter: "Week 1",
      source_chapters: [quizDefinition.phase],
      phase: payload.phase,
      instructions: payload.instructions,
      questions
    };
  }

  async function loadQuiz(slug) {
    const requestedQuestion = new URLSearchParams(window.location.search).get("question_id");
    if (requestedQuestion) {
      const preferred = QUIZZES.find((quiz) => quiz.slug === slug && quiz.ids.includes(requestedQuestion));
      const candidates = preferred ? [preferred, ...QUIZZES.filter((quiz) => quiz !== preferred)] : QUIZZES;
      for (const quizDefinition of candidates) {
        if (!quizDefinition.ids.includes(requestedQuestion)) continue;
        const quiz = await fetchQuiz(quizDefinition);
        const item = quiz.questions.find((question) => question.id === requestedQuestion);
        if (item) {
          return {
            ...quiz,
            topic_name: `${quiz.topic_name} · linked check`,
            questions: [item]
          };
        }
      }
      throw new Error(`Question ${requestedQuestion} is not in either Week 1 quiz.`);
    }
    const quizDefinition = QUIZZES.find((quiz) => quiz.slug === slug) || QUIZZES[0];
    return fetchQuiz(quizDefinition);
  }

  async function startQuiz() {
    setupError("");
    const settings = supabaseSettings();
    const mode = ui.mode.value;
    const session = ui.session.value.trim();
    const alias = ui.alias.value.trim();
    if (mode === "lecture" && settings && !session) { setupError("Enter the session label announced by your instructor so responses can be grouped."); ui.session.focus(); return; }
    if (session.length > 40 || alias.length > 32) { setupError("The session label must be 40 characters or fewer and the optional alias 32 characters or fewer."); return; }
    if (settings && mode === "lecture" && !/^[A-Za-z0-9 _.-]{1,40}$/.test(session)) { setupError("Use only letters, numbers, spaces, hyphens, underscores, and periods in the session label."); ui.session.focus(); return; }
    if (/[\u0000-\u001f\u007f]/.test(alias)) { setupError("The optional alias cannot contain control characters."); ui.alias.focus(); return; }
    ui.start.disabled = true; ui.start.textContent = "Loading quiz…";
    try {
      const quiz = await loadQuiz(ui.topic.value);
      state.mode = mode; state.quiz = quiz; state.index = 0; state.correct = 0; state.scored = 0; state.session = session; state.alias = alias;
      ui.setupPanel.hidden = true; ui.completionPanel.hidden = true; ui.quizPanel.hidden = false;
      renderQuestion(); ui.quizPanel.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
      setupError(`${error.message} Check that the Pages site includes both Week 1 quiz files, then try again.`);
    } finally { ui.start.disabled = false; ui.start.innerHTML = 'Start quiz <span aria-hidden="true">→</span>'; }
  }

  function getAnswer(question) {
    if (question.type === "word_cloud") {
      const answer = ui.word.value.trim();
      if (!answer) { ui.message.className = "answer-message error"; text(ui.message, "Type one word before submitting."); ui.word.focus(); return null; }
      const max = Number(question.max_length || 35);
      if (/\s/u.test(answer) || Array.from(answer).length > max) { ui.message.className = "answer-message error"; text(ui.message, `Enter one word, up to ${max} characters.`); ui.word.focus(); return null; }
      return { answerText: answer, answerIndex: null, isCorrect: null };
    }
    if (state.selected === null) { ui.message.className = "answer-message error"; text(ui.message, "Choose an answer before submitting."); return null; }
    return { answerText: question.options[state.selected], answerIndex: state.selected, isCorrect: state.selected === question.correct };
  }
  function responseRow(question, answer) {
    return {
      session_code: state.session, topic_slug: state.quiz.topic_slug, question_id: question.id,
      question_type: question.type, answer_text: answer.answerText, answer_index: answer.answerIndex,
      is_correct: answer.isCorrect, display_name: state.alias || null
    };
  }
  async function uploadResponse() {
    const settings = supabaseSettings();
    if (!settings || !state.response) return;
    state.pending = true; ui.retry.hidden = true; ui.submit.disabled = true;
    text(ui.message, "Sending your lecture response…");
    try {
      const result = await fetch(`${settings.url}/rest/v1/week1_quiz_responses`, {
        method: "POST",
        headers: { apikey: settings.key, "Content-Type": "application/json", Prefer: "return=minimal" },
        body: JSON.stringify(state.response)
      });
      if (!result.ok) throw new Error("Supabase insert failed");
      text(ui.message, "Lecture response saved. Wait for your instructor's cue.");
    } catch (_error) {
      ui.message.className = "answer-message error";
      text(ui.message, "Could not save the lecture response. Check your connection or tell the instructor; the quiz can continue.");
      ui.retry.hidden = false;
    } finally {
      state.pending = false; ui.submit.disabled = false; ui.reveal.hidden = false;
      ui.reveal.textContent = currentQuestion().type === "word_cloud" ? "Continue after instructor cue" : "Reveal after instructor cue";
      ui.reveal.focus();
    }
  }
  async function submitAnswer() {
    if (state.submitted || state.pending) return;
    const question = currentQuestion();
    const answer = getAnswer(question);
    if (!answer) return;
    state.submitted = true; state.response = responseRow(question, answer);
    ui.submit.hidden = true; ui.word.disabled = true;
    for (const button of ui.options.querySelectorAll(".option-button")) button.disabled = true;
    if (question.type !== "word_cloud") { state.scored += 1; if (answer.isCorrect) state.correct += 1; }
    if (state.mode === "practice") {
      revealFeedback(); showNextButton(); return;
    }
    if (supabaseSettings()) await uploadResponse();
    else { text(ui.message, "Response collection is off; this answer was not saved. Wait for your instructor's cue."); ui.reveal.hidden = false; ui.reveal.focus(); }
  }
  function revealFeedback() {
    const question = currentQuestion();
    ui.feedback.hidden = false;
    if (question.type === "word_cloud") {
      ui.feedback.className = "feedback good";
      text(ui.feedback, question.explanation || "There is no single correct word. Compare your response with the class discussion.");
      state.revealed = true; return;
    }
    const correct = state.selected === question.correct;
    for (const button of ui.options.querySelectorAll(".option-button")) {
      const index = Number(button.dataset.optionIndex);
      if (index === question.correct) button.classList.add("correct");
      else if (index === state.selected) button.classList.add("incorrect");
    }
    ui.feedback.className = `feedback ${correct ? "good" : "bad"}`;
    text(ui.feedback, `${correct ? "Correct." : `Not quite. The answer is: ${question.options[question.correct]}.`}${question.explanation ? ` ${question.explanation}` : ""}`);
    ui.message.className = `answer-message ${correct ? "success" : "error"}`;
    text(ui.message, correct ? "Your answer is correct." : "Review the answer and explanation below.");
    state.revealed = true;
  }
  async function retryUpload() { if (state.response && !state.pending) await uploadResponse(); }
  function showNextButton() {
    ui.next.hidden = false;
    ui.next.textContent = state.index + 1 === state.quiz.questions.length ? "See results" : "Next question →";
    ui.next.focus();
  }
  function revealOrContinue() {
    if (state.pending) return;
    if (!state.revealed) revealFeedback();
    ui.reveal.hidden = true; showNextButton();
  }
  function completeQuiz() {
    ui.quizPanel.hidden = true; ui.completionPanel.hidden = false;
    if (state.mode === "practice") {
      ui.again.textContent = "Try this quiz again"; text(ui.completionTitle, "Nice work.");
      const note = state.quiz.questions.some((question) => question.type === "word_cloud") ? " Word-cloud responses are not scored." : "";
      text(ui.summary, `${state.quiz.topic_name}: ${state.correct} of ${state.scored} scored questions correct.${note} Retake this quiz or choose the other one.`);
    } else {
      ui.again.textContent = "Practise this quiz now"; text(ui.completionTitle, "Quiz complete.");
      text(ui.summary, `${state.quiz.topic_name} is finished. Start practice mode to retry on your own. Lecture responses ${supabaseSettings() ? "were sent when the connection worked" : "were not collected"}.`);
    }
    ui.completionPanel.scrollIntoView({ behavior: "smooth", block: "center" }); ui.again.focus();
  }
  function nextQuestion() {
    if (state.index + 1 === state.quiz.questions.length) { completeQuiz(); return; }
    state.index += 1; renderQuestion(); ui.quizPanel.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  function exitQuiz() {
    ui.quizPanel.hidden = true; ui.completionPanel.hidden = true; ui.setupPanel.hidden = false;
    ui.setupPanel.scrollIntoView({ behavior: "smooth", block: "start" }); ui.topic.focus();
  }
  function again() {
    if (state.mode === "lecture") ui.mode.value = "practice";
    updateSetup(); ui.completionPanel.hidden = true; ui.setupPanel.hidden = false; ui.start.focus(); startQuiz();
  }

  for (const quiz of QUIZZES) {
    const option = document.createElement("option"); option.value = quiz.slug; option.textContent = quiz.name; ui.topic.append(option);
  }
  ui.topic.value = QUIZZES[0].slug;
  const linkedQuiz = new URLSearchParams(window.location.search).get("quiz") || new URLSearchParams(window.location.search).get("topic");
  if (QUIZZES.some((quiz) => quiz.slug === linkedQuiz)) ui.topic.value = linkedQuiz;
  ui.mode.addEventListener("change", updateSetup); ui.topic.addEventListener("change", updateSetup);
  ui.start.addEventListener("click", startQuiz); ui.submit.addEventListener("click", submitAnswer);
  ui.retry.addEventListener("click", retryUpload); ui.reveal.addEventListener("click", revealOrContinue);
  ui.next.addEventListener("click", nextQuestion); ui.exit.addEventListener("click", exitQuiz);
  ui.again.addEventListener("click", again); ui.change.addEventListener("click", exitQuiz);
  ui.word.addEventListener("keydown", (event) => { if (event.key === "Enter" && !ui.submit.hidden) submitAnswer(); });
  updateSetup();
})();
