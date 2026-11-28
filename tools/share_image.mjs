// Draws the default link-preview images (1200x630) for pages with no picture of their own.
// Run once when the brand or home heading changes: node tools/share_image.mjs  (Playwright, no network, 0 credits)
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { fileURLToPath } from 'node:url';
const out = new URL('../assets/', import.meta.url);
const cards = [
  { file: 'share-en.png', lang: 'en', head: 'Study in Australia, your way', sub: 'Courses, working holiday help and student support', foot: 'weintervisa.com' },
  { file: 'share-th.png', lang: 'th', head: 'เรียนต่อออสเตรเลีย<br>ในแบบของคุณ', sub: 'คอร์สเรียน วีซ่าทำงานและท่องเที่ยว และดูแลนักเรียน', foot: 'weintervisa.com/th' },
];
const html = c => `<!doctype html><html lang="${c.lang}"><meta charset="utf-8"><style>
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#0f5c63;color:#fff;font-family:${c.lang === 'th' ? 'Loma,' : ''}"DejaVu Sans",Arial,sans-serif;position:relative;overflow:hidden}
.band{position:absolute;right:-120px;top:-160px;width:560px;height:560px;border-radius:50%;background:#14727a}
.band2{position:absolute;right:120px;bottom:-260px;width:420px;height:420px;border-radius:50%;background:#0b4a50}
.wrap{position:absolute;left:84px;top:84px;right:84px;bottom:72px;display:flex;flex-direction:column}
.brand{font-size:34px;font-weight:700;letter-spacing:.5px}
.bar{width:96px;height:8px;background:#e8a33d;border-radius:4px;margin:40px 0 34px}
h1{font-size:${c.lang === 'th' ? 70 : 76}px;line-height:1.15;font-weight:700;max-width:900px}
p{font-size:32px;line-height:1.35;margin-top:26px;color:#dcefee;max-width:860px}
.foot{margin-top:auto;font-size:26px;color:#bfe0de}
</style><body><div class="band"></div><div class="band2"></div><div class="wrap">
<div class="brand">We International</div><div class="bar"></div><h1>${c.head}</h1><p>${c.sub}</p><div class="foot">${c.foot}</div></div></body></html>`;
const b = await chromium.launch();
const pg = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
for (const c of cards) {
  await pg.setContent(html(c));
  await pg.screenshot({ path: fileURLToPath(new URL(c.file, out)), type: 'png' });
  console.log('wrote assets/' + c.file);
}
await b.close();
