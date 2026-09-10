/* Donate form submission — ported from natalievencovska.cz, unchanged target
   (same fund, same bank account) per the "beze změny" requirement. Wires up
   every [data-donate-form] instance on the page independently, so the same
   markup can appear on both /darujte and the homepage CTA band. */
(function () {
  "use strict";

  var API_URL = "https://api.dary.zeleni.cz/payments";
  var FUND_ID = "57e111cd859b5a092c8c7c1a";
  var BANK_ACCOUNT = "2400146729/2010";
  var BANK_IBAN = "CZ5520100000002400146729";

  function initInstance(root) {
    var form = root.querySelector("form");
    var success = root.querySelector("[data-donate-success]");
    if (!form || !success) return;

    var amountBtns = root.querySelectorAll("[data-amount]");
    var customAmount = root.querySelector("[data-amount-custom]");
    var amountLabel = root.querySelector("[data-donate-amount-label]");
    var submitBtn = root.querySelector("[data-donate-submit]");
    var originalBtnHTML = submitBtn ? submitBtn.innerHTML : "";
    var selectedAmount = 1000;

    function updateLabel() {
      var v = customAmount.value.trim();
      amountLabel.textContent = (v || selectedAmount) + " Kč";
    }
    amountBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        selectedAmount = Number(btn.dataset.amount);
        amountBtns.forEach(function (b) { b.classList.toggle("is-selected", b === btn); });
        customAmount.value = "";
        customAmount.classList.remove("has-value");
        updateLabel();
      });
    });
    customAmount.addEventListener("input", function () {
      if (customAmount.value.trim()) {
        amountBtns.forEach(function (b) { b.classList.remove("is-selected"); });
        customAmount.classList.add("has-value");
      } else {
        customAmount.classList.remove("has-value");
        amountBtns.forEach(function (b) { b.classList.toggle("is-selected", Number(b.dataset.amount) === selectedAmount); });
      }
      updateLabel();
    });

    // Homepage teaser links here as /darujte/?amount=500 — pick that amount up.
    var queryAmount = new URLSearchParams(location.search).get("amount");
    if (queryAmount) {
      var preset = Array.prototype.filter.call(amountBtns, function (b) {
        return b.dataset.amount === queryAmount;
      })[0];
      if (preset) {
        preset.click();
      } else if (/^\d+$/.test(queryAmount)) {
        customAmount.value = queryAmount;
        customAmount.dispatchEvent(new Event("input"));
      }
    }

    function field(name) {
      var el = form.querySelector('[data-field="' + name + '"]');
      return el ? el.value.trim() : "";
    }
    function getAmount() {
      var custom = customAmount.value.trim();
      if (custom) return Number(custom);
      return selectedAmount;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var amount = getAmount();
      if (!amount || amount < 1) {
        alert("Vyplňte prosím částku.");
        return;
      }

      var donor = {
        type: "person",
        name: field("firstName"),
        surname: field("lastName"),
        birth: field("birth"),
        email: field("email"),
        mobile: field("phone") || undefined,
        address: field("street"),
        city: field("city"),
        zip: field("zip"),
      };

      var payload = {
        fund: FUND_ID,
        donor: donor,
        payment: { method: "transfer", amount: amount, periodical: false, periodicity: null, endDate: null },
        message: null,
      };

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = "Odesílám…";
      }

      fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then(function (resp) {
          if (!resp.ok) throw new Error("HTTP " + resp.status);
          return resp.json();
        })
        .then(function (data) {
          success.querySelector("[data-success-amount]").textContent = amount.toLocaleString("cs-CZ");
          success.querySelector("[data-success-amount-2]").textContent = amount.toLocaleString("cs-CZ");
          success.querySelector("[data-success-email]").textContent = donor.email;
          success.querySelector("[data-success-account]").textContent = BANK_ACCOUNT;
          success.querySelector("[data-success-iban]").textContent = BANK_IBAN;
          success.querySelector("[data-success-vs]").textContent = data.vs || "—";

          form.style.display = "none";
          success.hidden = false;
          if (window.umami) window.umami.track("donate-form-submit");

          var ibanCompact = BANK_IBAN.replace(/\s+/g, "");
          var spayd = "SPD*1.0*ACC:" + ibanCompact + "*AM:" + amount + ".00*CC:CZK*X-VS:" + data.vs + "*MSG:DAR";
          var qrImg = success.querySelector("[data-success-qr]");
          if (qrImg) {
            qrImg.src = "https://api.qrserver.com/v1/create-qr-code/?size=220x220&margin=4&data=" + encodeURIComponent(spayd);
          }
          success.scrollIntoView({ behavior: "smooth", block: "start" });
        })
        .catch(function (err) {
          console.error("Donate submit error:", err);
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnHTML;
          }
          alert("Něco se nepovedlo, zkuste to prosím znovu. Pokud problém přetrvá, napište na natalie@zeleni.cz.");
        });
    });
  }

  function init() {
    document.querySelectorAll("[data-donate-form]").forEach(initInstance);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
