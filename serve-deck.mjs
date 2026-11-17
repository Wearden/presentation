#!/usr/bin/env node
// Wearden deck: a presenter page that PLAYS the HyperFrames animation between stops
// (the stock slideshow only seeks, so no motion is visible). It reuses the files that
// `hyperframes present` serves on :3004, so start that first:
//   cd deck && npx hyperframes present . --no-open --port 3004
//   node serve-deck.mjs      ->  http://localhost:3010
import http from "node:http";
import fs from "node:fs";
const DECK = process.env.DECK || "deck";
const BG = process.env.BG || "#030605";
const CFG = JSON.parse(fs.readFileSync(new URL("./" + DECK + "/stops.json", import.meta.url)));

const UPSTREAM = process.env.UPSTREAM || "http://localhost:3004";
const PORT = Number(process.env.PORT || 3010);

const PAGE = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Wearden deck</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="/player.js"></script>
<style>
  html,body{margin:0;height:100%;background:${BG};overflow:hidden;font-family:Inter,system-ui,sans-serif}
  hyperframes-player{position:absolute;inset:0}
  #hud{position:fixed;right:18px;bottom:14px;display:flex;gap:10px;align-items:center;font:600 14px ui-monospace,monospace;color:#f3f6f4;opacity:.45;z-index:5;user-select:none}
  #hud b{display:inline-block;padding:4px 10px;border:1px solid #2a3a33;border-radius:999px;background:#08100d}
  #hint{position:fixed;left:18px;bottom:14px;font:500 13px system-ui;color:#9fb0a7;opacity:.0;transition:opacity .4s;z-index:5}
  body:hover #hint{opacity:.6}
  #start{position:fixed;inset:0;z-index:20;display:flex;align-items:center;justify-content:center;background:rgba(8,16,13,.55);backdrop-filter:blur(3px);cursor:pointer}
  #start span{padding:14px 26px;border-radius:999px;background:#f7faf8;color:#08100d;font:700 18px system-ui,sans-serif;box-shadow:0 10px 40px rgba(0,0,0,.35)}
</style></head>
<body>
<hyperframes-player id="p" src="/composition/index.html"></hyperframes-player>
<div id="hint">Space / → next · ← back · F fullscreen · Home / End</div>
<div id="start" role="button" tabindex="0"><span>Başlamaq üçün klik et · tam ekran</span></div>
<div id="hud"><b id="ctr">1 / 11</b></div>
<script>
  const STARTS = ${JSON.stringify(CFG.starts)};
  const STOPS = ${JSON.stringify(CFG.stops)};
  const p = document.getElementById("p"), ctr = document.getElementById("ctr");
  let k = 0, j = 0, target = null, ready = false, mode = "held";

  const label = () => (ctr.textContent = (k + 1) + " / " + STOPS.length);
  function holdAt(t) { p.pause(); p.seek(t); target = null; mode = "held"; label(); }
  function playTo(t) { target = t; mode = "playing"; label(); p.play(); }
  function enter(newK) { k = newK; j = 0; p.seek(STARTS[k]); playTo(STOPS[k][0]); }
  function next() {
    if (!ready) return;
    if (mode === "playing") return holdAt(target);          // skip the rest of the animation
    if (j + 1 < STOPS[k].length) { j++; playTo(STOPS[k][j]); }
    else if (k + 1 < STOPS.length) enter(k + 1);
  }
  function prev() {
    if (!ready) return;
    if (mode === "playing") { holdAt(target); return; }
    if (j > 0) { j--; holdAt(STOPS[k][j]); }
    else if (k > 0) { k--; j = STOPS[k].length - 1; holdAt(STOPS[k][j]); }
  }
  function goto(newK, last) { k = newK; j = last ? STOPS[k].length - 1 : 0; last ? holdAt(STOPS[k][j]) : enter(k); }

  function tick() {
    if (mode === "playing" && target != null && p.currentTime >= target - 0.02) holdAt(target);
    requestAnimationFrame(tick);
  }
  // The first click or key press goes full screen (browsers only allow that after a user action) and starts the deck.
  let started = false, entered = false;
  const go = () => { if (ready && started && !entered) { entered = true; enter(0); } };
  const begin = (e) => {
    e.preventDefault(); e.stopPropagation();
    started = true;
    document.getElementById("start")?.remove();
    const fs = document.documentElement.requestFullscreen?.();
    if (fs && fs.catch) fs.catch(() => {});
    go();
  };
  document.getElementById("start").addEventListener("click", begin);
  p.addEventListener("ready", () => { if (ready) return; ready = true; go(); });
  requestAnimationFrame(tick);
  setTimeout(() => { if (!ready && p.ready) { ready = true; go(); } }, 4000);

  addEventListener("keydown", (e) => {
    if (!started) { begin(e); return; }
    if (["ArrowRight", "ArrowDown", " ", "PageDown", "Enter"].includes(e.key)) { e.preventDefault(); next(); }
    else if (["ArrowLeft", "ArrowUp", "PageUp", "Backspace"].includes(e.key)) { e.preventDefault(); prev(); }
    else if (e.key === "Home") goto(0, false);
    else if (e.key === "End") goto(STOPS.length - 1, true);
    else if (e.key === "f" || e.key === "F") { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); }
  });
  addEventListener("click", (e) => { (e.clientX > innerWidth * 0.3) ? next() : prev(); });
  label();
</script></body></html>`;

// --export <dir>: write a static copy (GitHub Pages ready) instead of serving
const ei = process.argv.indexOf("--export");
if (ei > 0) {
  const dir = process.argv[ei + 1];
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(dir + "/index.html", PAGE.replace('src="/player.js"', 'src="player.js"').replace('src="/composition/index.html"', 'src="composition/index.html"'));
  const src = new URL("./" + DECK + "/", import.meta.url).pathname;
  fs.cpSync(src, dir + "/composition", { recursive: true, filter: (f) => !/\/(\.hyperframes|renders|node_modules)(\/|$)|\.png$/.test(f.slice(src.length - 1)) || /assets\/[^/]+\.png$/.test(f) });
  const r = await fetch(UPSTREAM + "/player.js");
  fs.writeFileSync(dir + "/player.js", Buffer.from(await r.arrayBuffer()));
  fs.writeFileSync(dir + "/.nojekyll", "");
  console.log("exported", DECK, "->", dir);
  process.exit(0);
}

http
  .createServer(async (req, res) => {
    try {
      if (req.url === "/" || req.url.startsWith("/?")) {
        res.writeHead(200, { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" });
        return res.end(PAGE);
      }
      const r = await fetch(UPSTREAM + req.url);
      res.writeHead(r.status, { "content-type": r.headers.get("content-type") || "application/octet-stream", "cache-control": "no-store" });
      res.end(Buffer.from(await r.arrayBuffer()));
    } catch (e) {
      res.writeHead(502); res.end("upstream error: " + e.message);
    }
  })
  .listen(PORT, () => console.log("Wearden deck: http://localhost:" + PORT + "  (upstream " + UPSTREAM + ")"));
