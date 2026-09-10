/* Inline volunteer sign-up form on /zapoj-se. Posts straight to the Action
   Network form used campaign-wide for volunteer sign-up (same endpoint as
   newsletter-form.js and natalievencovska.cz's volunteer form), with the
   question fields (mestska_cast, podpora, expertiza) that the public embed
   at actionnetwork.org/forms/kampan-brno/ collects. */
(function () {
  "use strict";

  var AN_URL = "https://actionnetwork.org/api/v2/forms/396d43a2-696d-4c38-969f-9af48e107597/submissions/";

  var emailRegex =
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;

  function initInstance(root) {
    var form = root.querySelector("form");
    if (!form) return;
    var success = root.querySelector("[data-vf-success]");
    var error = root.querySelector("[data-vf-error]");
    var honeypot = root.querySelector("[data-vf-hp]");
    var submitBtn = root.querySelector("[data-vf-submit]");
    var originalText = submitBtn ? submitBtn.textContent : "";

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (honeypot && honeypot.value !== "") return;

      var firstName = form.querySelector("[data-vf-first-name]").value.trim();
      var lastName = form.querySelector("[data-vf-last-name]").value.trim();
      var email = form.querySelector("[data-vf-email]").value.trim();
      var phone = form.querySelector("[data-vf-phone]").value.trim();
      var district = form.querySelector("[data-vf-district]").value.trim();
      var help = form.querySelector("[data-vf-help]").value.trim();
      var time = form.querySelector("[data-vf-time]").value.trim();

      if (!firstName || !lastName || !email || !emailRegex.test(email)) {
        error.classList.add("is-visible");
        return;
      }
      error.classList.remove("is-visible");
      submitBtn.disabled = true;
      submitBtn.textContent = "Odesílám…";

      var customFields = {};
      if (district) customFields.mestska_cast = district;
      if (help) customFields.podpora = help;
      if (time) customFields.expertiza = time;

      var person = {
        given_name: firstName,
        family_name: lastName,
        email_addresses: [{ address: email, status: "subscribed" }],
      };
      if (phone) person.phone_numbers = [{ number: phone }];
      if (district) person.postal_addresses = [{ locality: district, country: "CZ" }];
      if (Object.keys(customFields).length) person.custom_fields = customFields;

      fetch(AN_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          person: person,
          add_tags: ["brno_kampan"],
        }),
      })
        .then(function (resp) {
          if (!resp.ok) throw new Error("HTTP " + resp.status);
          form.hidden = true;
          success.hidden = false;
        })
        .catch(function (err) {
          console.error("Volunteer form submit error:", err);
          submitBtn.disabled = false;
          submitBtn.textContent = originalText;
          error.textContent = "Něco se nepovedlo, zkuste to prosím znovu.";
          error.classList.add("is-visible");
        });
    });
  }

  function init() {
    document.querySelectorAll("[data-volunteer-form]").forEach(initInstance);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
