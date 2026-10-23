(function () {
  if (typeof io !== "function") return;
  const socket = io({ transports: ["websocket", "polling"], reconnection: true, reconnectionAttempts: 20 });
  const status = document.getElementById("host-status");
  const controlStatus = document.getElementById("control-status");
  const prompt = document.getElementById("question-prompt");
  const tag = document.getElementById("question-tag");
  const number = document.getElementById("question-number");
  const choices = document.getElementById("host-choices");
  const explanation = document.getElementById("question-explanation");
  const cloud = document.getElementById("word-cloud");
  const revealButton = document.getElementById("reveal-button");
  const nextButton = document.getElementById("next-button");
  let current = null;

  socket.on("connect", () => { status.textContent = "Connected; authenticating host session…"; socket.emit("host_auth"); });
  socket.on("disconnect", () => { status.textContent = "Connection lost; reconnecting…"; });
  socket.on("host_error", (data) => { status.textContent = data.message || "Host control unavailable."; status.classList.add("error"); });
  socket.on("host_state", (data) => {
    status.textContent = "Host controls ready.";
    status.classList.remove("error");
    document.getElementById("participant-count").textContent = data.participant_count || 0;
    if (data.question) renderQuestion(data.question);
  });
  socket.on("participant_count", (data) => { document.getElementById("participant-count").textContent = data.count || 0; });
  socket.on("host_question_state", renderQuestion);
  socket.on("live_summary", renderSummary);
  socket.on("session_complete", (data) => {
    current = null;
    prompt.textContent = `All ${data.total} questions are complete.`;
    tag.textContent = "Finished";
    number.textContent = "";
    choices.replaceChildren();
    explanation.textContent = "Download the CSV before closing the server.";
    controlStatus.textContent = "Session finished.";
    cloud.replaceChildren();
  });

  revealButton.addEventListener("click", () => socket.emit("host_reveal"));
  nextButton.addEventListener("click", () => socket.emit("host_advance"));

  function renderQuestion(question) {
    current = question;
    const topicLabel = question.topic_name ? `${question.topic_name} · ` : "";
    tag.textContent = `${topicLabel}${question.chapter} · Day ${question.day} · ${question.type}`;
    number.textContent = `Question ${question.index} of ${question.total}`;
    prompt.textContent = question.prompt;
    choices.replaceChildren();
    cloud.replaceChildren();
    explanation.textContent = question.explanation ? `Key: ${question.correct || "open response"}. ${question.explanation}` : "Key is hidden until reveal.";
    if (question.type === "mcq") {
      question.choices.forEach((choice) => {
        const p = document.createElement("p");
        p.textContent = `${choice.key}. ${choice.text}${question.revealed && choice.key === question.correct ? " ✓" : ""}`;
        choices.appendChild(p);
      });
    }
    controlStatus.textContent = question.revealed ? "Question closed; advance when ready." : "Answers are open.";
    document.getElementById("answer-count").textContent = "0";
  }

  function renderSummary(summary) {
    document.getElementById("answer-count").textContent = summary.answered || 0;
    cloud.replaceChildren();
    if (summary.word_cloud) {
      Object.entries(summary.word_cloud).forEach(([word, count]) => {
        const item = document.createElement("span");
        item.textContent = `${word} (${count})`;
        item.style.fontSize = `${Math.min(2.2, 1 + Number(count) * 0.1)}rem`;
        cloud.appendChild(item);
      });
    }
    if (summary.counts && current) {
      const counts = summary.counts;
      controlStatus.textContent = Object.entries(counts).map(([key, value]) => `${key}: ${value}`).join(" · ");
    }
  }
})();
