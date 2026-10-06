/* RSVP for the election-night results watch party on /sledovani.
   Posts into the same Action Network volunteer form as newsletter-form.js
   (autoresponse disabled), tagged brno-sledovani; probability and arrival
   time go into custom_fields, as does the "napíšu 5 lidem" pledge. */
(function () {
  "use strict";

  var AN_URL = "https://actionnetwork.org/api/v2/forms/396d43a2-696d-4c38-969f-9af48e107597/submissions/";

  var emailRegex =
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;

  function checked(form, name) {
    var el = form.querySelector('input[name="' + name + '"]:checked');
    return el ? el.value : "";
  }

  function initInstance(root) {
    var form = root.querySelector("form");
    var success = root.querySelector("[data-rsvp-success]");
    var error = root.querySelector("[data-rsvp-error]");
    var honeypot = root.querySelector("[data-rsvp-hp]");
    var submitBtn = root.querySelector("[data-rsvp-submit]");
    var tag = root.getAttribute("data-tag") || "brno-sledovani";
    if (!form) return;
    var originalText = submitBtn.textContent;
    initPledge(root);

    function showError(msg) {
      error.textContent = msg;
      error.classList.add("is-visible");
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (honeypot && honeypot.value !== "") return;

      var givenName = form.given_name.value.trim();
      var familyName = form.family_name.value.trim();
      var email = form.email.value.trim();
      var probability = checked(form, "pravdepodobnost");
      var arrival = checked(form, "cas_prichodu");
      var pledged = form.slib.checked;

      if (!givenName || !familyName) return showError("Vyplňte prosím jméno a příjmení.");
      if (!emailRegex.test(email)) return showError("Zadejte prosím platný e-mail.");
      if (!probability) return showError("Vyberte prosím, s jakou pravděpodobností dorazíte.");
      if (!arrival) return showError("Vyberte prosím, v kolik hodin zhruba dorazíte.");

      error.classList.remove("is-visible");
      submitBtn.disabled = true;
      submitBtn.textContent = "Odesílám…";

      fetch(AN_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          person: {
            given_name: givenName,
            family_name: familyName,
            email_addresses: [{ address: email, status: "subscribed" }],
            custom_fields: {
              sledovani_pravdepodobnost: probability,
              sledovani_cas_prichodu: arrival,
              sledovani_slib_5_lidi: pledged ? "ano" : "ne",
            },
          },
          add_tags: [tag],
          triggers: { autoresponse: { enabled: false } },
        }),
      })
        .then(function (resp) {
          if (!resp.ok) throw new Error("HTTP " + resp.status);
          form.hidden = true;
          success.hidden = false;
          success.querySelector("[data-rsvp-success-pledge]").hidden = !pledged;
          if (window.umami) window.umami.track("sledovani-submit", { pravdepodobnost: probability, cas: arrival, slib: pledged });
        })
        .catch(function (err) {
          console.error("RSVP submit error:", err);
          submitBtn.disabled = false;
          submitBtn.textContent = originalText;
          showError("Něco se nepovedlo, zkuste to prosím znovu.");
        });
    });
  }

  function initPledge(root) {
    var msgEl = root.querySelector("[data-pledge-msg]");
    var copyBtn = root.querySelector("[data-pledge-copy]");
    var waLink = root.querySelector("[data-pledge-wa]");
    if (!msgEl) return;
    var message = msgEl.textContent.trim();

    if (waLink) {
      waLink.href = "https://wa.me/?text=" + encodeURIComponent(message);
      waLink.addEventListener("click", function () {
        if (window.umami) window.umami.track("sledovani-whatsapp");
      });
    }

    if (copyBtn) {
      var copyText = copyBtn.textContent;
      copyBtn.addEventListener("click", function () {
        var done = function () {
          copyBtn.textContent = "Zkopírováno ✓";
          setTimeout(function () { copyBtn.textContent = copyText; }, 2000);
          if (window.umami) window.umami.track("sledovani-kopirovat");
        };
        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(message).then(done, function () { fallbackCopy(message) && done(); });
        } else if (fallbackCopy(message)) {
          done();
        }
      });
    }
  }

  function fallbackCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "absolute";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(ta);
    return ok;
  }

  function init() {
    document.querySelectorAll("[data-rsvp-form]").forEach(initInstance);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
