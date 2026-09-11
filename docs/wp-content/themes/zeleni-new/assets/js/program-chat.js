/* "Chatujte s chatbotem o programu" modal on /program. Calls the
   program-chat-worker (see /program-chat-worker in the repo root) which
   answers using Claude, grounded in the full program text. */
(function () {
  "use strict";

  // Set after deploying program-chat-worker (see its README) — e.g.
  // "https://zb-program-chat.<your-subdomain>.workers.dev/chat".
  var PROGRAM_CHAT_ENDPOINT = "https://zb-program-chat.zelenebrno.workers.dev/chat";

  var modal = document.querySelector("[data-program-chat-modal]");
  if (!modal) return;

  var openBtns = document.querySelectorAll("[data-open-program-chat]");
  var closeEls = modal.querySelectorAll("[data-program-chat-close]");
  var chips = modal.querySelectorAll("[data-chat-question]");
  var input = modal.querySelector("[data-chat-input]");
  var form = modal.querySelector("[data-program-chat-form]");
  var submitBtn = modal.querySelector("[data-chat-submit]");
  var answerBox = modal.querySelector("[data-chat-answer]");

  function open(fromHash) {
    modal.hidden = false;
    modal.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("program-chat-open");
    if (input) input.focus();
    if (!fromHash && location.hash !== "#chat") {
      history.pushState({ zbChat: true }, "", "#chat");
    }
    if (window.umami) window.umami.track("chat-opened");
  }
  function close(fromHash) {
    modal.setAttribute("aria-hidden", "true");
    document.documentElement.classList.remove("program-chat-open");
    window.setTimeout(function () { modal.hidden = true; }, 300);
    if (!fromHash && location.hash === "#chat") {
      history.pushState(null, "", location.pathname + location.search);
    }
  }

  openBtns.forEach(function (btn) { btn.addEventListener("click", function () { open(false); }); });
  closeEls.forEach(function (el) { el.addEventListener("click", function () { close(false); }); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !modal.hidden) close(false);
  });
  window.addEventListener("hashchange", function () {
    if (location.hash === "#chat") open(true);
    else if (!modal.hidden) close(true);
  });
  if (location.hash === "#chat") open(true);
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      if (input) {
        input.value = chip.textContent.trim();
        input.focus();
      }
    });
  });

  // Belt-and-braces: the system prompt asks the model for plain text, but it
  // doesn't always comply — strip stray Markdown syntax before displaying.
  function stripMarkdown(text) {
    return text
      .replace(/^#{1,6}\s*/gm, "")
      .replace(/\*\*(.+?)\*\*/g, "$1")
      .replace(/(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)/g, "$1")
      .replace(/^\s*[-*]\s+/gm, "- ");
  }

  // Turns bare URLs in plain text into real <a> links, without ever
  // interpreting the rest of the model's output as HTML (only the matched
  // URL substrings become elements — everything else stays a text node).
  var urlRegex = /(https?:\/\/[^\s<>"]+[^\s<>".,;:!?)])/g;
  function renderTextWithLinks(container, text) {
    container.textContent = "";
    var lastIndex = 0;
    var match;
    urlRegex.lastIndex = 0;
    while ((match = urlRegex.exec(text))) {
      if (match.index > lastIndex) {
        container.appendChild(document.createTextNode(text.slice(lastIndex, match.index)));
      }
      var a = document.createElement("a");
      a.href = match[0];
      a.textContent = match[0];
      a.target = "_blank";
      a.rel = "noopener";
      container.appendChild(a);
      lastIndex = match.index + match[0].length;
    }
    if (lastIndex < text.length) {
      container.appendChild(document.createTextNode(text.slice(lastIndex)));
    }
  }

  function showAnswer(text, variant) {
    if (!answerBox) return;
    answerBox.hidden = false;
    answerBox.classList.remove("is-loading", "is-error");
    if (variant === "is-loading") {
      answerBox.innerHTML =
        '<span class="program-chat-modal__loading">' +
          '<span class="program-chat-modal__dots"><span></span><span></span><span></span></span>' +
          text +
        "</span>";
    } else if (variant === "is-error") {
      answerBox.textContent = text;
    } else {
      renderTextWithLinks(answerBox, stripMarkdown(text));
    }
    if (variant) answerBox.classList.add(variant);
  }

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var question = input ? input.value.trim() : "";
      if (!question) return;

      if (!PROGRAM_CHAT_ENDPOINT) {
        showAnswer("Chat zatím není zapojený — chybí adresa serveru v program-chat.js.", "is-error");
        return;
      }

      submitBtn.disabled = true;
      showAnswer("Hledám odpověď v programu…", "is-loading");

      fetch(PROGRAM_CHAT_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question }),
      })
        .then(function (resp) {
          return resp.json().then(function (data) {
            if (!resp.ok) throw new Error(data.error || "Chyba serveru.");
            return data;
          });
        })
        .then(function (data) {
          showAnswer(data.answer);
        })
        .catch(function (err) {
          console.error("Program chat error:", err);
          showAnswer(err.message || "Něco se nepovedlo, zkuste to prosím znovu.", "is-error");
        })
        .finally(function () {
          submitBtn.disabled = false;
        });
    });
  }
})();
