#!/usr/bin/env python3
"""Wearden pitch deck v2 — dark cinematic theme, Higgsfield plates, HyperFrames motion.
Generates deck/compositions/*.html, deck/index.html and deck/stops.json (presenter stops)."""
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
THEME = os.environ.get("THEME", "dark")
OUT = os.path.join(ROOT, "deck" if THEME == "dark" else "deck-ag")
LIGHT = [
    ('rgba(239,68,68,.35),transparent 60%);opacity:0"></div></div><div class="scrimL"></div>', 'rgba(239,68,68,.35),transparent 60%);opacity:0"></div></div>'),
    (":root{--bg:#030605;--em:#10b981;--em2:#34d399;--em3:#a7f3d0;--emd:#047857;--red:#ef4444;--red2:#f87171;--tx:#f3f6f4;--mut:#9fb0a7;--line:rgba(255,255,255,.14);--glass:rgba(8,16,13,.62);",
     ":root{--bg:#f7faf8;--em:#10b981;--em2:#047857;--em3:#065f46;--emd:#059669;--red:#dc2626;--red2:#dc2626;--tx:#0a0f0d;--mut:#45544d;--line:rgba(10,15,13,.12);--glass:rgba(255,255,255,.82);"),
    ('<div class="platebox"><img id="plate" class="plate" src="assets/hf/problem.jpg"', '<div class="platebox" style="inset:auto;left:1090px;top:150px;width:770px;height:660px;border-radius:30px;box-shadow:0 40px 100px rgba(10,30,20,.28)"><img id="plate" class="plate" style="left:-830px;top:-230px" src="assets/hfx/problem.jpg"'),
    ("assets/hf/horizon.jpg", "assets/hfl/fibers.jpg"), ("assets/hf/soc.jpg", "assets/hfl/fibers.jpg"), ("assets/hf/", "assets/hfl/"), ("assets/hfx/", "assets/hf/"),
    ("#f3f6f4", "#0a0f0d"), ("#9fb0a7", "#45544d"), ("#7d8d85", "#55655d"), ("#6b7c74", "#55655d"), ("#c9d6cf", "#3b4a43"),
    ("#6ee7b7", "#047857"), ("#a7f3d0", "#047857"), ("#34d399", "#059669"), ("#f87171", "#dc2626"),
    ("rgba(255,255,255,.14)", "rgba(10,15,13,.12)"), ("rgba(255,255,255,.18)", "rgba(10,15,13,.18)"), ("rgba(255,255,255,.35)", "rgba(10,15,13,.35)"),
    ("rgba(255,255,255,.1)", "rgba(10,15,13,.09)"), ("rgba(255,255,255,.08)", "rgba(10,15,13,.08)"), ("rgba(255,255,255,.07)", "rgba(10,15,13,.06)"), ("rgba(255,255,255,.06)", "rgba(255,255,255,.7)"),
    ("rgba(243,246,244,.85)", "#1f2a25"), ("rgba(243,246,244,.75)", "rgba(10,15,13,.72)"), ("rgba(243,246,244,.55)", "rgba(10,15,13,.5)"),
    ("#e7ece9", "#1f2a25"), ("rgba(3,6,5,.6)", "rgba(255,255,255,.8)"), ("rgba(3,6,5,", "rgba(247,250,248,"), ("#030605", "#f7faf8"),
    ("rgba(8,16,13,.7)", "rgba(255,255,255,.88)"), ("#0d1412", "#eef1ef"),
    ("rgba(0,0,0,.45)", "rgba(10,30,20,.10)"), ("0 70px 160px rgba(0,0,0,.7)", "0 50px 120px rgba(10,30,20,.20)"),
    ("background:#000", "background:#0a0f0d"),
    ("#root{position:absolute;inset:0;overflow:hidden;background:var(--bg);", "#root{position:absolute;inset:0;overflow:hidden;background:#064e3b;"),
    ("radial-gradient(circle at 73% 46%,#d1fae5 0%,rgba(16,185,129,.6) 25%,transparent 60%)", "radial-gradient(circle at 73% 46%,#10b981 0%,rgba(16,185,129,.55) 30%,transparent 66%)"),
    ("opacity: 0.25 + r() * 0.55", "opacity: 0.12 + r() * 0.28"), ("--mut:#45544d", "--mut:#33413b"), ("#45544d", "#33413b"),
    (".ac-a{background:#1f2a25}", ".ac-a{background:#a9bdb3}"), ('stroke="#1f2a25" stroke-width="26"', 'stroke="#a9bdb3" stroke-width="26"'),
    ("rgba(239,68,68,.35),transparent 60%", "rgba(239,68,68,.12),transparent 60%"),
    (".hud .tr{", ".hud .tr{text-shadow:0 0 10px #fff,0 0 4px #fff;"), (".hud .tl{", ".hud .tl{text-shadow:0 0 10px #fff;"),
    ("background:var(--em2);box-shadow:0 0 12px 2px rgba(52,211,153,.6)", "background:#10b981;box-shadow:none"), ("box-shadow:0 0 12px 2px rgba(52,211,153,.6)", "box-shadow:0 0 10px 1px rgba(16,185,129,.45)"),
]


def themed(txt):
    if THEME == "dark":
        return txt
    for o, n in LIGHT:
        txt = txt.replace(o, n)
    return txt
os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)

# id, label, duration, intro, presenter stops (local seconds), notes
SCENES = [
    ("s01-hero", "Giriş", 9, "zoom", [5.4], "Wearden: agent-based security hardening for Linux and Windows. Scan, harden, roll back."),
    ("s02-problem", "Problem", 10, "shutter", [8.6], "Real scan of a fresh Ubuntu 24.04 host against a curated CIS Top 100: 12 of 100 checks fail. Manual hardening is slow and risky (lockout), so it rarely gets done."),
    ("s03-solution", "Həll", 10, "wipe", [8.4], "Agent scans read-only, core scores, AI ranks every failure, one-click hardening, every change reversible."),
    ("s04-dashboard", "Panel", 12, "zoom", [3.6, 5.6, 7.6, 10.6], "Live dashboard: 89.5% average compliance, AI analysis (1 to fix, 11 to review), compliance trend."),
    ("s05-scan", "Skan", 11, "shutter", [4.4, 6.6, 9.6], "One scan: 100 checks, 88 pass, 12 fail. AI decides fix / review / accept and ranks SSH root login first."),
    ("s06-rollback", "Geri qaytarma", 12, "iris", [3.2, 10.6], "Every change is backed up first and re-checked afterwards. Roll back one control, a selection or a whole run."),
    ("s07-attack", "ATT&CK", 10, "zoom", [8.4], "ATT&CK coverage rises from 36 to 39 of 53 mapped techniques after hardening."),
    ("s08-users", "İstifadəçilər", 9, "wipe", [7.6], "SMB IT teams, universities and public sector, MSSPs and pentesters. Ubuntu 22.04/24.04, Windows 10/11/Server 2022."),
    ("s09-impact", "Təsir", 9, "shutter", [7.6], "Hours of manual CIS work become one reversible click. Proposed model: per-host SaaS, on-prem license, MSSP partners."),
    ("s10-market", "Bazar", 10, "wipe", [8.6], "SPM market $26.6B (2025) to $53.3B (2030), 14.9% CAGR (MarketsandMarkets). Azerbaijan: cyber-incident losses expected to reach 40m AZN (report.az). Go-to-market: OYU pilot, Azerbaijani SMEs and banks, then MSSPs across the region."),
    ("s11-compete", "Rəqabət", 11, "shutter", [9.6], "CalCom CHS hardens and rolls back but is enterprise, quote-only. CIS-CAT Pro and Nessus Pro only assess (Nessus Pro $4,790/yr). Wazuh SCA and OpenSCAP are free but fixes are manual and OpenSCAP remediation cannot be reverted automatically (Red Hat)."),
    ("s12-revenue", "Gəlir modeli", 11, "iris", [9.6], "Indicative pricing: free Community tier up to 5 hosts, Pro at $4 per host per month, Enterprise annual on-prem licence. 50 hosts = $2,400/yr vs Nessus Pro $4,790/yr for scanning only."),
    ("s13-future", "Gələcək", 9, "zoom", [7.6], "Next: runtime validation on real fleets, more benchmarks, health-checked auto-rollback."),
    ("s14-close", "Təşəkkür", 9, "zoom", [6.4], "Hər hostu gücləndir. Hər dəyişikliyi idarə et. Questions?"),
]
N = len(SCENES)

CSS = r"""
:root{--bg:#030605;--em:#10b981;--em2:#34d399;--em3:#a7f3d0;--emd:#047857;--red:#ef4444;--red2:#f87171;--tx:#f3f6f4;--mut:#9fb0a7;--line:rgba(255,255,255,.14);--glass:rgba(8,16,13,.62);--font:"Inter",sans-serif;--mono:"JetBrains Mono",monospace}
*{margin:0;padding:0;box-sizing:border-box}
#root{position:absolute;inset:0;overflow:hidden;background:var(--bg);color:var(--tx);font-family:var(--font)}
.abs{position:absolute}
#stage{position:absolute;inset:0;overflow:hidden;background:var(--bg)}
.platebox{position:absolute;inset:0;overflow:hidden}
.plate{position:absolute;left:-96px;top:-54px;width:2112px;height:1188px;object-fit:cover}
.scrimL{position:absolute;inset:0;background:linear-gradient(90deg,rgba(3,6,5,.94) 0%,rgba(3,6,5,.72) 34%,rgba(3,6,5,.12) 66%,rgba(3,6,5,0) 100%)}
.scrimB{position:absolute;inset:0;background:linear-gradient(0deg,rgba(3,6,5,.95) 0%,rgba(3,6,5,.55) 34%,rgba(3,6,5,0) 62%)}
.scrimT{position:absolute;inset:0;background:linear-gradient(180deg,rgba(3,6,5,.85) 0%,rgba(3,6,5,.2) 40%,rgba(3,6,5,0) 60%)}
.scrimC{position:absolute;inset:0;background:radial-gradient(ellipse 60% 55% at 50% 52%,rgba(3,6,5,.82) 0%,rgba(3,6,5,.35) 60%,rgba(3,6,5,.1) 100%)}
.dim{position:absolute;inset:0;background:rgba(3,6,5,.55)}
.parts{position:absolute;inset:0;overflow:hidden}
.part{position:absolute;border-radius:50%;background:var(--em2);box-shadow:0 0 12px 2px rgba(52,211,153,.6);opacity:0}
.eyebrow{display:flex;align-items:center;gap:18px;font-family:var(--mono);font-size:26px;font-weight:700;letter-spacing:.26em;text-transform:uppercase;color:var(--em2)}
.eyebrow i{display:block;width:56px;height:2px;background:currentColor;transform-origin:0 50%}
.ln{display:block;overflow:hidden;padding:0 .02em .1em 0;margin-bottom:-.1em}
.ln>span{display:inline-block}
h1{font-weight:900;letter-spacing:-.05em;line-height:.92}
h2{font-weight:700;font-size:92px;letter-spacing:-.045em;line-height:1.02}
.em{color:var(--em2)}
.red{color:var(--red2)}
.sub{font-size:34px;line-height:1.35;color:var(--mut);font-weight:400}
.glass{position:absolute;background:var(--glass);border:1px solid var(--line);border-radius:28px;box-shadow:0 30px 80px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.06);backdrop-filter:blur(14px)}
.chip{display:inline-flex;align-items:center;gap:14px;padding:14px 24px;border-radius:999px;border:1px solid var(--line);background:rgba(8,16,13,.7);font-size:28px;font-weight:600;color:var(--tx);white-space:nowrap}
.chip b{width:12px;height:12px;border-radius:50%;background:var(--em);box-shadow:0 0 12px var(--em);display:block}
.mono{font-family:var(--mono)}
.ico{width:64px;height:64px;overflow:visible}
.ico path{fill:none;stroke:var(--em2);stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
/* HUD */
.hud{position:absolute;inset:0;pointer-events:none;z-index:40}
.hud .tl{position:absolute;left:96px;top:54px;display:flex;align-items:center;gap:16px;font-family:var(--mono);font-size:22px;letter-spacing:.2em;color:rgba(243,246,244,.75)}
.hud .tl svg{width:20px;height:26px}
.hud .tl em{font-style:normal;color:var(--em2)}
.hud .tr{position:absolute;right:96px;top:54px;font-family:var(--mono);font-size:22px;letter-spacing:.2em;color:rgba(243,246,244,.55)}
.hud .prog{position:absolute;left:96px;right:96px;bottom:46px;height:3px;background:rgba(255,255,255,.1);border-radius:2px;overflow:hidden}
.hud .prog b{position:absolute;inset:0;background:linear-gradient(90deg,var(--emd),var(--em2));transform-origin:0 50%;box-shadow:0 0 14px var(--em)}
/* transitions */
#fl-line{position:absolute;left:0;top:539px;width:1920px;height:3px;background:var(--em2);box-shadow:0 0 30px 8px rgba(16,185,129,.7);transform-origin:50% 50%;opacity:0;z-index:50}
#fl-bar{position:absolute;left:-4px;top:0;width:8px;height:1080px;background:var(--em2);box-shadow:0 0 50px 16px rgba(16,185,129,.65);opacity:0;z-index:50}
#fl-ring{position:absolute;left:660px;top:240px;width:600px;height:600px;border-radius:50%;border:4px solid var(--em2);box-shadow:0 0 60px 10px rgba(16,185,129,.5),inset 0 0 60px 10px rgba(16,185,129,.4);opacity:0;z-index:50}
/* browser */
.persp{position:absolute;inset:0;perspective:2400px}
.frame{position:absolute;overflow:hidden;border-radius:18px;background:#0d1412;box-shadow:0 70px 160px rgba(0,0,0,.7),0 0 0 1px rgba(255,255,255,.1),0 0 140px rgba(16,185,129,.22)}
.bar{position:absolute;left:0;top:0;right:0;height:46px;background:#0d1412;display:flex;align-items:center;gap:10px;padding:0 18px;border-bottom:1px solid rgba(255,255,255,.08)}
.bar i{width:13px;height:13px;border-radius:50%;display:block}
.addr{margin-left:20px;width:520px;height:30px;border-radius:15px;background:rgba(255,255,255,.07);font-family:var(--mono);font-size:17px;color:#c9d6cf;display:flex;align-items:center;gap:10px;padding:0 16px;white-space:nowrap;overflow:hidden}
.addr svg{width:14px;height:14px;flex:none}
.load{position:absolute;left:0;bottom:-1px;height:3px;width:100%;background:var(--em2);transform-origin:0 50%;box-shadow:0 0 10px var(--em)}
.screen{position:absolute;left:0;right:0;top:46px;bottom:0;overflow:hidden;background:#fafafa}
.skel{position:absolute;inset:0;background:#fafafa}
.skel div{position:absolute;background:#ececec;border-radius:12px}
.cam{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0}
.cam img.shot{position:absolute;left:0;top:0;width:1920px;height:1080px;display:block}
.hl{position:absolute;border:5px solid var(--em);border-radius:16px;box-shadow:0 0 0 10px rgba(16,185,129,.18),0 0 60px rgba(16,185,129,.45)}
.cur{position:absolute;left:0;top:0;width:46px;height:46px;z-index:9}
.ring{position:absolute;left:0;top:0;width:100px;height:100px;margin:-50px 0 0 -50px;border:5px solid var(--em);border-radius:50%;opacity:0;z-index:8}
.call{display:flex;gap:20px;align-items:flex-start;padding:22px 0;border-top:1px solid var(--line)}
.call .n{font-family:var(--mono);font-size:24px;color:var(--em2);padding-top:6px;flex:none}
.call .t{font-size:32px;line-height:1.25;font-weight:600}
.call .t small{display:block;font-size:24px;font-weight:400;color:var(--mut);margin-top:4px}
"""

COMMON_JS = r"""
const tl = gsap.timeline({ paused: true });
const D = __D__;
function lines(sel, t, st = 0.1, dur = 1.1) {
  tl.fromTo(sel + " .ln > span", { yPercent: 112, rotate: 2.5 }, { yPercent: 0, rotate: 0, duration: dur, ease: "expo.out", stagger: st }, t);
}
function rise(sel, t, dur = 0.9, dy = 40) {
  tl.fromTo(sel, { opacity: 0, y: dy }, { opacity: 1, y: 0, duration: dur, ease: "expo.out" }, t);
}
function blurIn(sel, t, dur = 1.0, st = 0) {
  tl.fromTo(sel, { opacity: 0, filter: "blur(16px)", y: 18 }, { opacity: 1, filter: "blur(0px)", y: 0, duration: dur, ease: "power3.out", stagger: st }, t);
}
function eyebrow(sel, t) {
  tl.fromTo(sel + " i", { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "expo.out" }, t);
  tl.fromTo(sel + " span", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 1.1, ease: "expo.out" }, t + 0.1);
}
function kb(from, to, sel = "#plate") { tl.fromTo(sel, from, Object.assign({ duration: D, ease: "none" }, to), 0); }
function outro(t = D - 0.75) {
  tl.to("#stage", { scale: 1.07, opacity: 0, filter: "blur(14px)", duration: 0.7, ease: "power2.in" }, t);
}
function hud(i, n) {
  tl.fromTo(".hud .tl, .hud .tr", { opacity: 0, y: -12 }, { opacity: 1, y: 0, duration: 0.9, ease: "expo.out", stagger: 0.1 }, 0.5);
  tl.fromTo(".hud .prog b", { scaleX: (i - 1) / n }, { scaleX: i / n, duration: 1.4, ease: "expo.inOut" }, 0.6);
}
function count(sel, to, t, dur, o = {}) {
  const el = document.querySelector(sel), obj = { v: o.from || 0 }, dec = o.dec || 0, pre = o.pre || "", suf = o.suf || "";
  el.textContent = pre + (o.from || 0).toFixed(dec) + suf;
  tl.fromTo(obj, { v: o.from || 0 }, { v: to, duration: dur, ease: o.ease || "power3.out", onUpdate: () => (el.textContent = pre + obj.v.toFixed(dec) + suf) }, t);
}
function typeText(sel, t, dur) {
  const el = document.querySelector(sel), full = el.textContent, o = { n: 0 };
  el.textContent = "";
  tl.fromTo(o, { n: 0 }, { n: full.length, duration: dur, ease: "none", onUpdate: () => (el.textContent = full.slice(0, Math.round(o.n))) }, t);
}
function draw(sel, t, dur = 1, ease = "power2.inOut") { tl.fromTo(sel, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: dur, ease }, t); }
function seeded(seed) { return () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function particles(n, seed, color) {
  const host = document.querySelector("#parts"), r = seeded(seed);
  for (let i = 0; i < n; i++) {
    const p = document.createElement("div"); p.className = "part";
    const sz = 3 + r() * 6; p.style.width = p.style.height = sz + "px";
    if (color) { p.style.background = color; p.style.boxShadow = "0 0 12px 2px " + color; }
    p.style.left = r() * 1920 + "px"; p.style.top = 300 + r() * 900 + "px"; host.appendChild(p);
    const dly = r() * 2.5, dur = D - dly;
    tl.fromTo(p, { y: 0, x: 0 }, { y: -(260 + r() * 420), x: (r() - 0.5) * 160, duration: dur, ease: "none" }, dly);
    tl.fromTo(p, { opacity: 0 }, { opacity: 0.25 + r() * 0.55, duration: 1.2, ease: "power1.out" }, dly);
  }
}
// camera inside a browser screen of size fw x fh, looking at screenshot coords (cx, cy)
function camAt(fw, fh, cx, cy, zoom) {
  const s = (fw / 1920) * zoom;
  let x = fw / 2 - cx * s, y = fh / 2 - cy * s;
  x = Math.min(0, Math.max(fw - 1920 * s, x)); y = Math.min(0, Math.max(fh - 1080 * s, y));
  return { x, y, scale: s };
}
function cam(sel, fw, fh, cx, cy, zoom, t, dur = 1.4) { tl.to(sel, Object.assign(camAt(fw, fh, cx, cy, zoom), { duration: dur, ease: "power3.inOut" }), t); }
function hl(sel, t) {
  tl.fromTo(sel, { opacity: 0, scale: 1.12 }, { opacity: 1, scale: 1, duration: 0.6, ease: "expo.out" }, t);
}
function hlOff(sel, t) { tl.to(sel, { opacity: 0, duration: 0.35 }, t); }
function move(sel, x, y, t, dur = 0.9) { tl.to(sel, { x, y, duration: dur, ease: "power3.inOut" }, t); }
function click(cur, ring, x, y, t, d = 0.6) {
  tl.to(cur, { scale: 0.82, duration: 0.09, yoyo: true, repeat: 1, ease: "power1.inOut" }, t);
  tl.set(ring, { x, y }, t);
  tl.fromTo(ring, { scale: 0.2, opacity: 1 }, { scale: 1.6, opacity: 0, duration: d, ease: "power2.out" }, t);
}
"""

LOGO_PATH = "M0 0H100V83H200V0H300V83H400V0H500V183H0ZM50 233H450V658H50Z"
CURSOR = '<svg viewBox="0 0 24 24"><path d="M3 2l7 18 2.6-7.4L20 10z" fill="#fff" stroke="#0a0a0a" stroke-width="1.5" stroke-linejoin="round"/></svg>'
LOCK = '<svg viewBox="0 0 24 24"><path d="M6 11h12v9H6zM8.5 11V8a3.5 3.5 0 0 1 7 0v3" fill="none" stroke="#34d399" stroke-width="2.2"/></svg>'


def hud_html(i, label):
    return f"""
<div class="hud">
  <div class="tl"><svg viewBox="0 0 500 658"><path d="{LOGO_PATH}" fill="#f3f6f4"/></svg>WEARDEN <em>{i:02d} / {N:02d}</em> {label.replace("i", "İ").replace("ı", "I").upper()}</div>
  <div class="tr">OYU CYBERAI HACKATHON 2026</div>
  <div class="prog"><b></b></div>
</div>"""


def plate(img, scrims="scrimL", extra=""):
    sc = "".join(f'<div class="{s}"></div>' for s in scrims.split())
    return f'<div class="platebox"><img id="plate" class="plate" src="assets/hf/{img}" alt="" />{extra}</div>{sc}<div id="parts" class="parts"></div>'


def browser(prefix, img, url, left, top, fw, overlays="", skel=True):
    fh = round(fw * 1080 / 1920)
    sk = ""
    if skel:
        sk = f"""<div id="{prefix}-skel" class="skel"><div style="left:0;top:0;width:{round(fw*.125)}px;height:100%;border-radius:0;background:#f1f1f1"></div>
<div style="left:{round(fw*.21)}px;top:{round(fh*.09)}px;width:{round(fw*.18)}px;height:{round(fh*.05)}px"></div>
<div style="left:{round(fw*.21)}px;top:{round(fh*.15)}px;width:{round(fw*.7)}px;height:{round(fh*.15)}px"></div>
<div style="left:{round(fw*.21)}px;top:{round(fh*.34)}px;width:{round(fw*.7)}px;height:{round(fh*.14)}px"></div>
<div style="left:{round(fw*.21)}px;top:{round(fh*.52)}px;width:{round(fw*.46)}px;height:{round(fh*.3)}px"></div>
<div style="left:{round(fw*.69)}px;top:{round(fh*.52)}px;width:{round(fw*.22)}px;height:{round(fh*.3)}px"></div></div>"""
    return f"""
<div class="persp"><div id="{prefix}-frame" class="frame" style="left:{left}px;top:{top}px;width:{fw}px;height:{fh+46}px">
  <div class="bar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i>
    <span class="addr">{LOCK}<span id="{prefix}-url">{url}</span></span><div id="{prefix}-load" class="load"></div></div>
  <div class="screen"><div id="{prefix}-cam" class="cam"><img id="{prefix}-shot" class="shot" src="assets/{img}" alt="" />{overlays}
    <div id="{prefix}-cur" class="cur">{CURSOR}</div><div id="{prefix}-ring" class="ring"></div></div>{sk}</div>
</div></div>""", fh


def browser_open_js(prefix, fw, fh, t, from_side=1):
    return f"""
tl.set("#{prefix}-cam", camAt({fw}, {fh}, 960, 540, 1), 0);
tl.set("#{prefix}-cur", {{ x: 1500, y: 1200 }}, 0);
tl.fromTo("#{prefix}-frame", {{ opacity: 0, x: {380*from_side}, y: 120, z: -500, rotateY: {-34*from_side}, rotateX: 16 }}, {{ opacity: 1, x: 0, y: 0, z: 0, rotateY: 0, rotateX: 0, duration: 1.6, ease: "expo.out" }}, {t});
typeText("#{prefix}-url", {t+0.5}, 0.8);
tl.fromTo("#{prefix}-load", {{ scaleX: 0, opacity: 1 }}, {{ scaleX: 1, duration: 0.8, ease: "power2.inOut" }}, {t+1.2});
tl.to("#{prefix}-load", {{ opacity: 0, duration: 0.3 }}, {t+2.0});
tl.to("#{prefix}-skel", {{ opacity: 0, duration: 0.5 }}, {t+1.9});
tl.fromTo("#{prefix}-shot", {{ clipPath: "inset(0% 0% 100% 0%)", opacity: 0.4 }}, {{ clipPath: "inset(0% 0% 0% 0%)", opacity: 1, duration: 0.9, ease: "power3.out" }}, {t+1.8});
"""


def icon(d, id_=""):
    paths = "".join(f'<path pathLength="1" stroke-dasharray="1" d="{p}"/>' for p in d.split("|"))
    return f'<svg {f"id={chr(34)}{id_}{chr(34)}" if id_ else ""} class="ico" viewBox="0 0 24 24">{paths}</svg>'


ICONS = {
    "scan": "M11 4a7 7 0 1 1 0 14a7 7 0 1 1 0-14z|M16.5 16.5L21 21",
    "ai": "M12 3l2.2 5.8L20 11l-5.8 2.2L12 19l-2.2-5.8L4 11l5.8-2.2z",
    "shield": "M12 3l8 3v6c0 4.5-3.4 8.2-8 9c-4.6-.8-8-4.5-8-9V6z|M8.5 12l2.5 2.5L16 9.5",
    "undo": "M4 4v6h6|M4.6 10A8 8 0 1 1 6.3 17.7",
    "building": "M4 21V5h10v16|M14 9h6v12|M7 9h4|M7 13h4|M7 17h4",
    "uni": "M3 9l9-5 9 5-9 5z|M6 11v5c3 2 9 2 12 0v-5",
    "term": "M3 5h18v14H3z|M7 10l3 2-3 2|M12 15h5",
}

S = {}

# ============================================================ 01 HERO
S["s01-hero"] = (
    plate("hero.jpg", "scrimL scrimB", '<div id="h-scan" class="abs" style="left:1240px;top:0;width:700px;height:4px;background:linear-gradient(90deg,transparent,#6ee7b7,transparent);box-shadow:0 0 40px 10px rgba(16,185,129,.55);opacity:0"></div>')
    + f"""
<div id="h-bars"><div id="h-bt" class="abs" style="left:0;top:0;width:1920px;height:150px;background:#000;z-index:30"></div><div id="h-bb" class="abs" style="left:0;bottom:0;width:1920px;height:150px;background:#000;z-index:30"></div></div>
<div class="abs" style="left:150px;top:200px;width:1500px">
  <div id="h-eye" class="eyebrow"><i></i><span>OYU CyberAI Hackathon 2026</span></div>
  <div style="display:flex;align-items:flex-end;gap:40px;margin-top:40px">
    <svg id="h-logo" viewBox="-10 -10 520 678" style="width:150px;height:197px;flex:none;overflow:visible"><path id="h-lp" pathLength="1" stroke-dasharray="1" d="{LOGO_PATH}" fill="#f3f6f4" fill-opacity="0" stroke="#34d399" stroke-width="10"/></svg>
    <h1 id="h-title" style="font-size:236px;white-space:nowrap"><span class="ln">{''.join(f'<span>{c}</span>' for c in 'Wearden')}</span></h1>
  </div>
  <div id="h-tag" style="margin-top:46px;font-size:76px;font-weight:700;letter-spacing:-.035em;line-height:1.05">
    <span class="ln"><span>Skan et.</span> <span>Gücləndir.</span> <span class="em">Geri qaytar.</span></span>
  </div>
  <p id="h-sub" class="sub" style="margin-top:30px;width:900px;font-size:38px">Linux və Windows üçün agent əsaslı təhlükəsizlik gücləndirmə platforması: hər dəyişiklik geri qaytarıla bilər.</p>
  <div id="h-chips" style="display:flex;gap:16px;margin-top:52px">
    <span class="chip"><b></b>CIS standartları</span><span class="chip"><b></b>AI ilə prioritetləşdirmə</span><span class="chip"><b></b>MITRE ATT&amp;CK</span>
  </div>
</div>""",
    r"""
kb({ scale: 1.16, x: 70, y: 24, opacity: 0 }, { scale: 1.0, x: -30, y: 0, opacity: 1 });
tl.fromTo("#h-bt", { yPercent: 0 }, { yPercent: -100, duration: 1.6, ease: "expo.inOut" }, 0.2);
tl.fromTo("#h-bb", { yPercent: 0 }, { yPercent: 100, duration: 1.6, ease: "expo.inOut" }, 0.2);
particles(34, 7);
eyebrow("#h-eye", 0.7);
draw("#h-lp", 0.7, 1.3, "power2.inOut");
tl.fromTo("#h-lp", { fillOpacity: 0 }, { fillOpacity: 1, duration: 0.6, ease: "power2.out" }, 1.8);
tl.fromTo("#h-title .ln > span", { yPercent: 115, rotateX: -70, opacity: 0 }, { yPercent: 0, rotateX: 0, opacity: 1, duration: 1.2, ease: "expo.out", stagger: 0.07 }, 1.0);
tl.fromTo("#h-tag .ln > span", { yPercent: 115 }, { yPercent: 0, duration: 1.0, ease: "expo.out", stagger: 0.18 }, 2.1);
blurIn("#h-sub", 2.9, 1.0);
blurIn("#h-chips .chip", 3.4, 0.8, 0.14);
tl.fromTo("#h-scan", { y: 80, opacity: 0 }, { y: 1000, opacity: 1, duration: 2.2, ease: "power1.inOut" }, 2.0);
tl.to("#h-scan", { opacity: 0, duration: 0.4 }, 4.3);
outro();
"""
)

# ============================================================ 02 PROBLEM
S["s02-problem"] = (
    plate("problem.jpg", "scrimL", '<div id="p-alarm" class="abs" style="left:900px;top:0;width:1100px;height:1080px;background:radial-gradient(ellipse at 70% 45%,rgba(239,68,68,.35),transparent 60%);opacity:0"></div>')
    + """
<div class="abs" style="left:96px;top:170px;width:1000px">
  <div id="p-eye" class="eyebrow" style="color:#f87171"><i></i><span>01 · Problem</span></div>
  <h2 id="p-h" style="margin-top:30px;font-size:100px"><span class="ln"><span>Yeni server</span></span><span class="ln"><span>hələ <span class="red">təhlükəsiz</span> deyil.</span></span></h2>
  <div style="display:flex;align-items:flex-end;gap:28px;margin-top:44px">
    <div id="p-num" style="font-size:230px;font-weight:900;letter-spacing:-.06em;line-height:.8;color:#f87171;text-shadow:0 0 60px rgba(239,68,68,.55)">0</div>
    <div id="p-cap" style="padding-bottom:6px"><div style="font-size:46px;font-weight:700">/ 100 CIS yoxlaması keçmir</div><div class="sub" style="font-size:30px">tamamilə yeni Ubuntu 24.04 quraşdırmasında</div></div>
  </div>
  <div id="p-src" class="mono" style="margin-top:20px;font-size:22px;color:#7d8d85;letter-spacing:.06em">REAL SKAN · CIS UBUNTU 24.04 LEVEL 1 · SEÇİLMİŞ TOP 100</div>
</div>
<div class="abs" style="left:1180px;top:250px;width:650px">
  <div id="p-f1" class="glass" style="position:relative;padding:24px 30px;margin-bottom:20px;border-color:rgba(239,68,68,.45)"><div class="mono red" style="font-size:22px">LNX-SSH-007 · KRİTİK</div><div style="font-size:32px;font-weight:600;margin-top:6px">SSH ilə root girişi açıqdır</div></div>
  <div id="p-f2" class="glass" style="position:relative;padding:24px 30px;margin-bottom:20px;border-color:rgba(239,68,68,.45)"><div class="mono red" style="font-size:22px">LNX-FW-001 · YÜKSƏK</div><div style="font-size:32px;font-weight:600;margin-top:6px">Host firewall quraşdırılmayıb</div></div>
  <div id="p-f3" class="glass" style="position:relative;padding:24px 30px;border-color:rgba(239,68,68,.45)"><div class="mono red" style="font-size:22px">LNX-PKG-004 · YÜKSƏK</div><div style="font-size:32px;font-weight:600;margin-top:6px">Paketlər şifrəsiz HTTP ilə yüklənir</div></div>
</div>
<div id="p-bot" class="glass" style="left:96px;top:830px;width:1728px;padding:30px 40px;display:flex;align-items:center;gap:30px">
  <div style="width:12px;height:64px;border-radius:6px;background:#f87171;flex:none;box-shadow:0 0 20px rgba(239,68,68,.7)"></div>
  <div style="font-size:38px;font-weight:600;line-height:1.25">Əl ilə gücləndirmə saatlar çəkir, bir səhv ayar isə sizi sistemdən kənarda qoya bilər. <span class="red">Ona görə də çox vaxt edilmir.</span></div>
</div>""",
    r"""
kb({ scale: 1.0, x: 0 }, { scale: 1.2, x: -60 });
tl.fromTo("#p-alarm", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.inOut", yoyo: true, repeat: 7 }, 1.6);
particles(18, 21, "#f87171");
eyebrow("#p-eye", 0.6);
lines("#p-h", 0.8, 0.14);
count("#p-num", 12, 1.6, 2.2, { ease: "power2.inOut" });
tl.fromTo("#p-num", { x: 0 }, { keyframes: [{ x: -8, duration: 0.04 }, { x: 7, duration: 0.04 }, { x: -4, duration: 0.04 }, { x: 0, duration: 0.05 }] }, 3.8);
blurIn("#p-cap", 1.9, 0.9);
blurIn("#p-src", 2.4, 0.9);
["#p-f1", "#p-f2", "#p-f3"].forEach((s, i) => {
  tl.fromTo(s, { opacity: 0, x: 120, rotateY: -25 }, { opacity: 1, x: 0, rotateY: 0, duration: 1.0, ease: "expo.out" }, 3.6 + i * 0.4);
  tl.fromTo(s, { boxShadow: "0 0 0 0 rgba(239,68,68,.7)" }, { boxShadow: "0 0 0 18px rgba(239,68,68,0)", duration: 0.8, ease: "power2.out" }, 3.8 + i * 0.4);
});
tl.fromTo("#p-bot", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 1.0, ease: "expo.out" }, 5.6);
outro();
"""
)

# ============================================================ 03 SOLUTION
STEPS = [
    ("01", "Skan", "Hər host üçün 100 CIS nəzarəti, standart olaraq yalnız oxuma", "scan"),
    ("02", "Prioritet", "AI hər uğursuzluğu risk və kilidlənmə təhlükəsinə görə sıralayır", "ai"),
    ("03", "Gücləndir", "Bir kliklə düzəliş, tətbiqdən əvvəl ehtiyat nüsxə", "shield"),
    ("04", "Geri qaytar", "Bir nəzarəti, seçimi və ya bütün işi geri qaytarın", "undo"),
]
cards = ""
for k, (n, t, d, ic) in enumerate(STEPS):
    x = 96 + k * 440
    cards += f"""<div id="sol-c{k}" class="glass" style="left:{x}px;top:640px;width:408px;height:310px;padding:34px 34px">
  <div style="display:flex;justify-content:space-between;align-items:flex-start">{icon(ICONS[ic], f"sol-i{k}")}<span class="mono" style="font-size:24px;color:#7d8d85">{n}</span></div>
  <div style="font-size:44px;font-weight:700;letter-spacing:-.02em;margin-top:26px">{t}</div>
  <div class="sub" style="font-size:27px;margin-top:10px;line-height:1.3">{d}</div>
  <div id="sol-g{k}" class="abs" style="inset:-1px;border-radius:28px;border:2px solid #34d399;box-shadow:0 0 50px rgba(16,185,129,.45),inset 0 0 40px rgba(16,185,129,.12);opacity:0"></div>
</div>"""
S["s03-solution"] = (
    plate("layers.jpg", "scrimL scrimB")
    + f"""
<div class="abs" style="left:96px;top:170px;width:1200px">
  <div id="sol-eye" class="eyebrow"><i></i><span>02 · Həll</span></div>
  <h2 id="sol-h" style="margin-top:30px;font-size:100px"><span class="ln"><span>Tap. Düzəlt.</span></span><span class="ln"><span class="em">Lazım olsa, geri qaytar.</span></span></h2>
  <p id="sol-sub" class="sub" style="margin-top:28px;width:1000px">Yüngül Go agenti hər hostu yoxlayır, core onu qiymətləndirir, AI isə əvvəlcə nəyi düzəltməli olduğunuzu deyir.</p>
</div>
<svg class="abs" style="left:0;top:0" width="1920" height="1080"><path id="sol-line" pathLength="1" stroke-dasharray="1" d="M300 616 H1620" stroke="#34d399" stroke-width="2" fill="none" opacity=".6"/></svg>
<div id="sol-dot" class="abs" style="left:290px;top:606px;width:20px;height:20px;border-radius:50%;background:#a7f3d0;box-shadow:0 0 24px 8px rgba(16,185,129,.8);opacity:0"></div>
{cards}""",
    r"""
kb({ scale: 1.1, x: 40 }, { scale: 1.16, x: -90 });
particles(26, 33);
eyebrow("#sol-eye", 0.7);
lines("#sol-h", 0.9, 0.16);
blurIn("#sol-sub", 1.6, 1.0);
[0, 1, 2, 3].forEach((k) => {
  tl.fromTo("#sol-c" + k, { opacity: 0, y: 80, rotateX: -30 }, { opacity: 1, y: 0, rotateX: 0, duration: 1.1, ease: "expo.out" }, 2.0 + k * 0.15);
});
draw("#sol-line", 3.0, 3.6, "none");
tl.fromTo("#sol-dot", { x: 0, opacity: 0 }, { x: 1320, opacity: 1, duration: 3.6, ease: "none" }, 3.0);
tl.to("#sol-dot", { opacity: 0, duration: 0.3 }, 6.6);
[0, 1, 2, 3].forEach((k) => {
  const t = 3.0 + k * 1.1;
  tl.fromTo("#sol-i" + k + " path", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.8, ease: "power2.out" }, t);
  tl.fromTo("#sol-g" + k, { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "power2.out" }, t);
  tl.to("#sol-g" + k, { opacity: 0.35, duration: 0.6, ease: "power2.inOut" }, t + 0.6);
  tl.fromTo("#sol-c" + k, { y: 0 }, { y: -14, duration: 0.3, ease: "power2.out", yoyo: true, repeat: 1 }, t);
});
outro();
"""
)

# ============================================================ 04 DASHBOARD (site opens)
FW4 = 1240
ov4 = """<div id="d-h1" class="hl" style="left:1080px;top:150px;width:690px;height:186px;opacity:0"></div>
<div id="d-h2" class="hl" style="left:396px;top:344px;width:1368px;height:180px;opacity:0"></div>
<div id="d-h3" class="hl" style="left:1308px;top:532px;width:456px;height:348px;opacity:0"></div>"""
b4, FH4 = browser("d", "shot-dashboard.png", "wearden.local/dashboard", 590, 196, FW4, ov4)
S["s04-dashboard"] = (
    plate("fibers.jpg", "dim")
    + f"""
<div class="abs" style="left:96px;top:170px;width:440px">
  <div id="d-eye" class="eyebrow"><i></i><span>03 · Məhsul</span></div>
  <h2 id="d-h" style="margin-top:28px;font-size:66px"><span class="ln"><span>Bütün hostlar</span></span><span class="ln"><span class="em">bir ekranda.</span></span></h2>
  <div style="margin-top:44px">
    <div id="d-c1" class="call"><span class="n">01</span><div class="t">89.5% orta uyğunluq<small>Hostlar, status və kritik uğursuzluqlar</small></div></div>
    <div id="d-c2" class="call"><span class="n">02</span><div class="t">Hər skanda AI analizi<small>1 düzəliş, 11 baxış, 0 qəbul</small></div></div>
    <div id="d-c3" class="call"><span class="n">03</span><div class="t">88% keçir, canlı<small>Hər standart üzrə son skan nəticələri</small></div></div>
  </div>
</div>
{b4}""",
    browser_open_js("d", FW4, FH4, 0.5)
    + f"""
eyebrow("#d-eye", 0.6);
lines("#d-h", 0.8, 0.14);
kb({{ scale: 1.05, x: 0 }}, {{ scale: 1.15, x: -60 }});
particles(16, 44);
// callouts are dim until their beat
["#d-c1", "#d-c2", "#d-c3"].forEach((s, i) => tl.fromTo(s, {{ opacity: 0, x: -30 }}, {{ opacity: 0.38, x: 0, duration: 0.8, ease: "expo.out" }}, 1.4 + i * 0.12));
const W = {FW4}, H = {FH4};
// beat 1: KPI
move("#d-cur", 1420, 250, 2.4, 1.0);
click("#d-cur", "#d-ring", 1420, 250, 3.3);
cam("#d-cam", W, H, 1420, 250, 1.9, 3.0, 1.3);
hl("#d-h1", 3.5);
tl.to("#d-c1", {{ opacity: 1, duration: 0.4 }}, 3.3);
// beat 2: AI analysis
hlOff("#d-h1", 5.6);
tl.to("#d-c1", {{ opacity: 0.38, duration: 0.4 }}, 5.6);
move("#d-cur", 900, 470, 5.6, 1.0);
cam("#d-cam", W, H, 1080, 430, 1.45, 5.6, 1.4);
hl("#d-h2", 6.4);
tl.to("#d-c2", {{ opacity: 1, duration: 0.4 }}, 6.0);
// beat 3: donut
hlOff("#d-h2", 7.6);
tl.to("#d-c2", {{ opacity: 0.38, duration: 0.4 }}, 7.6);
move("#d-cur", 1560, 760, 7.6, 1.0);
cam("#d-cam", W, H, 1536, 706, 1.9, 7.6, 1.4);
click("#d-cur", "#d-ring", 1560, 760, 8.6);
hl("#d-h3", 8.4);
tl.to("#d-c3", {{ opacity: 1, duration: 0.4 }}, 8.2);
// pull back
hlOff("#d-h3", 9.4);
cam("#d-cam", W, H, 960, 540, 1, 9.4, 1.3);
["#d-c1", "#d-c2"].forEach((s) => tl.to(s, {{ opacity: 1, duration: 0.5 }}, 9.6));
tl.to("#d-frame", {{ rotateY: -4, rotateX: 2, duration: 1.5, ease: "power2.inOut" }}, 9.4);
outro();
"""
)

# ============================================================ 05 SCAN
FW5 = 1240
ov5 = """<div id="sc-bar" class="abs" style="left:404px;top:302px;width:1352px;height:14px;border-radius:7px;background:#e5e5e5;overflow:hidden"><div id="sc-fill" class="abs" style="left:0;top:0;width:100%;height:100%;background:linear-gradient(90deg,#047857 0%,#047857 88%,#ef4444 88%,#ef4444 100%);transform-origin:0 50%"></div></div>
<div id="sc-h1" class="hl" style="left:404px;top:366px;width:440px;height:294px;opacity:0"></div>
<div id="sc-h2" class="hl" style="left:412px;top:886px;width:1336px;height:62px;opacity:0"></div>"""
b5, FH5 = browser("sc", "shot-scan.png", "wearden.local/scans/full-top-100", 96, 196, FW5, ov5)
S["s05-scan"] = (
    plate("fibers.jpg", "dim")
    + f"""
{b5}
<div class="abs" style="left:1384px;top:170px;width:440px">
  <div id="sc-eye" class="eyebrow"><i></i><span>04 · Bir skan</span></div>
  <h2 id="sc-h" style="margin-top:28px;font-size:66px"><span class="ln"><span>100 yoxlama.</span></span><span class="ln"><span class="red">12 real risk.</span></span></h2>
  <div style="display:flex;gap:36px;margin-top:40px">
    <div id="sc-s1"><div id="sc-pass" style="font-size:108px;font-weight:900;letter-spacing:-.05em;line-height:.9;color:#34d399">0</div><div class="sub" style="font-size:26px;margin-top:8px">keçdi</div></div>
    <div id="sc-s2"><div id="sc-fail" style="font-size:108px;font-weight:900;letter-spacing:-.05em;line-height:.9;color:#f87171">0</div><div class="sub" style="font-size:26px;margin-top:8px">keçmədi</div></div>
  </div>
  <div style="margin-top:36px">
    <div id="sc-c1" class="call"><span class="n">AI</span><div class="t">Düzəlt, bax və ya qəbul et<small>Hər uğursuzluq üçün qərar və səbəb</small></div></div>
    <div id="sc-c2" class="call"><span class="n">#1</span><div class="t">Əvvəlcə SSH root girişi<small>Öncə işlək sudo admin yoxlanır, kilidlənmə olmur</small></div></div>
  </div>
</div>""",
    browser_open_js("sc", FW5, FH5, 0.4, -1)
    + f"""
eyebrow("#sc-eye", 0.6);
lines("#sc-h", 0.8, 0.14);
kb({{ scale: 1.15, x: -60 }}, {{ scale: 1.05, x: 0 }});
particles(16, 55);
const W = {FW5}, H = {FH5};
// live scan: zoom on the header + progress bar
cam("#sc-cam", W, H, 1080, 270, 1.7, 2.3, 1.3);
tl.fromTo("#sc-fill", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 2.0, ease: "power1.inOut" }}, 2.5);
count("#sc-pass", 88, 2.5, 2.0, {{ ease: "power1.inOut" }});
count("#sc-fail", 12, 2.5, 2.0, {{ ease: "power1.inOut" }});
blurIn("#sc-s1, #sc-s2", 2.2, 0.8);
// donut
cam("#sc-cam", W, H, 624, 520, 1.9, 4.6, 1.3);
move("#sc-cur", 690, 560, 4.6, 1.1);
hl("#sc-h1", 5.4);
// AI decisions
hlOff("#sc-h1", 6.8);
cam("#sc-cam", W, H, 1080, 900, 1.45, 6.8, 1.5);
move("#sc-cur", 560, 918, 7.0, 1.2);
click("#sc-cur", "#sc-ring", 560, 918, 8.3);
hl("#sc-h2", 8.2);
rise("#sc-c1", 7.0, 0.8, 30);
rise("#sc-c2", 8.0, 0.8, 30);
outro();
"""
)

# ============================================================ 06 ROLLBACK
ROWS = [
    ("LNX-SSH-007", "Root login over SSH", "PermitRootLogin", "yes", "no"),
    ("LNX-NET-015", "Core dumps for set-id programs", "fs.suid_dumpable", "2", "0"),
    ("LNX-FS-009", "nodev, nosuid, noexec on /tmp", "/tmp mount options", "defaults", "nodev,nosuid,noexec"),
]
rows = ""
for k, (cid, name, key, before, after) in enumerate(ROWS):
    y = 236 + k * 104
    rows += f"""<div id="rb-r{k}" class="abs" style="left:0;top:{y}px;width:1060px;height:104px;border-top:1px solid #e7e7e7;display:flex;align-items:center;padding:0 30px;font-size:22px;color:#0a0a0a">
  <div style="width:30px;height:30px;border-radius:7px;border:2px solid #cfcfcf;position:relative;flex:none"><div id="rb-k{k}" class="abs" style="inset:-2px;border-radius:7px;background:#0a0a0a;opacity:0"><svg viewBox="0 0 24 24" style="width:100%;height:100%"><path d="M6 12.5l4 4L18 8" stroke="#fff" stroke-width="3" fill="none"/></svg></div></div>
  <div style="width:330px;margin-left:24px"><div class="mono" style="font-size:19px;font-weight:700">{cid}</div><div style="color:#525252;margin-top:4px;font-size:20px">{name}</div></div>
  <div class="mono" style="width:210px;font-size:18px;color:#525252">{key}</div>
  <div class="mono" style="width:170px;font-size:19px">{before}</div>
  <div style="width:190px;position:relative;height:40px"><span id="rb-a{k}" class="mono abs" style="left:0;top:8px;font-size:19px;white-space:nowrap">{after if len(after) < 12 else after[:11] + '…'}</span><span id="rb-b{k}" class="mono abs" style="left:0;top:8px;font-size:19px;color:#047857;font-weight:700;opacity:0">{before}</span></div>
  <div style="position:relative;width:150px;height:40px"><span id="rb-s{k}" class="abs" style="left:0;top:2px;padding:6px 14px;border-radius:999px;background:#ecfdf5;color:#047857;font-size:18px;font-weight:600;white-space:nowrap">applied</span><span id="rb-t{k}" class="abs" style="left:0;top:2px;padding:6px 14px;border-radius:999px;background:#0a0a0a;color:#fff;font-size:18px;font-weight:600;white-space:nowrap;opacity:0">↺ restored</span></div>
</div>"""
S["s06-rollback"] = (
    plate("rewind.jpg", "scrimL", '<div id="rb-flash" class="abs" style="inset:0;background:radial-gradient(circle at 73% 46%,#d1fae5 0%,rgba(16,185,129,.6) 25%,transparent 60%);opacity:0"></div>')
    + f"""
<div id="rb-left" class="abs" style="left:96px;top:250px;width:760px">
  <div id="rb-eye" class="eyebrow"><i></i><span>05 · Təhlükəsiz dizayn</span></div>
  <h2 id="rb-h" style="margin-top:30px;font-size:80px"><span class="ln"><span>Hər dəyişiklik</span></span><span class="ln"><span class="em">geri qaytarılır.</span></span></h2>
  <p id="rb-sub" class="sub" style="margin-top:30px;width:620px">Əvvəlcə ehtiyat nüsxə, sonra təkrar yoxlama. Bir nəzarəti, seçimi və ya bütün işi geri qaytarın.</p>
</div>
<div class="persp"><div id="rb-panel" class="abs" style="left:780px;top:190px;width:1060px;height:720px;background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 70px 160px rgba(0,0,0,.7),0 0 140px rgba(16,185,129,.25);color:#0a0a0a">
  <div class="abs" style="left:30px;top:30px"><div style="font-size:15px;color:#737373;letter-spacing:.08em" class="mono">HARDENING / RUN DETAIL</div><div style="font-size:32px;font-weight:700;letter-spacing:-.02em;margin-top:8px">CIS Ubuntu 24.04 · 3 changes applied</div><div style="font-size:19px;color:#525252;margin-top:6px">Each applied change keeps its backup.</div></div>
  <div class="abs" style="right:30px;top:44px;display:flex;gap:12px"><span style="padding:12px 20px;border:1px solid #d4d4d4;border-radius:10px;font-size:19px;font-weight:600">Roll back selected</span><span id="rb-btn" style="padding:12px 20px;background:#0a0a0a;color:#fff;border-radius:10px;font-size:19px;font-weight:600">Roll back all</span></div>
  <div class="abs mono" style="left:0;top:196px;width:1060px;height:40px;display:flex;align-items:center;padding:0 30px;font-size:15px;color:#737373;letter-spacing:.08em;background:#fafafa;border-top:1px solid #e7e7e7"><span style="width:54px"></span><span style="width:330px">CONTROL</span><span style="width:210px">SETTING</span><span style="width:170px">BEFORE</span><span style="width:190px">CURRENT</span><span>STATUS</span></div>
  {rows}
  <div id="rb-foot" class="abs" style="left:30px;top:572px;width:1000px;padding:20px 24px;border-radius:14px;background:#ecfdf5;border:1px solid #a7f3d0;display:flex;gap:16px;align-items:center;font-size:21px;color:#065f46;opacity:0"><svg viewBox="0 0 24 24" style="width:30px;height:30px;flex:none"><circle cx="12" cy="12" r="11" fill="#10b981"/><path d="M7 12.5l3.2 3.2L17 9" stroke="#fff" stroke-width="2.6" fill="none"/></svg><span><b>3 changes restored.</b> Each check re-ran after the rollback; the full report is exportable.</span></div>
  <div id="rb-modal" class="abs" style="left:270px;top:250px;width:520px;padding:28px;border-radius:16px;background:#fff;box-shadow:0 30px 80px rgba(0,0,0,.35);border:1px solid #e5e5e5;opacity:0"><div style="font-size:24px;font-weight:700">Roll back every applied change in this run?</div><div style="display:flex;justify-content:flex-end;gap:12px;margin-top:24px"><span style="padding:10px 18px;border:1px solid #d4d4d4;border-radius:10px;font-size:18px">Cancel</span><span style="padding:10px 18px;background:#0a0a0a;color:#fff;border-radius:10px;font-size:18px;font-weight:600">Roll back</span></div></div>
  <div id="rb-cur" class="cur">{CURSOR}</div><div id="rb-ring" class="ring"></div>
</div></div>""",
    r"""
// phase A: the rewind ring spins backwards
tl.set("#plate", { transformOrigin: "1506px 554px" }, 0);
tl.fromTo("#plate", { rotation: 20, x: 0 }, { rotation: -40, x: -20, duration: 3.6, ease: "power2.inOut" }, 0);
particles(22, 66);
eyebrow("#rb-eye", 0.6);
lines("#rb-h", 0.8, 0.16);
blurIn("#rb-sub", 1.6, 1.0);
// phase B: punch through the ring into the product
tl.to("#plate", { scale: 3.2, opacity: 0.25, duration: 0.9, ease: "expo.in" }, 3.6);
tl.fromTo("#rb-flash", { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "power2.in" }, 4.05);
tl.to("#rb-flash", { opacity: 0, duration: 0.7, ease: "power2.out" }, 4.4);
tl.to("#rb-left", { x: -30, opacity: 0.9, duration: 0.6 }, 3.6);
tl.fromTo("#rb-panel", { opacity: 0, scale: 0.6, rotateY: -30, z: -400 }, { opacity: 1, scale: 1, rotateY: 0, z: 0, duration: 1.3, ease: "expo.out" }, 4.2);
[0, 1, 2].forEach((k) => tl.fromTo("#rb-r" + k, { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.7, ease: "expo.out" }, 4.7 + k * 0.12));
// select rows, roll back all
tl.set("#rb-cur", { x: 700, y: 760 }, 0);
move("#rb-cur", 52, 284, 5.4, 0.8);
[0, 1, 2].forEach((k) => { tl.to("#rb-cur", { y: 284 + k * 104, duration: 0.25, ease: "power2.inOut" }, 6.2 + k * 0.3); click("#rb-cur", "#rb-ring", 52, 284 + k * 104, 6.42 + k * 0.3, 0.26); tl.fromTo("#rb-k" + k, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.2 }, 6.44 + k * 0.3); });
move("#rb-cur", 975, 70, 7.3, 0.6);
click("#rb-cur", "#rb-ring", 975, 70, 7.9, 0.5);
tl.fromTo("#rb-modal", { opacity: 0, scale: 0.92, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(2)" }, 8.0);
move("#rb-cur", 728, 344, 8.2, 0.45);
click("#rb-cur", "#rb-ring", 728, 344, 8.7, 0.5);
tl.to("#rb-modal", { opacity: 0, scale: 0.96, duration: 0.25 }, 8.8);
[0, 1, 2].forEach((k) => {
  const t = 9.0 + k * 0.28;
  tl.fromTo("#rb-a" + k, { opacity: 1, x: 0, filter: "blur(0px)" }, { opacity: 0, x: -40, filter: "blur(6px)", duration: 0.3, ease: "power2.in" }, t);
  tl.fromTo("#rb-b" + k, { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.4, ease: "expo.out" }, t + 0.2);
  tl.to("#rb-s" + k, { opacity: 0, duration: 0.2 }, t + 0.1);
  tl.fromTo("#rb-t" + k, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.5)" }, t + 0.2);
  tl.fromTo("#rb-r" + k, { backgroundColor: "rgba(16,185,129,0)" }, { backgroundColor: "rgba(16,185,129,0.12)", duration: 0.25, yoyo: true, repeat: 1 }, t);
});
tl.fromTo("#rb-foot", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, 9.9);
tl.to("#rb-cur", { opacity: 0, duration: 0.3 }, 10.0);
outro();
"""
)

# ============================================================ 07 ATT&CK
cells = ""
for k in range(53):
    c, r = k % 18, k // 18
    cls = "a" if k < 36 else ("b" if k < 39 else "c")
    cells += f'<div class="ac ac-{cls}" style="left:{c*46}px;top:{r*46}px"></div>'
S["s07-attack"] = (
    plate("network.jpg", "scrimL")
    + f"""
<style>.ac{{position:absolute;width:36px;height:36px;border-radius:8px}}.ac-a{{background:rgba(243,246,244,.85)}}.ac-b{{background:#34d399;box-shadow:0 0 18px rgba(16,185,129,.9)}}.ac-c{{border:2px solid rgba(248,113,113,.6)}}</style>
<div class="abs" style="left:96px;top:190px;width:860px">
  <div id="at-eye" class="eyebrow"><i></i><span>06 · MITRE ATT&amp;CK</span></div>
  <h2 id="at-h" style="margin-top:30px;font-size:92px"><span class="ln"><span>Gücləndirmənin</span></span><span class="ln"><span class="em">təsiri görünür.</span></span></h2>
  <p id="at-sub" class="sub" style="margin-top:28px;width:800px">Texnikaya bağlı nəzarətlər yoxlanılan hostlarda keçəndə texnika əhatə olunmuş sayılır.</p>
  <div id="at-grid" class="abs" style="left:0;top:560px;width:828px;height:130px">{cells}</div>
  <div id="at-leg" class="abs mono" style="left:0;top:720px;display:flex;gap:30px;font-size:21px;color:#9fb0a7;white-space:nowrap"><span>■ əvvəldən əhatəli</span><span style="color:#34d399">■ yeni əhatə</span><span style="color:#f87171">□ hələ boşluq</span></div>
</div>
<div class="abs" style="left:1190px;top:250px;width:620px;height:620px">
  <svg viewBox="0 0 620 620" width="620" height="620" style="position:absolute;left:0;top:0;transform:rotate(-90deg)">
    <circle cx="310" cy="310" r="260" fill="rgba(3,6,5,.6)" stroke="rgba(255,255,255,.1)" stroke-width="26"/>
    <circle id="at-a1" cx="310" cy="310" r="260" fill="none" stroke="#e7ece9" stroke-width="26" pathLength="53" stroke-dasharray="36 53" stroke-dashoffset="36"/>
    <circle id="at-a2" cx="310" cy="310" r="260" fill="none" stroke="#34d399" stroke-width="26" pathLength="53" stroke-dasharray="3 53" stroke-dashoffset="-33" style="filter:drop-shadow(0 0 14px rgba(16,185,129,.9))"/>
  </svg>
  <div class="abs" style="left:0;top:170px;width:620px;text-align:center"><span id="at-num" style="font-size:200px;font-weight:900;letter-spacing:-.06em;line-height:1">0</span><span style="font-size:64px;font-weight:700;color:#9fb0a7">/53</span></div>
  <div id="at-lab" class="abs" style="left:0;top:400px;width:620px;text-align:center;font-size:30px;color:#9fb0a7">texnika əhatə olunub</div>
  <div id="at-delta" class="abs mono" style="left:190px;top:456px;width:240px;text-align:center;padding:10px 0;border-radius:999px;background:rgba(16,185,129,.16);border:1px solid #34d399;color:#6ee7b7;font-size:26px;font-weight:700">+3 yeni</div>
</div>""",
    r"""
kb({ scale: 1.25, x: 60 }, { scale: 1.02, x: -20 });
particles(24, 77);
eyebrow("#at-eye", 0.6);
lines("#at-h", 0.8, 0.16);
blurIn("#at-sub", 1.5, 1.0);
tl.fromTo("#at-grid .ac", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)", stagger: { each: 0.025, from: "start" } }, 2.0);
tl.fromTo("#at-grid .ac-b", { scale: 1 }, { scale: 1.35, duration: 0.25, yoyo: true, repeat: 1, ease: "power2.out", stagger: 0.12 }, 5.6);
blurIn("#at-leg", 3.4, 0.8);
tl.fromTo("#at-a1", { strokeDashoffset: 36 }, { strokeDashoffset: 0, duration: 2.0, ease: "power3.inOut" }, 2.2);
tl.fromTo("#at-a2", { strokeDasharray: "0 53" }, { strokeDasharray: "3 53", duration: 0.9, ease: "power3.out" }, 5.4);
count("#at-num", 36, 2.2, 2.0, { ease: "power3.inOut" });
const n2 = { v: 36 }, el2 = document.getElementById("at-num");
tl.fromTo(n2, { v: 36 }, { v: 39, duration: 0.9, ease: "power3.out", onUpdate: () => (el2.textContent = Math.round(n2.v)) }, 5.4);
tl.fromTo("#at-num", { color: "#f3f6f4" }, { color: "#6ee7b7", duration: 0.5 }, 5.5);
blurIn("#at-lab", 2.6, 0.8);
tl.fromTo("#at-delta", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.6, ease: "back.out(2.5)" }, 6.1);
outro();
"""
)

# ============================================================ 08 USERS
USERS = [
    ("building", "KOB-larda IT komandaları", "Ayrıca təhlükəsizlik mühəndisi olmadan server və iş stansiyalarını gücləndirin."),
    ("uni", "Universitetlər və dövlət sektoru", "Auditə hazır hesabatlar və tam izlə CIS uyğunluğunu sübut edin."),
    ("term", "MSSP-lər və pentesterlər", "Agent quraşdırmadan, SSH və ya WinRM ilə çoxlu hostu uzaqdan yoxlayın."),
]
ucards = ""
for k, (ic, t, d) in enumerate(USERS):
    ucards += f"""<div id="u-c{k}" class="glass" style="left:{96 + k*592}px;top:590px;width:560px;height:380px;padding:38px">
  {icon(ICONS[ic], f"u-i{k}")}
  <div style="font-size:38px;font-weight:700;letter-spacing:-.02em;margin-top:22px;line-height:1.1">{t}</div>
  <div class="sub" style="font-size:27px;margin-top:12px">{d}</div></div>"""
S["s08-users"] = (
    plate("soc.jpg", "scrimT scrimB")
    + f"""
<div class="abs" style="left:96px;top:160px;width:1500px">
  <div id="u-eye" class="eyebrow"><i></i><span>07 · Hədəf istifadəçilər</span></div>
  <h2 id="u-h" style="margin-top:28px;font-size:92px"><span class="ln"><span>Böyük təhlükəsizlik komandası</span></span><span class="ln"><span class="em">olmayanlar üçün.</span></span></h2>
  <div id="u-plat" style="display:flex;gap:14px;margin-top:36px"><span class="chip"><b></b>Ubuntu 22.04</span><span class="chip"><b></b>Ubuntu 24.04</span><span class="chip"><b></b>Windows 10 · 11</span><span class="chip"><b></b>Windows Server 2022</span></div>
</div>
{ucards}""",
    r"""
kb({ scale: 1.04, y: 0 }, { scale: 1.14, y: -30 });
particles(18, 88);
eyebrow("#u-eye", 0.6);
lines("#u-h", 0.8, 0.16);
blurIn("#u-plat .chip", 1.6, 0.7, 0.1);
[0, 1, 2].forEach((k) => {
  tl.fromTo("#u-c" + k, { opacity: 0, y: 100, rotateX: -35 }, { opacity: 1, y: 0, rotateX: 0, duration: 1.2, ease: "expo.out" }, 2.4 + k * 0.25);
  draw("#u-i" + k + " path", 2.8 + k * 0.25, 1.0, "power2.out");
});
outro();
"""
)

# ============================================================ 09 IMPACT
STATS = [("100", "", "CIS nəzarəti bir skanda yoxlanılır"), ("1", "&nbsp;klik", "gücləndirmək üçün, 1 klik də geri qaytarmaq üçün"), ("100", "%", "dəyişiklik qeydə alınır, təkrar yoxlanılır və ixrac olunur")]
stats = ""
for k, (n, suf, d) in enumerate(STATS):
    stats += f"""<div id="i-s{k}" style="display:flex;align-items:baseline;gap:26px;padding:26px 0;border-top:1px solid rgba(255,255,255,.14)">
  <div style="width:330px;flex:none;font-size:110px;font-weight:900;letter-spacing:-.05em;line-height:.9;color:#34d399"><span id="i-n{k}">{n}</span><span style="font-size:52px;margin-left:10px">{suf.replace("&nbsp;", "")}</span></div>
  <div style="font-size:34px;font-weight:600;line-height:1.25">{d}</div></div>"""
S["s09-impact"] = (
    plate("layers.jpg", "dim scrimL")
    + f"""
<div class="abs" style="left:96px;top:160px;width:1100px">
  <div id="i-eye" class="eyebrow"><i></i><span>08 · Təsir</span></div>
  <h2 id="i-h" style="margin-top:28px;font-size:76px"><span class="ln"><span>Saatlarla əl işi əvəzinə</span></span><span class="ln"><span class="em">geri qaytarıla bilən bir klik.</span></span></h2>
  <div style="margin-top:46px;width:1000px">{stats}</div>
</div>""",
    r"""
kb({ scale: 1.2, x: -40 }, { scale: 1.08, x: 30 });
particles(20, 99);
eyebrow("#i-eye", 0.6);
lines("#i-h", 0.8, 0.16);
[0, 1, 2].forEach((k) => rise("#i-s" + k, 1.9 + k * 0.3, 0.9, 40));
count("#i-n0", 100, 2.0, 1.4); count("#i-n1", 1, 2.3, 0.8); count("#i-n2", 100, 2.6, 1.4);
outro();
"""
)


# ============================================================ 10 MARKET
GTM = [("1", "Pilot", "OYU və universitetlər"), ("2", "Yerli bazar", "Azərbaycan KOB-ları və banklar"), ("3", "Region", "MSSP tərəfdaşları ilə Qafqaz və MDB")]
gtm = ""
for k, (n, t, d) in enumerate(GTM):
    gtm += f"""<div id="m-g{k}" class="glass" style="left:{96 + k*592}px;top:800px;width:552px;height:160px;padding:28px 32px;display:flex;gap:24px;align-items:center">
  <div style="width:64px;height:64px;border-radius:50%;border:2px solid #34d399;display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:700;color:#34d399;flex:none">{n}</div>
  <div><div class="mono" style="font-size:22px;letter-spacing:.18em;color:#34d399">{t.replace("i", "İ").upper()}</div><div style="font-size:32px;font-weight:700;margin-top:6px;line-height:1.15">{d}</div></div></div>"""
S["s10-market"] = (
    plate("pillars.jpg", "scrimL")
    + f"""
<div class="abs" style="left:96px;top:160px;width:1100px">
  <div id="m-eye" class="eyebrow"><i></i><span>09 · Bazar</span></div>
  <h2 id="m-h" style="margin-top:28px;font-size:84px"><span class="ln"><span>Bazar böyükdür</span></span><span class="ln"><span class="em">və hər il böyüyür.</span></span></h2>
</div>
<div class="abs" style="left:96px;top:440px;width:1000px">
  <div id="m-r0" style="display:flex;align-items:center;gap:26px;height:90px"><span class="mono" style="width:90px;font-size:28px;color:#9fb0a7">2025</span><div style="position:relative;width:700px;height:56px"><div id="m-b0" class="abs" style="left:0;top:0;width:{round(700*26.64/53.31)}px;height:56px;border-radius:12px;background:linear-gradient(90deg,#065f46,#10b981);transform-origin:0 50%"></div></div><span id="m-v0" style="font-size:44px;font-weight:800;white-space:nowrap">$0B</span></div>
  <div id="m-r1" style="display:flex;align-items:center;gap:26px;height:90px"><span class="mono" style="width:90px;font-size:28px;color:#9fb0a7">2030</span><div style="position:relative;width:700px;height:56px"><div id="m-b1" class="abs" style="left:0;top:0;width:700px;height:56px;border-radius:12px;background:linear-gradient(90deg,#10b981,#6ee7b7);box-shadow:0 0 40px rgba(16,185,129,.6);transform-origin:0 50%"></div></div><span id="m-v1" style="font-size:44px;font-weight:800;color:#6ee7b7;white-space:nowrap">$0B</span></div>
  <div id="m-cap" class="mono" style="margin-top:18px;font-size:22px;color:#7d8d85;letter-spacing:.04em">SECURITY POSTURE MANAGEMENT BAZARI · İLLİK ARTIM 14.9% · MARKETSANDMARKETS</div>
</div>
<div id="m-az" class="glass" style="left:1240px;top:380px;width:584px;height:390px;padding:32px 36px">
  <div class="mono" style="font-size:22px;letter-spacing:.2em;color:#34d399">AZƏRBAYCAN</div>
  <div style="display:flex;align-items:baseline;gap:14px;margin-top:16px"><span id="m-az1" style="font-size:96px;font-weight:900;letter-spacing:-.05em;line-height:.9;color:#f87171">0</span><span style="font-size:40px;font-weight:700">mln AZN</span></div>
  <div class="sub" style="font-size:26px;margin-top:10px">kiber insidentlərdən gözlənilən illik itki (report.az)</div>
  <div style="height:1px;background:rgba(255,255,255,.14);margin:20px 0"></div>
  <div style="font-size:25px;line-height:1.3"><b style="color:#34d399">Fürsət:</b> yerli bazarda avtomatik gücləndirmə və geri qaytarma edən əlçatan məhsul yoxdur.</div>
</div>
{gtm}""",
    r"""
tl.fromTo("#plate", { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 3.2, ease: "power2.inOut" }, 0.6);
kb({ scale: 1.08, x: 30 }, { scale: 1.16, x: -50 });
particles(26, 131);
eyebrow("#m-eye", 0.6);
lines("#m-h", 0.8, 0.16);
blurIn("#m-r0, #m-r1", 1.6, 0.8, 0.15);
tl.fromTo("#m-b0", { scaleX: 0 }, { scaleX: 1, duration: 1.3, ease: "expo.out" }, 2.0);
tl.fromTo("#m-b1", { scaleX: 0 }, { scaleX: 1, duration: 1.8, ease: "expo.out" }, 2.4);
count("#m-v0", 26.6, 2.0, 1.3, { dec: 1, pre: "$", suf: "B" });
count("#m-v1", 53.3, 2.4, 1.8, { dec: 1, pre: "$", suf: "B" });
blurIn("#m-cap", 3.2, 0.8);
tl.fromTo("#m-az", { opacity: 0, x: 80, rotateY: -20 }, { opacity: 1, x: 0, rotateY: 0, duration: 1.2, ease: "expo.out" }, 3.4);
count("#m-az1", 40, 3.6, 1.4, { ease: "power2.out" });
[0, 1, 2].forEach((k) => tl.fromTo("#m-g" + k, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.9, ease: "expo.out" }, 5.2 + k * 0.35));
outro();
"""
)

# ============================================================ 11 COMPETITION
COLS = ["CIS yoxlaması", "Avto düzəliş", "Geri qaytarma", "AI prioritet", "ATT&amp;CK təsiri"]
COMP = [
    ("Wearden", "YYYYY", "Host başına · KOB üçün"),
    ("CalCom CHS", "YYYNN", "Sorğu ilə · enterprise"),
    ("CIS-CAT Pro", "YNNNN", "SecureSuite üzvlüyü"),
    ("Nessus Pro", "YNNNN", "$4,790 / il"),
    ("Wazuh SCA", "YNNNN", "Pulsuz · əl ilə düzəliş"),
    ("OpenSCAP", "YPNNN", "Pulsuz · geri qaytarma yox"),
]
MARK = {
    "Y": '<svg viewBox="0 0 24 24" style="width:40px;height:40px"><circle cx="12" cy="12" r="11" fill="#10b981"/><path d="M7 12.5l3.2 3.2L17 9" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "N": '<svg viewBox="0 0 24 24" style="width:40px;height:40px"><circle cx="12" cy="12" r="10" fill="none" stroke="rgba(255,255,255,.18)" stroke-width="1.6"/><path d="M8.5 12h7" stroke="rgba(255,255,255,.35)" stroke-width="2.2" stroke-linecap="round"/></svg>',
    "P": '<svg viewBox="0 0 24 24" style="width:40px;height:40px"><circle cx="12" cy="12" r="10" fill="none" stroke="#f59e0b" stroke-width="2"/><path d="M12 2a10 10 0 0 1 0 20z" fill="#f59e0b"/></svg>',
}
CW = [320, 170, 170, 170, 170, 170, 330]
hdr = "".join(f'<div style="width:{CW[i+1]}px;text-align:center">{c}</div>' for i, c in enumerate(COLS))
trows = ""
for r, (name, marks, price) in enumerate(COMP):
    win = r == 0
    cells = "".join(f'<div style="width:{CW[i+1]}px;display:flex;justify-content:center"><span class="cm cm{i}">{MARK[m]}</span></div>' for i, m in enumerate(marks))
    trows += f"""<div id="cp-r{r}" style="position:relative;display:flex;align-items:center;height:78px;padding:0 30px;border-top:1px solid rgba(255,255,255,.1)">
  {'<div id="cp-win" class="abs" style="inset:4px 8px;border-radius:16px;border:2px solid #34d399;background:rgba(16,185,129,.12);box-shadow:0 0 50px rgba(16,185,129,.35);opacity:0"></div>' if win else ''}
  <div style="position:relative;width:{CW[0]}px;font-size:{34 if win else 30}px;font-weight:{800 if win else 600};color:{'#6ee7b7' if win else '#f3f6f4'}">{name}</div>{cells}
  <div style="position:relative;width:{CW[6]}px;font-size:24px;color:{'#a7f3d0' if win else '#9fb0a7'};text-align:right">{price}</div></div>"""
S["s11-compete"] = (
    plate("chess.jpg", "scrimL")
    + f"""
<div class="abs" style="left:96px;top:150px;width:1500px">
  <div id="cp-eye" class="eyebrow"><i></i><span>10 · Rəqabət</span></div>
  <h2 id="cp-h" style="margin-top:26px;font-size:72px"><span class="ln"><span>Başqaları problemi tapır.</span></span><span class="ln"><span class="em">Wearden düzəldir və geri qaytarır.</span></span></h2>
</div>
<div id="cp-t" class="glass" style="left:96px;top:420px;width:1540px;height:556px;padding:8px 0">
  <div id="cp-hd" class="mono" style="display:flex;align-items:center;height:60px;padding:0 30px;font-size:19px;letter-spacing:.06em;color:#9fb0a7"><div style="width:{CW[0]}px">MƏHSUL</div>{hdr}<div style="width:{CW[6]}px;text-align:right">QİYMƏT</div></div>
  {trows}
</div>
<div id="cp-note" class="abs mono" style="left:96px;top:990px;font-size:19px;color:#6b7c74">◐ qismən: OpenSCAP düzəliş skripti yaradır, amma geri qaytara bilmir (Red Hat). Mənbə: açıq məlumatlar, noyabr 2026.</div>""",
    r"""
kb({ scale: 1.12, x: 40 }, { scale: 1.02, x: -20 });
particles(18, 141);
eyebrow("#cp-eye", 0.6);
lines("#cp-h", 0.8, 0.16);
tl.fromTo("#cp-t", { opacity: 0, y: 70, rotateX: -18 }, { opacity: 1, y: 0, rotateX: 0, duration: 1.2, ease: "expo.out" }, 1.6);
blurIn("#cp-hd", 2.0, 0.7);
[1, 2, 3, 4, 5, 0].forEach((r, k) => tl.fromTo("#cp-r" + r, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.7, ease: "expo.out" }, 2.2 + k * 0.14));
[0, 1, 2, 3, 4].forEach((c) => tl.fromTo("#cp-t .cm" + c, { opacity: 0, scale: 0.2 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.6)", stagger: 0.05 }, 3.4 + c * 0.45));
tl.fromTo("#cp-win", { opacity: 0, scaleX: 0.6 }, { opacity: 1, scaleX: 1, duration: 0.9, ease: "expo.out" }, 6.0);
tl.fromTo("#cp-r0", { scale: 1 }, { scale: 1.03, duration: 0.35, ease: "power2.out", yoyo: true, repeat: 1 }, 6.2);
blurIn("#cp-note", 6.6, 0.8);
outro();
"""
)

# ============================================================ 12 REVENUE
TIERS = [
    ("COMMUNITY", "Pulsuz", "", "5 hosta qədər", ["Skan və hesabat", "Universitet və tələbələr üçün"], False),
    ("PRO", "$4", "/ host / ay", "KOB-lar üçün", ["AI prioritet", "Bir kliklə düzəliş və geri qaytarma"], True),
    ("ENTERPRİSE", "İllik", "lisenziya", "Banklar və dövlət", ["On-prem quraşdırma", "Audit ixracı və dəstək"], False),
]
tiers = ""
for k, (tag, price, unit, who, feats, main) in enumerate(TIERS):
    border = "border:2px solid #34d399;box-shadow:0 30px 80px rgba(0,0,0,.45),0 0 70px rgba(16,185,129,.35)" if main else ""
    badge = '<div class="abs mono" style="right:28px;top:30px;padding:6px 14px;border-radius:999px;background:#10b981;color:#03140d;font-size:18px;font-weight:700;letter-spacing:.08em">ƏSAS GƏLİR</div>' if main else ""
    fl = "".join(f'<div style="display:flex;gap:14px;align-items:center;margin-top:14px;font-size:26px"><span style="width:10px;height:10px;border-radius:50%;background:#34d399;flex:none"></span>{f}</div>' for f in feats)
    tiers += f"""<div id="rv-c{k}" class="glass" style="left:{96 + k*592}px;top:{410 if main else 430}px;width:552px;height:{380 if main else 350}px;padding:36px 38px;{border}">{badge}
  <div class="mono" style="font-size:22px;letter-spacing:.2em;color:#34d399">{tag}</div>
  <div style="display:flex;align-items:baseline;gap:12px;margin-top:14px"><span style="font-size:84px;font-weight:900;letter-spacing:-.05em;line-height:.95">{price}</span><span class="sub" style="font-size:28px">{unit}</span></div>
  <div style="font-size:30px;font-weight:700;margin-top:10px">{who}</div>{fl}</div>"""
S["s12-revenue"] = (
    plate("fibers.jpg", "dim scrimT")
    + f"""
<div class="abs" style="left:96px;top:150px;width:1500px">
  <div id="rv-eye" class="eyebrow"><i></i><span>11 · Gəlir modeli</span></div>
  <h2 id="rv-h" style="margin-top:26px;font-size:76px"><span class="ln"><span>Pulsuz başla,</span></span><span class="ln"><span class="em">host sayı ilə böyü.</span></span></h2>
</div>
{tiers}
<div id="rv-calc" class="glass" style="left:96px;top:850px;width:1728px;height:120px;padding:0 40px;display:flex;align-items:center;gap:40px">
  <div style="font-size:30px;font-weight:600;white-space:nowrap">50 host × $4 × 12 ay =</div>
  <div style="font-size:60px;font-weight:900;letter-spacing:-.04em;color:#6ee7b7;white-space:nowrap"><span id="rv-sum">$0</span><span style="font-size:30px;font-weight:600;color:#9fb0a7"> / il</span></div>
  <div style="width:1px;height:60px;background:rgba(255,255,255,.18)"></div>
  <div id="rv-vs" style="font-size:26px;color:#9fb0a7;line-height:1.3">Nessus Pro: <b style="color:#f3f6f4">$4,790 / il</b>, yalnız skan<br/>MSSP: toplu qiymət və gəlir payı</div>
  <div class="mono" style="margin-left:auto;font-size:18px;color:#6b7c74">TƏXMİNİ</div>
</div>""",
    r"""
kb({ scale: 1.1, x: 0 }, { scale: 1.2, x: -60 });
particles(22, 151);
eyebrow("#rv-eye", 0.6);
lines("#rv-h", 0.8, 0.16);
[0, 2, 1].forEach((k, i) => tl.fromTo("#rv-c" + k, { opacity: 0, y: 120, rotateX: -40 }, { opacity: 1, y: 0, rotateX: 0, duration: 1.2, ease: "expo.out" }, 1.8 + i * 0.3));
tl.fromTo("#rv-c1", { scale: 1 }, { scale: 1.04, duration: 0.4, ease: "power2.out", yoyo: true, repeat: 1 }, 3.4);
tl.fromTo("#rv-calc", { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 1.0, ease: "expo.out" }, 4.6);
const so = { v: 0 }, se = document.getElementById("rv-sum");
tl.fromTo(so, { v: 0 }, { v: 2400, duration: 1.6, ease: "power3.out", onUpdate: () => (se.textContent = "$" + Math.round(so.v).toLocaleString("en-US")) }, 5.0);
blurIn("#rv-vs", 6.0, 0.8);
outro();
"""
)

# ============================================================ 10 FUTURE
ROAD = [("İNDİ", "İşlək MVP", "Linux və Windows, lokal və uzaqdan", True), ("SONRA", "Real mühitdə test", "Real server parklarında sınaqlar", False), ("DAHA SONRA", "Yeni standartlar", "Debian, RHEL və daha çox Windows", False), ("GƏLƏCƏKDƏ", "Özünü bərpa", "Problem olanda avtomatik geri qaytarma", False)]
road = ""
for k, (tag, t, d, done) in enumerate(ROAD):
    x = 150 + k * 440
    dot = "background:#34d399;box-shadow:0 0 24px 6px rgba(16,185,129,.8)" if done else "background:#030605;border:3px solid #34d399"
    road += f"""<div id="f-n{k}" class="abs" style="left:{x}px;top:640px;width:400px">
  <div class="abs" style="left:0;top:178px;width:26px;height:26px;border-radius:50%;{dot}"></div>
  <div class="mono" style="font-size:22px;letter-spacing:.2em;color:#34d399">{tag}</div>
  <div style="font-size:40px;font-weight:700;margin-top:10px;letter-spacing:-.02em">{t}</div>
  <div class="sub" style="font-size:26px;margin-top:6px;width:380px">{d}</div></div>"""
S["s13-future"] = (
    plate("horizon.jpg", "scrimT")
    + f"""
<div class="abs" style="left:0;top:190px;width:1920px;text-align:center">
  <div id="f-eye" class="eyebrow" style="justify-content:center"><i></i><span>12 · Növbəti addımlar</span></div>
  <h2 id="f-h" style="margin-top:28px;font-size:104px"><span class="ln"><span>Prototipdən</span></span><span class="ln"><span class="em">bütün infrastruktura.</span></span></h2>
</div>
<div class="abs" style="left:0;top:560px;width:1920px;height:520px;background:linear-gradient(0deg,rgba(3,6,5,.92),rgba(3,6,5,.55) 60%,transparent)"></div>
<svg class="abs" style="left:0;top:0" width="1920" height="1080"><path id="f-line" pathLength="1" stroke-dasharray="1" d="M163 831 H1790" stroke="#34d399" stroke-width="3" fill="none" style="filter:drop-shadow(0 0 8px rgba(16,185,129,.9))"/></svg>
{road}""",
    r"""
kb({ scale: 1.0, y: 0 }, { scale: 1.16, y: 40 });
particles(30, 111);
eyebrow("#f-eye", 0.7);
lines("#f-h", 0.9, 0.16);
draw("#f-line", 1.8, 3.0, "power2.inOut");
[0, 1, 2, 3].forEach((k) => tl.fromTo("#f-n" + k, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.9, ease: "expo.out" }, 2.0 + k * 0.6));
outro();
"""
)

# ============================================================ 11 CLOSE
S["s14-close"] = (
    plate("hero.jpg", "scrimC")
    + f"""
<div class="abs" style="left:0;top:180px;width:1920px;display:flex;flex-direction:column;align-items:center;text-align:center">
  <svg viewBox="-10 -10 520 678" style="width:118px;height:155px;overflow:visible"><path id="c-lp" pathLength="1" stroke-dasharray="1" d="{LOGO_PATH}" fill="#f3f6f4" fill-opacity="0" stroke="#34d399" stroke-width="12"/></svg>
  <h1 id="c-title" style="font-size:180px;margin-top:30px"><span class="ln"><span>Wearden</span></span></h1>
  <div id="c-tag" style="margin-top:36px;font-size:56px;font-weight:700;letter-spacing:-.03em;line-height:1.2"><span class="ln"><span>Təhlükəni müəyyən et.</span> <span>Həlli yarat.</span> <span class="em">Gələcəyi qoru.</span></span></div>
  <p id="c-en" class="sub" style="margin-top:18px;font-size:32px">Hər hostu gücləndir. Hər dəyişikliyi idarə et.</p>
  <div id="c-q" class="chip" style="margin-top:56px;font-size:34px;padding:18px 34px"><b></b>Təşəkkürlər · Suallar?</div>
</div>""",
    r"""
kb({ scale: 1.25, x: -120 }, { scale: 1.1, x: -60 });
particles(40, 123);
draw("#c-lp", 0.6, 1.4, "power2.inOut");
tl.fromTo("#c-lp", { fillOpacity: 0 }, { fillOpacity: 1, duration: 0.6 }, 1.8);
tl.fromTo("#c-title .ln > span", { yPercent: 115, scale: 1.15 }, { yPercent: 0, scale: 1, duration: 1.6, ease: "expo.out" }, 1.2);
tl.fromTo("#c-tag .ln > span", { yPercent: 115 }, { yPercent: 0, duration: 1.0, ease: "expo.out", stagger: 0.35 }, 2.4);
blurIn("#c-en", 3.8, 1.0);
tl.fromTo("#c-q", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.9, ease: "back.out(2)" }, 4.6);
"""
)


INTROS = {
    "shutter": """
tl.fromTo("#fl-line", { scaleX: 0, opacity: 1 }, { scaleX: 1, opacity: 1, duration: 0.45, ease: "expo.out" }, 0);
tl.fromTo("#stage", { clipPath: "inset(50% 0% 50% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 1.1, ease: "expo.inOut" }, 0.25);
tl.to("#fl-line", { opacity: 0, duration: 0.5 }, 0.95);""",
    "iris": """
tl.fromTo("#stage", { clipPath: "circle(0% at 50% 50%)" }, { clipPath: "circle(80% at 50% 50%)", duration: 1.4, ease: "expo.inOut" }, 0);
tl.fromTo("#fl-ring", { scale: 0, opacity: 1 }, { scale: 2.6, opacity: 1, duration: 0.9, ease: "expo.in" }, 0);
tl.to("#fl-ring", { scale: 3.2, opacity: 0, duration: 0.5, ease: "power2.out" }, 0.9);""",
    "wipe": """
tl.fromTo("#stage", { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 1.15, ease: "expo.inOut" }, 0);
tl.fromTo("#fl-bar", { x: 0, opacity: 1 }, { x: 1800, opacity: 1, duration: 1.0, ease: "expo.inOut" }, 0);
tl.to("#fl-bar", { x: 1928, opacity: 0, duration: 0.2 }, 1.0);""",
    "zoom": """
tl.fromTo("#stage", { scale: 1.3, opacity: 0, filter: "blur(26px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", duration: 1.3, ease: "expo.out" }, 0);""",
}


def write_scene(k, sid, label, dur, kind):
    html, js = S[sid]
    js = COMMON_JS.replace("__D__", str(dur)) + INTROS[kind] + f'\nhud({k+1}, {N});\n' + js
    js += f'\nwindow.__timelines = window.__timelines || {{}};\nwindow.__timelines["{sid}"] = tl;\n'
    doc = f"""<template>
<style>{CSS}</style>
<div id="root" lang="az" data-composition-id="{sid}" data-width="1920" data-height="1080">
<div id="stage">
{html}
</div>
{hud_html(k+1, label)}
<div id="fl-line"></div><div id="fl-bar"></div><div id="fl-ring"></div>
</div>
<script>
{js}</script>
</template>
"""
    open(os.path.join(OUT, "compositions", f"{sid}.html"), "w").write(themed(doc))


starts, t = [], 0
for k, (sid, label, dur, kind, stops, notes) in enumerate(SCENES):
    write_scene(k, sid, label, dur, kind)
    starts.append(t)
    t += dur
TOTAL = t

hosts = "\n".join(
    f'    <div id="{sid}" class="clip" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{starts[k]}" data-duration="{dur}" data-track-index="{k+1}" data-track-kind="graphics" data-label="{label.replace("&", "&amp;")}" data-width="1920" data-height="1080"></div>'
    for k, (sid, label, dur, kind, stops, notes) in enumerate(SCENES)
)
island = {"slides": []}
for k, (sid, label, dur, kind, stops, notes) in enumerate(SCENES):
    s = {"sceneId": sid, "notes": notes}
    if len(stops) > 1:
        s["fragments"] = [round(starts[k] + x, 2) for x in stops[:-1]]
    island["slides"].append(s)

open(os.path.join(OUT, "index.html"), "w").write(themed(f"""<!doctype html>
<html lang="az">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Wearden pitch</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #030605; }}
    </style>
  </head>
  <body>
    <script type="application/hyperframes-slideshow+json">
{json.dumps(island, indent=2)}
    </script>
    <div id="root" data-composition-id="deck" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
{hosts}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.set({{}}, {{}}, {TOTAL});
      window.__timelines["deck"] = tl;
    </script>
  </body>
</html>
"""))
json.dump({"starts": starts, "stops": [[round(starts[k] + x, 2) for x in sc[4]] for k, sc in enumerate(SCENES)], "total": TOTAL},
          open(os.path.join(OUT, "stops.json"), "w"))
print("built", N, "scenes,", TOTAL, "s")
