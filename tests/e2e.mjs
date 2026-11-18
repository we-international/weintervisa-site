// Phone + desktop smoke test with screenshots. Run: node tests/e2e.mjs [outDir]
// Serves ./site like GitHub Pages (extensionless /post/<slug> → post/<slug>.html).
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)("playwright"); // global install works from any dir
import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../site");
const out = process.argv[2] || "shots";
fs.mkdirSync(out, { recursive: true });
const types = { ".html": "text/html", ".css": "text/css", ".svg": "image/svg+xml", ".xml": "application/xml" };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]);
  const cands = p === "/" ? ["index.html"] : [p, p + ".html", path.join(p, "index.html")];
  for (const c of cands) {
    const f = path.join(root, c);
    if (f.startsWith(root) && fs.existsSync(f) && fs.statSync(f).isFile()) {
      res.writeHead(200, { "content-type": types[path.extname(f)] || "text/plain" });
      return res.end(fs.readFileSync(f));
    }
  }
  res.writeHead(404, { "content-type": "text/html" });
  res.end(fs.readFileSync(path.join(root, "404.html")));
}).listen(0);
const base = `http://127.0.0.1:${server.address().port}`;

const slugs = JSON.parse(fs.readFileSync(path.join(root, "../tests/wix-post-slugs.json"), "utf8"));
const urls = ["/", "/blog", "/no-such-page", ...slugs.map(s => `/post/${s}`)];
const browser = await chromium.launch();
let fails = 0;
for (const [name, opts] of [["phone", { viewport: { width: 375, height: 800 }, isMobile: true, hasTouch: true }], ["desktop", { viewport: { width: 1280, height: 900 } }]]) {
  const ctx = await browser.newContext(opts);
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", e => errors.push(e.message));
  for (const u of urls) {
    const r = await page.goto(base + u, { waitUntil: "domcontentloaded" });
    const status = r.status();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    const h1 = await page.locator("h1").count();
    const expect = u === "/no-such-page" ? 404 : 200;
    if (status !== expect || overflow > 1 || h1 !== 1) {
      fails++;
      console.log(`✗ ${name} ${u} status=${status} overflow=${overflow} h1=${h1}`);
    }
  }
  if (errors.length) { fails++; console.log(`✗ ${name} JS errors: ${errors.join(" | ")}`); }
  for (const [u, f] of [["/", "home"], ["/blog", "blog"], [`/post/${slugs.find(s => s.startsWith("oshc"))}`, "post"]]) {
    await page.goto(base + u, { waitUntil: "domcontentloaded" });
    await page.waitForTimeout(300);
    await page.screenshot({ path: `${out}/${name}-${f}.png`, fullPage: f !== "blog" });
  }
  console.log(`✓ ${name}: ${urls.length} URLs checked`);
  await ctx.close();
}
await browser.close();
server.close();
console.log(fails ? `${fails} failed` : "all e2e checks passed");
process.exit(fails ? 1 : 0);
