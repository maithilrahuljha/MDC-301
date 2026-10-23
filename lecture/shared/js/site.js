(() => {
  "use strict";
  const STORAGE_KEY = "mdc301.lecture.badges.v1";
  const lineFor = (badgeId, label) => `- [x] ${badgeId} — ${label}`;

  function readBadges() {
    try {
      const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
      return value && typeof value === "object" ? value : {};
    } catch (_error) {
      return {};
    }
  }

  function writeBadges(value) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(value));
      return true;
    } catch (_error) {
      return false;
    }
  }

  function openedChecks() {
    try {
      const value = JSON.parse(localStorage.getItem("mdc301.selfcheck.opened.v1") || "{}");
      return { available: true, value: value && typeof value === "object" ? value : {} };
    } catch (_error) {
      return { available: false, value: {} };
    }
  }

  for (const button of document.querySelectorAll("[data-unlock-badge]")) {
    const badgeId = button.dataset.unlockBadge;
    const label = button.dataset.badgeLabel || badgeId;
    const wrapper = button.closest("[data-badge-card]") || button.parentElement;
    const consent = wrapper?.querySelector("[data-badge-consent]");
    const message = wrapper?.querySelector("[data-badge-result]");
    const line = wrapper?.querySelector("[data-badge-copy-line]");
    const copy = wrapper?.querySelector("[data-copy-badge-line]");
    const existing = readBadges();

    if (existing[badgeId]) {
      if (message) message.textContent = `Badge already unlocked on ${existing[badgeId].date || "this browser"}.`;
      if (line) line.textContent = lineFor(badgeId, label);
      if (line) line.hidden = false;
      if (copy) copy.hidden = false;
    }

    button.addEventListener("click", () => {
      if (consent && !consent.checked) {
        if (message) message.textContent = "Complete all three linked checks, then tick the confirmation box.";
        consent.focus();
        return;
      }
      const sessionPanel = button.closest("[data-session-badge]");
      const requiredIds = sessionPanel ? [...sessionPanel.querySelectorAll("[data-quiz-id]")].filter((link) => link.dataset.quizUnavailable === "false").map((link) => link.dataset.quizId) : [];
      const checkState = openedChecks();
      if (checkState.available && requiredIds.length) {
        const opened = new Set(Array.isArray(checkState.value[badgeId]) ? checkState.value[badgeId] : []);
        const remaining = requiredIds.filter((id) => !opened.has(id));
        if (remaining.length) {
          if (message) message.textContent = `Open each available existing poll link once, then return. Still to open: ${remaining.join(", ")}.`;
          return;
        }
      }
      const badges = readBadges();
      badges[badgeId] = { date: new Date().toISOString().slice(0, 10) };
      const saved = writeBadges(badges);
      if (message) {
        message.textContent = saved
          ? `Unlocked: ${label}. This is saved in this browser only; add the line below to progress.md in your repository.`
          : `Completed: ${label}. Browser storage is unavailable; copy the line below into progress.md.`;
      }
      if (line) {
        line.textContent = lineFor(badgeId, label);
        line.hidden = false;
      }
      if (copy) copy.hidden = false;
    });

    copy?.addEventListener("click", async () => {
      if (!line) return;
      const value = line.textContent || lineFor(badgeId, label);
      try {
        await navigator.clipboard.writeText(value);
        if (message) message.textContent = "Badge line copied. Paste it into progress.md and commit the file.";
      } catch (_error) {
        if (message) message.textContent = "Select and copy the badge line, then paste it into progress.md.";
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(line);
        selection?.removeAllRanges();
        selection?.addRange(range);
      }
    });
  }

  for (const link of document.querySelectorAll("a[data-optional-file]")) {
    const label = link.dataset.missingLabel || "Optional file not included in this copy";
    fetch(link.href, { method: "HEAD", cache: "no-cache" }).then((response) => {
      if (!response.ok) {
        link.href = "#optional-file-unavailable";
        link.textContent = label;
        link.setAttribute("aria-disabled", "true");
        link.addEventListener("click", (event) => event.preventDefault());
      }
    }).catch(() => { /* A blocked HEAD request is not proof the file is missing. Keep the normal link. */ });
  }

  for (const reveal of document.querySelectorAll("[data-reveal-answer]")) {
    const target = document.getElementById(reveal.dataset.revealAnswer);
    reveal.addEventListener("click", () => {
      if (!target) return;
      const willShow = target.hidden;
      target.hidden = !willShow;
      reveal.setAttribute("aria-expanded", String(willShow));
      reveal.textContent = willShow ? "Hide explanation" : "Reveal explanation";
    });
  }
})();
