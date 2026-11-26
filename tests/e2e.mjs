// Phone + desktop smoke test with screenshots. Run: node tests/e2e.mjs [outDir]
// Serves ./site like GitHub Pages (extensionless /post/<slug> → post/<slug>.html).
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)("playwright"); // global install works from any dir
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { validateLead } from "./getwec-lead-contract.mjs";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../site");
const out = process.argv[2] || "shots";
fs.mkdirSync(out, { recursive: true });
const types = { ".html": "text/html", ".css": "text/css", ".svg": "image/svg+xml", ".xml": "application/xml", ".js": "text/javascript" };
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
const content = ["/families", "/take-a-break", "/about-we-international", "/courses", "/courses/nursing-pathways-australia", "/fast-track-courses", "/english-practice", "/student-services", "/homestay", "/oshc", "/migration-support", "/referral-partners", "/frequently-asked-questions", "/privacy-policy", "/schools", ...JSON.parse(fs.readFileSync(path.join(root, "../content/schools.json"), "utf8")).schools.map(s => `/schools/${s.slug}`)];
const blogCats = JSON.parse(fs.readFileSync(path.join(root, "../content/blog-categories.json"), "utf8")).categories.map(c => `/blog/categories/${c.slug}`);
const urls = ["/", "/blog", ...blogCats, "/no-such-page", "/contact-us", "/charter-application", "/th/", "/th/contact-us", "/th/charter-application", "/working-holiday/charter", "/working-holiday/kca", "/th/working-holiday/charter", "/th/working-holiday/kca", "/already-in-australia", "/th/already-in-australia", "/courses/aged-care-certificate-iii", "/th/courses/aged-care-certificate-iii", ...content, "/th/blog", ...content.map(u => "/th" + u), ...slugs.map(s => `/post/${s}`)];
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
  // Lead forms: empty submit shows errors; valid submit passes the GetWec contract (preview = not sent)
  for (const [u, fill] of [
    ["/th/contact-us", async () => { await page.fill("#c-name", "ทดสอบ ตัวอย่าง"); await page.fill("#c-phone", "LINE: sample_test");
      await page.selectOption("#c-topic", { index: 1 }); await page.fill("#c-msg", "คำถามตัวอย่างเรื่องคอร์สภาษา"); }],
    ["/contact-us", async () => { await page.fill("#c-name", "Test Sample"); await page.fill("#c-email", "test.sample@example.com");
      await page.selectOption("#c-loc", "australia"); await page.selectOption("#c-topic", { index: 1 }); await page.fill("#c-msg", "Sample question about care courses."); }],
    ["/charter-application", async () => { await page.fill("#a-name", "Test Sample"); await page.fill("#a-phone", "0400 000 000");
      await page.selectOption("#a-field", { index: 1 }); await page.selectOption("#a-level", { index: 2 }); await page.fill("#a-start", "2027-02");
      await page.selectOption("#a-city", "Sydney"); await page.fill("#a-msg", "x".repeat(800)); }],
    ["/working-holiday/charter", async () => { await page.fill("#w-name", "Test Sample"); await page.fill("#w-email", "whv.sample@example.com");
      await page.selectOption("#w-visa", { index: 1 }); await page.fill("#w-end", "2027-06"); await page.selectOption("#w-course", { index: 2 }); }],
    ["/working-holiday/kca", async () => { await page.fill("#w-name", "Test Sample"); await page.fill("#w-email", "whv.sample@example.com");
      await page.fill("#w-end", "2027-04"); }],
    ["/th/working-holiday/charter", async () => { await page.fill("#w-name", "ทดสอบ ตัวอย่าง"); await page.fill("#w-email", "whv.th.sample@example.com");
      await page.selectOption("#w-visa", { index: 2 }); await page.fill("#w-end", "2027-03"); await page.selectOption("#w-course", { index: 2 }); }],
    // Already in Australia (26 Nov 2026): course left on "Not sure yet" → GetWec "no school yet" WHV case.
    ["/already-in-australia", async () => { await page.fill("#w-name", "Test Sample"); await page.fill("#w-email", "already.sample@example.com");
      await page.selectOption("#w-visa", { index: 3 }); await page.fill("#w-end", "2027-08"); }],
    ["/th/already-in-australia", async () => { await page.fill("#w-name", "ทดสอบ ตัวอย่าง"); await page.fill("#w-email", "already.th.sample@example.com");
      await page.selectOption("#w-visa", { index: 1 }); await page.fill("#w-end", "2027-05"); }],
    // Aged care comparison (26 Nov 2026): course area + Certificate III preset; School choice goes into the summary.
    ["/courses/aged-care-certificate-iii", async () => { await page.fill("#a-name", "Test Sample"); await page.fill("#a-email", "agedcare.sample@example.com");
      await page.selectOption("#a-school", "KCA Education"); }],
    ["/th/courses/aged-care-certificate-iii", async () => { await page.fill("#a-name", "ทดสอบ ตัวอย่าง"); await page.fill("#a-email", "agedcare.th.sample@example.com"); }],
  ]) {
    await page.goto(base + u, { waitUntil: "load" });
    const note = await page.textContent(".form-status");
    await page.click("form.lead button[type=submit]");
    const errs = await page.locator(".err:not(:empty)").count();
    await fill();
    await page.check("input[name=consent]");
    await page.click("form.lead button[type=submit]");
    const payload = await page.evaluate(() => window.__lastLeadPayload);
    const res = payload ? validateLead(payload) : { ok: false, errors: { none: "no payload" } };
    if (payload && payload.lang !== (u.startsWith("/th/") ? "th" : "en")) res.ok = false, res.errors = { lang: payload.lang };
    // GetWec reads the school + course code from the English option value (whv.js), on Thai pages too.
    if (payload && u.includes("/working-holiday/") && !/Course: (Charter|KCA): /.test(payload.interest)) res.ok = false, res.errors = { course: payload.interest };
    if (payload && u.includes("already-in-australia") && !/Course: Not sure yet/.test(payload.interest)) res.ok = false, res.errors = { course: payload.interest };
    if (payload && u.includes("aged-care-certificate-iii") && !/Course area: (Aged care|งานดูแล).*Level: Certificate III/.test(payload.interest)
        || payload && u.includes("aged-care-certificate-iii") && !/School: (KCA Education|Not sure yet)/.test(payload.interest)) res.ok = false, res.errors = { summary: payload.interest };
    const ok = /Preview/.test(note) && errs >= 2 && res.ok && /Preview check passed/.test(await page.textContent(".form-status"));
    if (!ok) { fails++; console.log(`✗ ${name} form ${u} note=${note} errs=${errs} contract=${JSON.stringify(res.errors)}`); }
    await page.screenshot({ path: `${out}/${name}-form-${u.slice(1)}.png`, fullPage: true });
  }
  // Live mode (endpoint + key injected, network mocked): POST body/headers and success message
  {
    const seen = [];
    await page.route("https://getwec.test/fn", async r => {
      seen.push({ body: JSON.parse(r.request().postData()), h: r.request().headers() });
      await r.fulfill({ status: 200, contentType: "application/json", headers: { "access-control-allow-origin": "*" }, body: '{"ok":true}' });
    });
    await page.route(base + "/contact-us", async r => {
      const res = await r.fetch(); const html = (await res.text()).replace("</head>",
        '<meta name="getwec-endpoint" content="https://getwec.test/fn"><meta name="getwec-key" content="anon-test"></head>');
      await r.fulfill({ response: res, body: html });
    });
    await page.goto(base + "/contact-us", { waitUntil: "load" });
    await page.fill("#c-name", "Test Sample"); await page.fill("#c-email", "test.sample@example.com"); await page.check("input[name=consent]");
    await page.click("form.lead button[type=submit]");
    await page.waitForFunction(() => document.querySelector(".form-status").className.includes("ok"), null, { timeout: 5000 }).catch(() => {});
    const msg = await page.textContent(".form-status");
    const good = seen.length === 1 && seen[0].h.apikey === "anon-test" && seen[0].body.form === "enquiry" && validateLead(seen[0].body).ok && /got your details/.test(msg)
      && (await page.inputValue("#c-name")) === "";
    if (!good) { fails++; console.log(`✗ ${name} live form: posts=${seen.length} msg=${msg}`); }
    await page.unrouteAll();
  }
  console.log(`✓ ${name}: lead forms checked (preview + live mock)`);

  for (const [u, f] of [["/", "home"], ["/th/", "home-th"], ["/th/contact-us", "contact-th"], ["/th/courses", "courses-th"], ["/th/schools/alana-kaye-college", "school-th"], ["/blog", "blog"], [`/post/${slugs.find(s => s.startsWith("oshc"))}`, "post"]]) {
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
