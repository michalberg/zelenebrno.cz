/* /vasi-lide checklist: 25 names in five groups, each with an "osloveno"
   checkbox and a WhatsApp button. Stored in this browser only (localStorage,
   best effort), never sent anywhere. Also wires copy/WhatsApp buttons for
   the sample message and the "pošlete dál" share text. */
(function () {
  "use strict";

  var STORAGE_KEY = "zb-vasi-lide-v2";
  var ROWS_PER_GROUP = 5;
  var GOAL = 25;
  var WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3.9 2.5 1.1 2.7.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.6-.3Z"/></svg>';

  function track(name, props) {
    if (window.umami && name) window.umami.track(name, props);
  }

  function load() {
    try {
      var d = JSON.parse(localStorage.getItem(STORAGE_KEY));
      return d && d.groups ? d : { groups: {} };
    } catch (e) {
      return { groups: {} };
    }
  }

  function save(data) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); } catch (e) {}
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(function () {
        if (!fallbackCopy(text)) throw new Error("copy failed");
      });
    }
    return fallbackCopy(text) ? Promise.resolve() : Promise.reject(new Error("copy failed"));
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

  function waHref(text) {
    return "https://wa.me/?text=" + encodeURIComponent(text);
  }

  var MSG_KEY = "zb-vasi-lide-msg";

  /* Sample message with a supporter/candidate switch. The textarea is
     editable; edits are remembered per role. Returns a getter for the
     current text so every WhatsApp/copy button sends what is shown. */
  function initMessage() {
    var area = document.querySelector("[data-msg]");
    if (!area) return function () { return ""; };
    var buttons = document.querySelectorAll("[data-msg-role]");
    var templates = {};
    document.querySelectorAll("[data-msg-template]").forEach(function (el) {
      templates[el.getAttribute("data-msg-template")] = el.textContent.trim();
    });
    var state;
    try { state = JSON.parse(localStorage.getItem(MSG_KEY)); } catch (e) {}
    if (!state || !state.texts) state = { role: "podporovatel", texts: {} };

    function persist() {
      try { localStorage.setItem(MSG_KEY, JSON.stringify(state)); } catch (e) {}
    }

    function show(role) {
      state.role = role;
      area.value = state.texts[role] || templates[role] || "";
      buttons.forEach(function (b) {
        var on = b.getAttribute("data-msg-role") === role;
        b.classList.toggle("is-active", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
      });
      persist();
    }

    buttons.forEach(function (b) {
      b.addEventListener("click", function () { show(b.getAttribute("data-msg-role")); });
    });
    area.addEventListener("input", function () {
      state.texts[state.role] = area.value;
      persist();
    });

    show(templates[state.role] ? state.role : "podporovatel");
    return function () { return area.value.trim(); };
  }

  function initShareButtons(getMessage) {
    var shareText = ((document.querySelector("[data-share]") || {}).textContent || "").trim();
    function textFor(kind) { return kind === "msg" ? getMessage() : shareText; }

    document.querySelectorAll("[data-wa]").forEach(function (a) {
      a.href = waHref(textFor(a.getAttribute("data-wa")));
      a.addEventListener("click", function () {
        a.href = waHref(textFor(a.getAttribute("data-wa")));
        track(a.getAttribute("data-umami-name"));
      });
    });
    document.querySelectorAll("[data-copy]").forEach(function (btn) {
      var label = btn.textContent;
      btn.addEventListener("click", function () {
        copyText(textFor(btn.getAttribute("data-copy"))).then(function () {
          btn.textContent = "Zkopírováno ✓";
          setTimeout(function () { btn.textContent = label; }, 2000);
          track(btn.getAttribute("data-umami-name"));
        });
      });
    });
  }

  function initChecklist(getMessage) {
    var root = document.querySelector("[data-people-form]");
    if (!root) return;
    var data = load();
    var groups = root.querySelectorAll("[data-group]");
    var progressEls = document.querySelectorAll("[data-progress]");
    var progressBar = root.querySelector("[data-progress-bar]");

    function counts() {
      var done = 0, named = 0;
      Object.keys(data.groups).forEach(function (k) {
        data.groups[k].forEach(function (item) {
          if (item.n.trim()) named++;
          if (item.d && item.n.trim()) done++;
        });
      });
      return { jmena: named, osloveno: done };
    }

    /* Only the counts go to Umami, never the names. Reported when the
       visitor leaves or hides the page, and only if they changed since the
       last report (remembered across visits). */
    var REPORT_KEY = "zb-vasi-lide-reported";
    var lastReported = "";
    try { lastReported = localStorage.getItem(REPORT_KEY) || ""; } catch (e) {}
    function reportCounts() {
      var c = counts();
      var sig = c.jmena + "/" + c.osloveno;
      if (c.jmena === 0 || sig === lastReported) return;
      lastReported = sig;
      try { localStorage.setItem(REPORT_KEY, sig); } catch (e) {}
      track("vasi-lide-seznam", c);
    }
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "hidden") reportCounts();
    });
    window.addEventListener("pagehide", reportCounts);

    function updateProgress() {
      var c = counts();
      var done = c.osloveno, named = c.jmena;
      var total = Math.max(GOAL, named);
      progressEls.forEach(function (el) { el.textContent = "Osloveno " + done + " z " + total; });
      if (progressBar) progressBar.style.width = Math.round((done / total) * 100) + "%";
    }

    function renderRow(container, items, idx, label) {
      var item = items[idx];
      var row = document.createElement("div");
      row.className = "zb-row" + (item.d ? " is-done" : "");

      var check = document.createElement("input");
      check.type = "checkbox";
      check.className = "zb-row-check";
      check.checked = !!item.d;
      check.setAttribute("aria-label", "Osloveno");

      var name = document.createElement("input");
      name.type = "text";
      name.className = "zb-row-name";
      name.value = item.n;
      name.autocomplete = "off";
      name.setAttribute("aria-label", label + " – " + (idx + 1) + ". člověk");

      var wa = document.createElement("a");
      wa.className = "zb-row-wa";
      wa.href = "#";
      wa.target = "_blank";
      wa.rel = "noopener";
      wa.setAttribute("aria-label", "Poslat zprávu přes WhatsApp");
      wa.title = "Poslat zprávu přes WhatsApp";
      wa.innerHTML = WA_ICON;

      function syncWa() { wa.setAttribute("aria-disabled", item.n.trim() ? "false" : "true"); }
      syncWa();

      name.addEventListener("input", function () {
        item.n = name.value;
        syncWa();
        save(data);
        updateProgress();
      });
      check.addEventListener("change", function () {
        item.d = check.checked;
        row.classList.toggle("is-done", item.d);
        save(data);
        updateProgress();
      });
      wa.addEventListener("click", function () {
        wa.href = waHref(getMessage());
        track("vasi-lide-radek-whatsapp");
      });

      row.appendChild(check);
      row.appendChild(name);
      row.appendChild(wa);
      container.appendChild(row);
      return name;
    }

    function render() {
      groups.forEach(function (fs) {
        var key = fs.getAttribute("data-group");
        var label = fs.getAttribute("data-group-label");
        var container = fs.querySelector("[data-rows]");
        var items = data.groups[key] || [];
        while (items.length < ROWS_PER_GROUP) items.push({ n: "", d: false });
        data.groups[key] = items;
        container.innerHTML = "";
        items.forEach(function (_, i) { renderRow(container, items, i, label); });
      });
      updateProgress();
    }

    groups.forEach(function (fs) {
      fs.querySelector("[data-add]").addEventListener("click", function () {
        var key = fs.getAttribute("data-group");
        var items = data.groups[key];
        items.push({ n: "", d: false });
        save(data);
        renderRow(fs.querySelector("[data-rows]"), items, items.length - 1, fs.getAttribute("data-group-label")).focus();
      });
    });

    root.querySelector("[data-people-print]").addEventListener("click", function () {
      track("vasi-lide-print", counts());
      window.print();
    });

    root.querySelector("[data-people-clear]").addEventListener("click", function () {
      if (!window.confirm("Opravdu vymazat celý seznam?")) return;
      data = { groups: {} };
      save(data);
      render();
    });

    render();
  }

  function init() {
    var getMessage = initMessage();
    initShareButtons(getMessage);
    initChecklist(getMessage);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
