// Side-by-side screenshots: live Wix page (left) vs new site (right), phone + desktop.
// Owner quality bar (20 Nov 2026): every new page must be as good as or better than the Wix page,
// compared with images side by side before review. Run on the CI runner (the cloud sandbox cannot
// reach www.weintervisa.com):  python3 build.py && node tools/compare_shots.mjs review/compare
// Read-only on the live site: it only opens public pages. Writes JPEGs + report.json/report.md.
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)("playwright");
import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const LIVE = "https://www.weintervisa.com";
const here = path.dirname(new URL(import.meta.url).pathname);
const root = path.resolve(here, "../site");
const out = path.resolve(process.argv[2] || "review/compare");
fs.mkdirSync(out, { recursive: true });

const types = { ".html": "text/html", ".css": "text/css", ".svg": "image/svg+xml", ".js": "text/javascript", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".gif": "image/gif" };
const server = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split("?")[0]);
  for (const c of p === "/" ? ["index.html"] : [p, p + ".html", path.join(p, "index.html")]) {
    const f = path.join(root, c);
    if (f.startsWith(root) && fs.existsSync(f) && fs.statSync(f).isFile()) {
      res.writeHead(200, { "content-type": types[path.extname(f).toLowerCase()] || "application/octet-stream" });
      return res.end(fs.readFileSync(f));
    }
  }
  res.writeHead(404); res.end("not found");
}).listen(0);
const NEW = `http://127.0.0.1:${server.address().port}`;

const slugs = JSON.parse(fs.readFileSync(path.join(here, "../tests/wix-post-slugs.json"), "utf8"));
const pages = process.env.ONLY ? process.env.ONLY.split(",") : ["/", "/about-we-international", "/courses", "/courses/nursing-pathways-australia", "/fast-track-courses",
  "/english-practice", "/student-services", "/homestay", "/oshc", "/migration-support", "/referral-partners",
  "/frequently-asked-questions", "/contact-us", "/charter-application", "/privacy-policy", "/blog",
  ...slugs.slice(0, 2).map(s => `/post/${s}`)];
const sizes = { phone: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 1 },
                desktop: { viewport: { width: 1280, height: 860 }, deviceScaleFactor: 1 } };
const MAXH = { phone: 3200, desktop: 2400 };

async function measure(ctx, url, size, w) {
  const page = await ctx.newPage();
  try { return await measureOn(page, url, size, w); } finally { await page.close(); }
}
async function measureOn(page, url, size, w) {
  const t0 = Date.now();
  let status = 0;
  try {
    const r = await page.goto(url, { waitUntil: "load", timeout: 45000 });
    status = r ? r.status() : 0;
  } catch (e) { return { status: 0, error: String(e.message).split("\n")[0].slice(0, 120) }; }
  const loadMs = Date.now() - t0;
  // Wix shows a bot check ("Please wait while we verify your request") to fast repeat visits;
  // wait for it to clear, and mark the row blocked if it does not.
  const check = () => /verify your request/i.test(document.body ? document.body.innerText : "");
  await page.waitForFunction(c => !new Function("return " + c)()(), check.toString(), { timeout: 30000 }).catch(() => {});
  await page.waitForTimeout(2500); // Wix paints sections late; let lazy images in
  const m = await page.evaluate(() => {
    const vis = el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
    const text = (document.body.innerText || "").replace(/\s+/g, " ").trim();
    return {
      title: document.title,
      h1: [...document.querySelectorAll("h1")].filter(vis).map(h => h.innerText.trim()).slice(0, 2),
      words: text ? text.split(" ").length : 0,
      links: [...document.querySelectorAll("a[href]")].filter(vis).length,
      buttons: [...document.querySelectorAll("button, a.btn, a.button, [role=button], input[type=submit]")].filter(vis).length,
      forms: document.querySelectorAll("form").length,
      height: document.documentElement.scrollHeight,
      sideways: document.documentElement.scrollWidth > window.innerWidth + 1,
      blocked: /verify your request/i.test(text),
    };
  });
  // Live Wix pages keep their content in embeds (iframes): collect the text of every frame so the
  // team can rebuild the page from what visitors really see (CMS drafts are older than the live page).
  const frameText = [];
  let frameHtml = "";
  for (const f of page.frames()) {
    const t = await f.evaluate(() => document.body ? document.body.innerText : "").catch(() => "");
    if (t && t.trim()) frameText.push(t.trim());
    // keep the markup of the frame with the most text (links, image sources, headings) for the rebuild
    if (t && t.length > (frameHtml.textLen || 0)) {
      const h = await f.evaluate(() => document.body.outerHTML).catch(() => "");
      // inline scripts of that frame hold data the page draws (e.g. the /courses catalogue) — saved as data, never run
      const js = await f.evaluate(() => [...document.scripts].filter(s => !s.src).map(s => s.textContent).join("\n;\n")).catch(() => "");
      frameHtml = Object.assign(new String(h), { textLen: t.length, js });
    }
  }
  m.allWords = frameText.join(" ").split(/\s+/).filter(Boolean).length;
  const img = await page.screenshot({ type: "jpeg", quality: 55, clip: { x: 0, y: 0, width: w,
    height: Math.min(MAXH[size], m.height) } }).catch(() => null);
  return { status, loadMs, ...m, img, frameText, frameHtml: String(frameHtml), frameJs: frameHtml.js || "" };
}

const name0 = p => p === "/" ? "home" : p.slice(1).replace(/\//g, "_");
const browser = await chromium.launch();
const report = [];
for (const [size, opts] of Object.entries(sizes)) {
  const ctx = await browser.newContext(opts);
  for (const p of pages) {
    const { img: liveImg, frameText: liveText, frameHtml: liveHtml, frameJs: liveJs, ...live } = await measure(ctx, LIVE + p, size, opts.viewport.width);
    if (size === "phone" && liveText && liveText.length) {
      fs.mkdirSync(path.join(out, "text"), { recursive: true });
      if (liveHtml) fs.writeFileSync(path.join(out, "text", name0(p) + ".html"), liveHtml.replace(/<script[\s\S]*?<\/script>/gi, "") + "\n");
      if (liveJs && liveJs.length > 200) fs.writeFileSync(path.join(out, "text", name0(p) + ".inline.js.txt"), liveJs + "\n");
      fs.writeFileSync(path.join(out, "text", name0(p) + ".txt"), liveText.join("\n\n----- frame -----\n\n") + "\n");
    }
    await new Promise(r => setTimeout(r, 6000)); // go slowly on the live site
    const { img: newImg, frameText: _nt, frameHtml: _nh, frameJs: _nj, ...neu } = await measure(ctx, NEW + p, size, opts.viewport.width);
    const name = (p === "/" ? "home" : p.slice(1).replace(/\//g, "_")) + "-" + size + ".jpg";
    const b64 = b => b ? `data:image/jpeg;base64,${b.toString("base64")}` : "";
    const w = opts.viewport.width;
    const cmp = await browser.newPage({ viewport: { width: w * 2 + 60, height: 400 }, deviceScaleFactor: 1 });
    await cmp.setContent(`<body style="margin:0;font:14px sans-serif;background:#ddd;display:flex;gap:20px;padding:10px">
      <div><b>Wix (live) ${p}</b><br><img src="${b64(liveImg)}" width="${w}" alt=""></div>
      <div><b>New site ${p}</b><br><img src="${b64(newImg)}" width="${w}" alt=""></div></body>`);
    await cmp.screenshot({ path: path.join(out, name), type: "jpeg", quality: 55, fullPage: true });
    await cmp.close();
    report.push({ path: p, size, image: name, live, new: neu });
    if (live.error || neu.error) console.log("  error:", live.error || "", "|", neu.error || "");
    console.log(size, p, "live", live.status, live.loadMs, "ms", live.words, "words | new", neu.status, neu.loadMs, "ms", neu.words, "words");
  }
  await ctx.close();
}
await browser.close();
server.close();
fs.writeFileSync(path.join(out, "report.json"), JSON.stringify(report, null, 1));
const md = ["| Page | Size | Wix words (all frames) / links / buttons / load ms | New words / links / buttons / load ms | New sideways scroll |", "|---|---|---|---|---|",
  ...report.map(r => `| ${r.path} | ${r.size} | ${r.live.allWords ?? r.live.words ?? "-"} / ${r.live.links ?? "-"} / ${r.live.buttons ?? "-"} / ${r.live.loadMs ?? r.live.error} | ${r.new.words} / ${r.new.links} / ${r.new.buttons} / ${r.new.loadMs} | ${r.new.sideways ? "YES" : "no"} |${r.live.blocked ? " (Wix bot check)" : ""}`)];
fs.writeFileSync(path.join(out, "report.md"), md.join("\n") + "\n");
console.log(md.join("\n"));
