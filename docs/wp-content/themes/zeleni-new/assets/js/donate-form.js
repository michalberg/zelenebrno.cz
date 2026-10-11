/* Donate form submission — ported from natalievencovska.cz, unchanged target
   (same fund, same bank account). Wires up every [data-donate-form] instance
   on the page independently.

   Supports one-off and monthly donations by bank transfer. A monthly gift is
   sent to the dary.zeleni.cz API the same way its own form does it
   (periodicity "month", periodical true, endDate one year ahead) and the
   thank-you screen asks for a standing order instead of showing a QR code —
   banks turn a QR payment into a one-off transfer. */
(function () {
  "use strict";

  var API_URL = "https://api.dary.zeleni.cz/payments";
  var FUND_ID = "57e111cd859b5a092c8c7c1a";
  var BANK_ACCOUNT = "2400146729/2010";
  var BANK_IBAN = "CZ5520100000002400146729";

  // Donors also go to Action Network (same form and field names as the
  // lepsibrno.cz donation pages). Sent on submit, like there: with a bank
  // transfer no payment gateway confirms the gift for us. AN's auto-response
  // stays off, dary.zeleni.cz already sends its own confirmation.
  var AN_URL = "https://actionnetwork.org/api/v2/forms/bc501b67-c587-494a-bf1e-570a9f73e8f5/submissions/";
  var AN_TAGS = ["brno-darci", "lepsibrno"];

  // Amount presets per frequency; the second value is preselected.
  var PRESETS = {
    month: { amounts: [150, 300, 500, 1000], selected: 300 },
    once: { amounts: [300, 500, 1000, 2000], selected: 1000 },
  };
  var NOTES = {
    month: "Po odeslání vám ukážeme údaje pro nastavení trvalého příkazu ve vaší bance.",
    once: "Po odeslání obdržíte platební údaje a QR kód pro převod.",
  };

  // Same default as dary.zeleni.cz: the 1st of the month, twelve months ahead.
  function defaultEndDate() {
    var d = new Date();
    return new Date(d.getFullYear() + 1, d.getMonth() + 1, 1);
  }

  function initInstance(root) {
    var form = root.querySelector("form");
    var success = root.querySelector("[data-donate-success]");
    if (!form || !success) return;

    var amountsWrap = root.querySelector("[data-donate-amounts]");
    var customAmount = root.querySelector("[data-amount-custom]");
    var note = root.querySelector("[data-donate-note]");
    var freqBtns = root.querySelectorAll("[data-freq]");
    var submitBtn = root.querySelector("[data-donate-submit]");
    var freq = "month";
    var selectedAmount = PRESETS[freq].selected;
    var amountBtns = [];

    function updateLabel() {
      var v = customAmount.value.trim();
      // Re-queried: the submit button's HTML is restored after a failed send.
      var amountLabel = root.querySelector("[data-donate-amount-label]");
      if (!amountLabel) return;
      amountLabel.textContent = (v || selectedAmount) + " Kč" + (freq === "month" ? " měsíčně" : "");
    }

    function renderAmounts() {
      amountBtns.forEach(function (b) { b.remove(); });
      amountBtns = PRESETS[freq].amounts.map(function (a) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "zb-amount-btn" + (a === selectedAmount && !customAmount.value.trim() ? " is-selected" : "");
        btn.dataset.amount = a;
        btn.textContent = a + " Kč";
        btn.addEventListener("click", function () {
          selectedAmount = a;
          amountBtns.forEach(function (b) { b.classList.toggle("is-selected", b === btn); });
          customAmount.value = "";
          customAmount.classList.remove("has-value");
          updateLabel();
        });
        amountsWrap.insertBefore(btn, customAmount);
        return btn;
      });
    }

    function setFreq(f) {
      if (!PRESETS[f]) return;
      freq = f;
      freqBtns.forEach(function (b) {
        var on = b.dataset.freq === f;
        b.classList.toggle("is-selected", on);
        b.setAttribute("aria-checked", on ? "true" : "false");
      });
      selectedAmount = PRESETS[f].selected;
      renderAmounts();
      if (note) note.textContent = NOTES[f];
      updateLabel();
    }

    freqBtns.forEach(function (b) {
      b.addEventListener("click", function () { setFreq(b.dataset.freq); });
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

    // Homepage teaser links here as /darujte/?freq=month&amount=300.
    var params = new URLSearchParams(location.search);
    setFreq(params.get("freq") === "once" ? "once" : "month");
    var queryAmount = params.get("amount");
    if (queryAmount && /^\d+$/.test(queryAmount)) {
      var preset = amountBtns.filter(function (b) { return b.dataset.amount === queryAmount; })[0];
      if (preset) {
        preset.click();
      } else {
        customAmount.value = queryAmount;
        customAmount.dispatchEvent(new Event("input"));
      }
    }

    var originalBtnHTML = submitBtn ? submitBtn.innerHTML : "";

    function field(name) {
      var el = form.querySelector('[data-field="' + name + '"]');
      return el ? el.value.trim() : "";
    }
    function getAmount() {
      var custom = customAmount.value.trim();
      if (custom) return Number(custom);
      return selectedAmount;
    }
    function setText(sel, text) {
      var el = success.querySelector(sel);
      if (el) el.textContent = text;
    }
    function show(sel, on) {
      var el = success.querySelector(sel);
      if (el) el.hidden = !on;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var amount = getAmount();
      if (!amount || amount < 1) {
        alert("Vyplňte prosím částku.");
        return;
      }
      var monthly = freq === "month";

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
        payment: monthly
          ? { method: "transfer", amount: amount, periodical: true, periodicity: "month", endDate: defaultEndDate() }
          : { method: "transfer", amount: amount, periodical: false, periodicity: null, endDate: null },
        message: null,
      };

      fetch(AN_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          person: {
            given_name: donor.name,
            family_name: donor.surname,
            email_addresses: [{ address: donor.email }],
            phone_numbers: donor.mobile ? [{ number: donor.mobile }] : undefined,
            postal_addresses: [{
              address_lines: donor.address ? [donor.address] : undefined,
              locality: donor.city,
              postal_code: donor.zip,
              country: "CZ",
            }],
            custom_fields: {
              datum_narozeni: donor.birth,
              castka_daru: amount,
              periodicita: monthly ? "mesicne" : "jednorazove",
              zpusob_platby: "prevod",
            },
          },
          "action_network:referrer_data": { source: "zelenebrno.cz", website: location.href },
          add_tags: AN_TAGS,
          triggers: { autoresponse: { enabled: false } },
        }),
        keepalive: true,
      }).catch(function (err) { console.warn("Action Network submit failed:", err); });

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
          var amountText = amount.toLocaleString("cs-CZ");
          setText("[data-success-amount]", amountText);
          setText("[data-success-amount-m]", amountText);
          setText("[data-success-amount-2]", amountText);
          setText("[data-success-email]", donor.email);
          setText("[data-success-email-m]", donor.email);
          setText("[data-success-account]", BANK_ACCOUNT);
          setText("[data-success-iban]", BANK_IBAN);
          setText("[data-success-vs]", data.vs || "—");

          show("[data-success-once-text]", !monthly);
          show("[data-success-once-note]", !monthly);
          show("[data-success-month-text]", monthly);
          show("[data-success-month-note]", monthly);
          show("[data-success-freq-row]", monthly);
          show("[data-success-msg-row]", monthly);
          show("[data-success-qr-wrap]", !monthly);
          success.classList.toggle("is-monthly", monthly);

          form.style.display = "none";
          success.hidden = false;
          if (window.umami) window.umami.track("donate-form-submit", { freq: freq, amount: amount });

          if (!monthly) {
            var ibanCompact = BANK_IBAN.replace(/\s+/g, "");
            var spayd = "SPD*1.0*ACC:" + ibanCompact + "*AM:" + amount + ".00*CC:CZK*X-VS:" + data.vs + "*MSG:DAR";
            var qrImg = success.querySelector("[data-success-qr]");
            if (qrImg) {
              qrImg.src = "https://api.qrserver.com/v1/create-qr-code/?size=220x220&margin=4&data=" + encodeURIComponent(spayd);
            }
          }
          success.scrollIntoView({ behavior: "smooth", block: "start" });
        })
        .catch(function (err) {
          console.error("Donate submit error:", err);
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnHTML;
            updateLabel();
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
