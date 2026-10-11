/* Compact "frequency + amount + continue" teaser used on the homepage — the
   full donor form (name, address, birth date...) lives only on /darujte/,
   reached with the picked frequency and amount carried over via
   ?freq=month|once&amount=. Keeps the homepage CTA short. Presets match
   donate-form.js. */
(function () {
  "use strict";

  var PRESETS = {
    month: { amounts: [150, 300, 500, 1000], selected: 300 },
    once: { amounts: [300, 500, 1000, 2000], selected: 1000 },
  };

  function initInstance(root) {
    var target = root.getAttribute("data-target");
    var amountsWrap = root.querySelector(".zb-donate-amounts");
    var custom = root.querySelector("[data-amount-custom]");
    var link = root.querySelector("[data-donate-teaser-link]");
    var freqBtns = root.querySelectorAll("[data-freq]");
    if (!link || !amountsWrap || !custom) return;
    var freq = "month";
    var selected = PRESETS[freq].selected;
    var btns = [];

    function updateLink() {
      var v = custom.value.trim();
      link.href = target + "?freq=" + freq + "&amount=" + encodeURIComponent(v || selected);
    }

    function renderAmounts() {
      btns.forEach(function (b) { b.remove(); });
      btns = PRESETS[freq].amounts.map(function (a) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "zb-amount-btn" + (a === selected && !custom.value.trim() ? " is-selected" : "");
        btn.dataset.amount = a;
        btn.textContent = a + " Kč";
        btn.addEventListener("click", function () {
          selected = a;
          btns.forEach(function (b) { b.classList.toggle("is-selected", b === btn); });
          custom.value = "";
          custom.classList.remove("has-value");
          updateLink();
        });
        amountsWrap.insertBefore(btn, custom);
        return btn;
      });
    }

    function setFreq(f) {
      freq = f;
      freqBtns.forEach(function (b) {
        var on = b.dataset.freq === f;
        b.classList.toggle("is-selected", on);
        b.setAttribute("aria-checked", on ? "true" : "false");
      });
      selected = PRESETS[f].selected;
      custom.value = "";
      custom.classList.remove("has-value");
      renderAmounts();
      updateLink();
    }

    freqBtns.forEach(function (b) {
      b.addEventListener("click", function () { setFreq(b.dataset.freq); });
    });
    custom.addEventListener("input", function () {
      if (custom.value.trim()) {
        btns.forEach(function (b) { b.classList.remove("is-selected"); });
        custom.classList.add("has-value");
      } else {
        btns.forEach(function (b) { b.classList.toggle("is-selected", Number(b.dataset.amount) === selected); });
        custom.classList.remove("has-value");
      }
      updateLink();
    });

    setFreq("month");
  }

  function init() {
    document.querySelectorAll("[data-donate-teaser]").forEach(initInstance);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
