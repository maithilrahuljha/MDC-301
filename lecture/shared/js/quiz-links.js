(() => {
  "use strict";
  const links = [...document.querySelectorAll("[data-quiz-id]")];
  if (!links.length) return;

  function unavailable(link, reason) {
    link.href = "#quiz-coming-soon";
    link.textContent = "Quiz coming soon";
    link.setAttribute("aria-disabled", "true");
    link.dataset.quizUnavailable = "true";
    link.addEventListener("click", (event) => event.preventDefault());
    const status = link.closest("li")?.querySelector("[data-quiz-status]");
    if (status) status.textContent = reason || "Quiz coming soon.";
  }

  function hasId(value, wanted) {
    if (Array.isArray(value)) return value.some((item) => hasId(item, wanted));
    if (!value || typeof value !== "object") return false;
    if (Object.prototype.hasOwnProperty.call(value, "id") && value.id === wanted) return true;
    return Object.values(value).some((item) => hasId(item, wanted));
  }

  async function initialize() {
    let config;
    try {
      const configUrl = new URL("quiz-links.json", document.baseURI);
      const configResponse = await fetch(configUrl, { cache: "no-cache" });
      if (!configResponse.ok) throw new Error("The lecture copy has no quiz link map.");
      config = await configResponse.json();
    } catch (_error) {
      links.forEach((link) => unavailable(link, "Quiz bank is not included with this lecture copy."));
      return;
    }

    const sourcePaths = Array.isArray(config.sources)
      ? config.sources
      : (config.source ? [config.source] : []);
    const banks = [];
    for (const source of sourcePaths) {
      try {
        const bankUrl = new URL(source, document.baseURI);
        const bankResponse = await fetch(bankUrl, { cache: "no-cache" });
        if (bankResponse.ok) banks.push(await bankResponse.json());
      } catch (_error) { /* A missing phase bank leaves only its own links unavailable. */ }
    }
    if (!banks.length) {
      links.forEach((link) => unavailable(link, "Quiz coming soon. The linked quiz banks are not available here."));
      return;
    }

    let pollAvailable = false;
    try {
      const pollUrl = new URL(config.poll, document.baseURI);
      const pollResponse = await fetch(pollUrl, { method: "HEAD", cache: "no-cache" });
      pollAvailable = pollResponse.ok;
    } catch (_error) {
      pollAvailable = false;
    }
    if (!pollAvailable) {
      links.forEach((link) => unavailable(link, "Quiz coming soon. The poll page is not available in this copy."));
      return;
    }

    for (const link of links) {
      const id = link.dataset.quizId || "";
      if (!Array.isArray(config.ids) || !config.ids.includes(id) || !banks.some((bank) => hasId(bank, id))) {
        unavailable(link, "Quiz coming soon. This ID is not present in the configured bank.");
        continue;
      }
      const target = new URL(config.poll, document.baseURI);
      target.searchParams.set("question_id", id);
      if (link.dataset.quizSlug) target.searchParams.set("quiz", link.dataset.quizSlug);
      link.href = target.href;
      link.textContent = "Open this poll question";
      link.removeAttribute("aria-disabled");
      link.dataset.quizUnavailable = "false";
      link.addEventListener("click", () => {
        const sessionPanel = link.closest("[data-session-badge]");
        const badgeId = sessionPanel?.dataset.sessionBadge;
        if (!badgeId) return;
        try {
          const key = "mdc301.selfcheck.opened.v1";
          const saved = JSON.parse(localStorage.getItem(key) || "{}");
          const ids = new Set(Array.isArray(saved[badgeId]) ? saved[badgeId] : []);
          ids.add(id);
          saved[badgeId] = [...ids];
          localStorage.setItem(key, JSON.stringify(saved));
        } catch (_error) { /* Badge completion remains a student self-attestation if storage is blocked. */ }
      });
      const status = link.closest("li")?.querySelector("[data-quiz-status]");
      if (status) status.textContent = "ID found in a provided Week 1 quiz; opens that question.";
    }
  }

  initialize();
})();
