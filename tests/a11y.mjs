// Accessibility check (axe-core) on every built page, phone + desktop.
// Run: python3 build.py && node tests/a11y.mjs
// Needs playwright + axe-core (CI: npm install --no-save playwright@1.48.2 axe-core@4.10.2;
// in the cloud workspace: NODE_PATH=$(npm root -g) with axe-core installed next to the script or globally).
// Rules: WCAG 2.0/2.1 A + AA and axe best practice. Any violation = exit 1.
// Pages that only redirect (meta refresh, e.g. /games) are skipped.
import { createRequire } from "node:module";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const axeSrc = fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../site");
const types = { ".html": "text/html", ".css": "text/css", ".svg": "image/svg+xml", ".js": "text/javascript",
  ".webp": "image/webp", ".jpg": "image/jpeg", ".png": "image/png" };
const server = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split("?")[0]);
  for (const c of p === "/" ? ["index.html"] : [p, p + ".html", path.join(p, "index.html")]) {
    const f = path.join(root, c);
    if (f.startsWith(root) && fs.existsSync(f) && fs.statSync(f).isFile()) {
      res.writeHead(200, { "content-type": types[path.extname(f)] || "text/plain" });
      return res.end(fs.readFileSync(f));
    }
  }
  res.writeHead(404); res.end("");
}).listen(0);
const base = `http://127.0.0.1:${server.address().port}`;

const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(x =>
  x.isDirectory() ? (["assets", "redesign"].includes(x.name) ? [] : walk(path.join(d, x.name)))
  : x.name.endsWith(".html") ? [path.join(d, x.name)] : []);
const files = walk(root).filter(f => !/http-equiv="refresh"/i.test(fs.readFileSync(f, "utf8")));
const urls = files.map(f => "/" + path.relative(root, f).replace(/index\.html$/, "").replace(/\.html$/, ""));
if (urls.length < 50) { console.log(`✗ only ${urls.length} pages found in site/ — run python3 build.py first`); process.exit(1); }

const browser = await chromium.launch();
let fails = 0;
for (const [name, opts] of [["phone", { viewport: { width: 375, height: 800 }, isMobile: true, hasTouch: true }],
                            ["desktop", { viewport: { width: 1280, height: 900 } }]]) {
  const page = await (await browser.newContext(opts)).newPage();
  for (const u of urls) {
    await page.goto(base + u, { waitUntil: "load" });
    await page.addScriptTag({ content: axeSrc });
    const v = await page.evaluate(async () => (await axe.run(document, {
      runOnly: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"] })).violations
      .map(x => `${x.id} [${x.impact}] ${x.help}: ${x.nodes.slice(0, 3).map(n => n.target.join(" ")).join(" | ")}`));
    for (const line of v) { fails++; console.log(`✗ ${name} ${u} ${line}`); }
  }
}
await browser.close(); server.close();
console.log(`${fails ? "✗" : "✓"} axe: ${urls.length} pages × phone + desktop, ${fails} violation(s)`);
process.exit(fails ? 1 : 0);
