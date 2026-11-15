// The site's default look is dark. Browsers that visited an earlier version
// may have remembered the light look; forget that once so the dark default
// applies. Visitors can still switch with the sun/moon button, and that
// choice is remembered from then on.
(function () {
  var FLAG = "kb-theme-default-v2";
  try {
    if (localStorage.getItem(FLAG)) return;
    localStorage.setItem(FLAG, "1");
    var stale = [];
    for (var i = 0; i < localStorage.length; i++) {
      var key = localStorage.key(i);
      if (key && /__palette$/.test(key)) stale.push(key);
    }
    if (!stale.length) return;
    stale.forEach(function (key) { localStorage.removeItem(key); });
    if (document.body.getAttribute("data-md-color-scheme") !== "slate") location.reload();
  } catch (e) {}
})();
