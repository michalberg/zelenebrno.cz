/* Homepage "Přijďte se potkat na naše procházky" widget — reads the shared walks data file
   (also the source for the full list on /prochazky/) and renders the three
   nearest upcoming walks, so the homepage always shows what's actually next
   without a rebuild. */
(function () {
  "use strict";

  var WEEKDAYS_CZ = ["Ne", "Po", "Út", "St", "Čt", "Pá", "So"];

  function initInstance(root) {
    var src = root.getAttribute("data-prochazky-src");
    if (!src) return;

    fetch(src)
      .then(function (resp) { return resp.json(); })
      .then(function (items) {
        var today = new Date();
        today.setHours(0, 0, 0, 0);
        var upcoming = items
          .filter(function (item) { return new Date(item.date + "T00:00:00") >= today; })
          .sort(function (a, b) { return a.date === b.date ? 0 : (a.date < b.date ? -1 : 1); })
          .slice(0, 3);

        if (!upcoming.length) {
          root.hidden = true;
          return;
        }

        root.innerHTML = upcoming.map(function (item, i) {
          var d = new Date(item.date + "T00:00:00");
          var kdy = WEEKDAYS_CZ[d.getDay()] + " " + d.getDate() + ". " + (d.getMonth() + 1) + ". | " + item.time;
          var badgeClass = i % 2 === 0 ? "bg-pink" : "bg-green";
          return (
            '<a class="group block bg-white shadow-card p-6" href="' + item.url + '" rel="noopener" target="_blank">' +
              '<span class="inline-block ' + badgeClass + ' text-ink font-name font-bold uppercase text-[13px] px-3 py-1 mb-3">' + kdy + '</span>' +
              '<h3 class="font-name text-[17px] font-extrabold leading-[1.25] text-ink tracking-tight mb-2">' + item.title + '</h3>' +
              '<p class="text-[13px] text-black/60 leading-[1.4] mb-3">' + item.desc + '</p>' +
              '<p class="text-[13px] text-black/50"><strong class="text-green-deep">' + item.place + '</strong><br>' + item.people + '</p>' +
            '</a>'
          );
        }).join("\n");
      })
      .catch(function (err) { console.error("Procházky widget error:", err); });
  }

  function init() {
    document.querySelectorAll("[data-prochazky-widget]").forEach(initInstance);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
