// Pick a fresh color scheme on every page load. Runs in <head> so the page
// never flashes the fallback colors.
(function () {
  var h = Math.floor(Math.random() * 360);        // button hue
  var b = (h + 150 + Math.floor(Math.random() * 60)) % 360; // bars: roughly opposite hue
  function hsl(hue, s, l) { return "hsl(" + hue + "," + s + "%," + l + "%)"; }
  var root = document.documentElement.style;
  root.setProperty("--btn", hsl(h, 38, 50));
  root.setProperty("--btn-light", hsl(h, 38, 80));
  root.setProperty("--btn-dark", hsl(h, 38, 28));
  root.setProperty("--btn-shadow", hsl(h, 38, 20));
  root.setProperty("--btn-hover", hsl(h, 38, 58));
  // Two neighboring shades, light enough for black text and blue links.
  root.setProperty("--bar1", hsl(b, 90, 72));
  root.setProperty("--bar2", hsl((b + 25) % 360, 90, 64));
  // Each hand-drawn symbol gets its own random color, dark enough to stand out.
  for (var i = 1; i <= 3; i++) {
    root.setProperty("--glyph" + i, hsl(Math.floor(Math.random() * 360), 70, 45));
  }
})();
