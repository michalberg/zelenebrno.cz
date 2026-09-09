/* Compact "amount + continue" teaser used on the homepage — the full donor
   form (name, address, birth date...) lives only on /darujte/, reached with
   the picked amount carried over via ?amount=. Keeps the homepage CTA short. */
(function () {
  "use strict";

  function initInstance(root) {
    var target = root.getAttribute("data-target");
    var btns = root.querySelectorAll("[data-amount]");
    var custom = root.querySelector("[data-amount-custom]");
    var link = root.querySelector("[data-donate-teaser-link]");
    if (!link) return;
    var selected = 1000;

    function updateLink() {
      var v = custom.value.trim();
      link.href = target + "?amount=" + encodeURIComponent(v || selected);
    }

    btns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        selected = Number(btn.dataset.amount);
        btns.forEach(function (b) { b.classList.toggle("is-selected", b === btn); });
        custom.value = "";
        custom.classList.remove("has-value");
        updateLink();
      });
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

    updateLink();
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
