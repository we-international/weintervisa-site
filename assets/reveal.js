/* Open the <details> folds round the target of a #link, then scroll to it.
   Chrome does this by itself; older Safari and Firefox do not. Pages work without this file. */
(function () {
  function reveal(id, scroll) {
    var t = id && document.getElementById(decodeURIComponent(id));
    if (!t) return;
    for (var n = t; n; n = n.parentElement) if (n.tagName === "DETAILS") n.open = true;
    if (scroll) t.scrollIntoView({ block: "start" });
  }
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href^="#"]');
    if (a && a.getAttribute("href").length > 1) reveal(a.getAttribute("href").slice(1), false);
  });
  window.addEventListener("hashchange", function () { reveal(location.hash.slice(1), true); });
  if (location.hash) reveal(location.hash.slice(1), true);
})();
