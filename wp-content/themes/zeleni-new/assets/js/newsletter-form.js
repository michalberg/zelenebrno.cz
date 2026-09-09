/* Generic "chci vědět o dalších akcích" newsletter opt-in — homepage CTA band
   (tag web-general) and /prochazky inline block (tag web-prochazky).
   NOTE: posts into the same Action Network form used for volunteer sign-up
   on natalievencovska.cz (the only confirmed-working public AN endpoint we
   have for this campaign) with autoresponse explicitly disabled, distinguished
   only by add_tags. Swap ANY_URL for a dedicated form if/when one exists. */
(function () {
  "use strict";

  var DEFAULT_AN_URL = "https://actionnetwork.org/api/v2/forms/396d43a2-696d-4c38-969f-9af48e107597/submissions/";

  var emailRegex =
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;

  function initInstance(root) {
    var form = root.querySelector("form");
    var success = root.querySelector("[data-newsletter-success]");
    var emailInput = root.querySelector("[data-newsletter-email]");
    var error = root.querySelector("[data-newsletter-error]");
    var honeypot = root.querySelector("[data-newsletter-hp]");
    var submitBtn = root.querySelector("[data-newsletter-submit]");
    var tag = root.getAttribute("data-tag") || "web-general";
    var anUrl = root.getAttribute("data-an-url") || DEFAULT_AN_URL;
    var autoresponse = root.getAttribute("data-autoresponse") === "true";
    if (!form) return;
    var originalText = submitBtn ? submitBtn.textContent : "";

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (honeypot && honeypot.value !== "") return;
      var email = emailInput.value.trim();
      if (!email || !emailRegex.test(email)) {
        error.classList.add("is-visible");
        return;
      }
      error.classList.remove("is-visible");
      submitBtn.disabled = true;
      submitBtn.textContent = "Odesílám…";

      fetch(anUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          person: { email_addresses: [{ address: email, status: "subscribed" }] },
          add_tags: [tag],
          triggers: { autoresponse: { enabled: autoresponse } },
        }),
      })
        .then(function (resp) {
          if (!resp.ok) throw new Error("HTTP " + resp.status);
          form.hidden = true;
          success.hidden = false;
        })
        .catch(function (err) {
          console.error("Newsletter submit error:", err);
          submitBtn.disabled = false;
          submitBtn.textContent = originalText;
          error.textContent = "Něco se nepovedlo, zkuste to prosím znovu.";
          error.classList.add("is-visible");
        });
    });
  }

  function init() {
    document.querySelectorAll("[data-newsletter-form]").forEach(initInstance);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
