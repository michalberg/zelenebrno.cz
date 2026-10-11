/* Floating newsletter widget (sitewide, post-election).
   Builds its own markup and injects it before </body> on every page, so no
   page template needs to carry it by hand. Posts into the same Action Network
   form and tag as the inline newsletter box (newsletter-form.js), so contacts
   end up in one list. Opens by itself after a few seconds or once the visitor
   scrolls a bit; on later pages of the same visit it stays a collapsed pill. */
(function () {
  "use strict";

  var CONFIG = {
    anSubmissionUrl:
      "https://actionnetwork.org/api/v2/forms/396d43a2-696d-4c38-969f-9af48e107597/submissions/",
    tag: "brno_newsletter",
    avatarSrc: "/wp-content/uploads/sites/123/2026/09/natalie-avatar.jpg",
    delayMs: 6000,
    scrollRatio: 0.3,
  };

  var DISMISS_KEY = "zbw_newsletter_dismissed_v1";
  var SUBMITTED_KEY = "zbw_newsletter_submitted_v1";
  var SEEN_KEY = "zbw_newsletter_seen_v1";

  var emailRegex =
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;

  function ls(key) {
    try { return window.localStorage.getItem(key); } catch (e) { return null; }
  }
  function setLs(key, val) {
    try { window.localStorage.setItem(key, val); } catch (e) { /* ignore */ }
  }
  function ss(key) {
    try { return window.sessionStorage.getItem(key); } catch (e) { return null; }
  }
  function setSs(key, val) {
    try { window.sessionStorage.setItem(key, val); } catch (e) { /* ignore */ }
  }

  function buildMarkup() {
    var wrap = document.createElement("div");
    wrap.className = "zbw";
    wrap.setAttribute("data-zbw", "");
    wrap.innerHTML =
      '<div class="zbw-pill-wrap">' +
        '<button type="button" class="zbw-pill" data-zbw-open aria-label="Otevřít: Zůstaňme v kontaktu">' +
          '<span class="zbw-pill__text">ZŮSTAŇME<br><span class="zbw-accent">V KONTAKTU</span></span>' +
        '</button>' +
        '<button type="button" class="zbw-close" data-zbw-dismiss aria-label="Zavřít">' +
          '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>' +
        '</button>' +
      '</div>' +
      '<div class="zbw-panel">' +
        '<button type="button" class="zbw-panel__collapse" data-zbw-collapse aria-label="Zavřít">' +
          '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>' +
        '</button>' +
        '<div class="zbw-form">' +
          '<div class="zbw-panel__author">' +
            '<img src="' + CONFIG.avatarSrc + '" alt="" width="40" height="40">' +
            '<span><strong>Natálie Vencovská</strong><br>zastupitelka města Brna</span>' +
          '</div>' +
          '<h3 class="zbw-panel__title">Zůstaňme v kontaktu</h3>' +
          '<p class="zbw-panel__text">Díky vám je nás v zastupitelstvu dvakrát víc. Budu vám psát, co se nám daří prosadit, o čem se v Brně rozhoduje a kdy se můžeme potkat.</p>' +
          '<form novalidate>' +
            '<div class="zbw-hp" aria-hidden="true"><label>Nevyplňujte, pokud jste člověk<input type="text" name="website" tabindex="-1" autocomplete="off" data-zbw-hp></label></div>' +
            '<div class="zbw-field">' +
              '<input type="email" name="email" placeholder="vas@email.cz" aria-label="Váš e-mail" required autocomplete="email" data-zbw-email>' +
            '</div>' +
            '<p class="zbw-error" data-zbw-email-error>Zadejte prosím platný e-mail.</p>' +
            '<label class="zbw-consent">' +
              '<input type="checkbox" data-zbw-consent>' +
              '<span>Souhlasím se zasíláním zpráv a pozvánek brněnských Zelených. <a href="https://www.zeleni.cz/ochrana-osobnich-udaju/" target="_blank" rel="noopener">Jak s údaji zacházíme</a></span>' +
            '</label>' +
            '<p class="zbw-error" data-zbw-consent-error>Pro odeslání je potřeba zaškrtnout souhlas.</p>' +
            '<button type="submit" class="zbw-submit" data-zbw-submit>Chci vědět, co se děje</button>' +
          '<p class="zbw-reassure">Žádný spam. Odhlásit se můžete jedním kliknutím.</p>' +
          '</form>' +
        '</div>' +
        '<div class="zbw-success">' +
          '<h3>Děkuju!</h3>' +
          '<p>Jste na seznamu. Brzy se vám ozvu. Natálie</p>' +
        '</div>' +
      '</div>';
    return wrap;
  }

  function init() {
    if (ls(DISMISS_KEY) || ls(SUBMITTED_KEY)) return;
    // Not on /darujte/: the full donation form is the one ask there.
    if (document.querySelector("[data-donate-form]")) return;

    var el = buildMarkup();
    document.body.appendChild(el);

    var openBtn = el.querySelector("[data-zbw-open]");
    var dismissBtn = el.querySelector("[data-zbw-dismiss]");
    var collapseBtn = el.querySelector("[data-zbw-collapse]");
    var form = el.querySelector("form");
    var emailInput = el.querySelector("[data-zbw-email]");
    var emailError = el.querySelector("[data-zbw-email-error]");
    var consentInput = el.querySelector("[data-zbw-consent]");
    var consentError = el.querySelector("[data-zbw-consent-error]");
    var honeypot = el.querySelector("[data-zbw-hp]");
    var submitBtn = el.querySelector("[data-zbw-submit]");

    // Nudge the widget above the footer instead of overlapping it (e.g. the
    // Facebook/Instagram icons) once the footer scrolls into view.
    var footer = document.querySelector("footer");
    if (footer && window.IntersectionObserver) {
      var footerObserver = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            el.classList.toggle("is-above-footer", entry.isIntersecting);
          });
        },
        { rootMargin: "0px" }
      );
      footerObserver.observe(footer);
    }

    // The collapsed pill hides while the inline newsletter box is on screen
    // (same sign-up twice). An open panel never hides — the visitor may be
    // typing into it (see .is-suppressed in styles.css).
    var busyEls = document.querySelectorAll("[data-newsletter-form]");
    if (busyEls.length && window.IntersectionObserver) {
      var busySet = new Set();
      var busyObserver = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) busySet.add(entry.target);
            else busySet.delete(entry.target);
          });
          el.classList.toggle("is-suppressed", busySet.size > 0);
        },
        { threshold: 0.25 }
      );
      busyEls.forEach(function (e) { busyObserver.observe(e); });
    }

    function reveal() {
      el.classList.add("is-visible");
    }
    function open() {
      el.classList.add("is-open");
    }
    function collapse() {
      el.classList.remove("is-open");
    }
    function dismiss() {
      el.classList.remove("is-visible", "is-open");
      setLs(DISMISS_KEY, "1");
    }

    openBtn.addEventListener("click", open);
    collapseBtn.addEventListener("click", collapse);
    dismissBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      dismiss();
    });

    function validateEmail() {
      var val = emailInput.value.trim();
      var valid = Boolean(val) && emailRegex.test(val);
      emailError.classList.toggle("is-visible", !valid);
      return valid;
    }
    emailInput.addEventListener("blur", validateEmail);

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (honeypot.value !== "") return;
      if (!consentInput.checked) {
        consentError.classList.add("is-visible");
        return;
      }
      consentError.classList.remove("is-visible");
      if (!validateEmail()) return;

      submitBtn.disabled = true;
      submitBtn.textContent = "Odesílám…";

      fetch(CONFIG.anSubmissionUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          person: {
            email_addresses: [{ address: emailInput.value.trim(), status: "subscribed" }],
          },
          add_tags: [CONFIG.tag, "brno-vsichni"],
          triggers: { autoresponse: { enabled: false } },
        }),
      })
        .then(function (resp) {
          if (!resp.ok) throw new Error("HTTP " + resp.status);
          el.classList.add("is-submitted");
          setLs(SUBMITTED_KEY, "1");
          if (window.umami) window.umami.track("newsletter-popup-submit", { tag: CONFIG.tag });
        })
        .catch(function (err) {
          console.error("Floating widget submit error:", err);
          submitBtn.disabled = false;
          submitBtn.textContent = "Chci vědět, co se děje";
          emailError.textContent = "Něco se nepovedlo, zkuste to prosím znovu.";
          emailError.classList.add("is-visible");
        });
    });

    // Discover: once per visit, opened, after a few seconds or a short scroll,
    // whichever comes first. Later pages of the visit show just the pill.
    if (ss(SEEN_KEY)) {
      reveal();
      return;
    }

    var triggered = false;
    function trigger() {
      if (triggered) return;
      triggered = true;
      setSs(SEEN_KEY, "1");
      reveal();
      open();
      window.removeEventListener("scroll", onScroll);
      clearTimeout(timer);
    }
    function onScroll() {
      var scrolled = window.scrollY || document.documentElement.scrollTop;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      if (max > 0 && scrolled / max >= CONFIG.scrollRatio) trigger();
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    var timer = setTimeout(trigger, CONFIG.delayMs);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
