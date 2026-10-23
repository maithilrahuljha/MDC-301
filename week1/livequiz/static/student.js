(function () {
  const root = document.querySelector("main[data-session-code]");
  if (!root || typeof io !== "function") return;
  const defaultCode = root.dataset.sessionCode;
  const joinForm = document.getElementById("join-form");
  const joinCard = document.getElementById("join-card");
  const joinStatus = document.getElementById("join-status");
  const questionArea = document.getElementById("question-area");
  const answerArea = document.getElementById("answer-area");
  const answerStatus = document.getElementById("answer-status");
  const nameInput = document.getElementById("display-name");
  const handleInput = document.getElementById("github-username");
  const codeInput = document.getElementById("session-code");
  const forgetButton = document.getElementById("forget-button");
  let currentQuestion = null;
  let participantId = localStorage.getItem("mdc301_week1_participant_id");
  if (!participantId) {
    participantId = (window.crypto && crypto.randomUUID)
      ? crypto.randomUUID()
      : `p-${Date.now()}-${Math.random().toString(36).slice(2, 12)}`;
    localStorage.setItem("mdc301_week1_participant_id", participantId);
  }

  nameInput.value = localStorage.getItem("mdc301_week1_display_name") || "";
  handleInput.value = localStorage.getItem("mdc301_week1_github_username") || "";
  codeInput.value = localStorage.getItem("mdc301_week1_session_code") || defaultCode;
  forgetButton.addEventListener("click", function () {
    if (!window.confirm("Clear the saved alias, optional GitHub username, session code, and reconnect ID from this browser?")) return;
    [
      "mdc301_week1_participant_id",
      "mdc301_week1_display_name",
      "mdc301_week1_github_username",
      "mdc301_week1_session_code",
    ].forEach((key) => localStorage.removeItem(key));
    window.location.reload();
  });

  const socket = io({ transports: ["websocket", "polling"], reconnection: true, reconnectionAttempts: 20 });

  function identity() {
    return {
      participant_id: participantId,
      display_name: localStorage.getItem("mdc301_week1_display_name") || "",
      github_username: localStorage.getItem("mdc301_week1_github_username") || "",
      session_code: localStorage.getItem("mdc301_week1_session_code") || defaultCode,
    };
  }

  function tryJoin() {
    const user = identity();
    if (!user.display_name) return;
    joinStatus.textContent = "Connecting to the session…";
    socket.emit("join_session", user);
  }

  joinForm.addEventListener("submit", function (event) {
    event.preventDefault();
    localStorage.setItem("mdc301_week1_display_name", nameInput.value.trim());
    localStorage.setItem("mdc301_week1_github_username", handleInput.value.trim().replace(/^@/, ""));
    localStorage.setItem("mdc301_week1_session_code", codeInput.value.trim().toUpperCase());
    tryJoin();
  });

  socket.on("connect", function () {
    const user = identity();
    if (user.display_name) tryJoin();
  });
  socket.on("disconnect", function () { joinStatus.textContent = "Connection lost; reconnecting…"; });
  socket.on("join_error", function (data) { joinStatus.textContent = data.message || "Could not join."; joinStatus.classList.add("error"); });
  socket.on("answer_error", function (data) { answerStatus.textContent = data.message || "Answer not accepted."; answerStatus.classList.add("error"); });
  socket.on("joined", function (data) {
    joinStatus.textContent = `Joined ${data.session_code} as ${data.display_name}.`;
    joinStatus.classList.remove("error");
    joinCard.hidden = true;
    questionArea.hidden = false;
  });
  socket.on("question_state", renderQuestion);
  socket.on("answer_ack", function (data) {
    answerStatus.textContent = data.already_submitted ? "Your previous answer is saved." : "Answer saved. Wait for the instructor to reveal or advance.";
    answerStatus.classList.remove("error");
    Array.from(answerArea.querySelectorAll("button,input")).forEach((node) => { node.disabled = true; });
  });
  socket.on("session_complete", function () {
    document.getElementById("question-prompt").textContent = "The live check has ended. Thank you.";
    answerArea.replaceChildren();
    answerStatus.textContent = "You may close this page.";
  });

  function renderQuestion(question) {
    currentQuestion = question;
    questionArea.hidden = false;
    const topicLabel = question.topic_name ? `${question.topic_name} · ` : "";
    document.getElementById("question-tag").textContent = `${topicLabel}${question.chapter} · Day ${question.day} · ${question.type}`;
    document.getElementById("question-number").textContent = `Question ${question.index} of ${question.total}`;
    document.getElementById("question-prompt").textContent = question.prompt;
    answerArea.replaceChildren();
    answerStatus.textContent = question.revealed
      ? `Question closed. Correct answer: ${question.correct || "open response"}. ${question.explanation || ""}`
      : "Choose or enter one response, then submit.";
    answerStatus.classList.remove("error");

    if (question.type === "mcq") {
      question.choices.forEach((choice) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "choice";
        button.textContent = `${choice.key}. ${choice.text}`;
        button.addEventListener("click", () => submit(choice.key));
        answerArea.appendChild(button);
      });
    } else if (question.type === "word_cloud") {
      const label = document.createElement("label");
      label.htmlFor = "word-answer";
      label.textContent = `Enter ${question.max_words || 1} word (max ${question.max_length || 35} characters)`;
      const input = document.createElement("input");
      input.id = "word-answer";
      input.maxLength = question.max_length || 35;
      input.autocomplete = "off";
      input.placeholder = "machine, pattern, learning…";
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = "Submit word";
      button.addEventListener("click", () => submit(input.value.trim()));
      answerArea.append(label, input, button);
      input.addEventListener("keydown", (event) => { if (event.key === "Enter") { event.preventDefault(); submit(input.value.trim()); } });
    }
  }

  function submit(answer) {
    if (!currentQuestion || currentQuestion.revealed) return;
    if (currentQuestion.type === "word_cloud") {
      const words = String(answer).trim().split(/\s+/).filter(Boolean);
      if (!words.length || words.length > (currentQuestion.max_words || 1)) {
        answerStatus.textContent = "Please submit one word only.";
        answerStatus.classList.add("error");
        return;
      }
    }
    answerStatus.textContent = "Sending…";
    socket.emit("submit_answer", {
      participant_id: participantId,
      question_id: currentQuestion.id,
      answer: answer,
    });
  }
})();
