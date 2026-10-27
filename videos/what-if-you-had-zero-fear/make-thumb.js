// Renders thumb.html (thumb.js) once in headless Chrome -> out/thumbnail.png (1280x720, YouTube size).
//   node make-thumb.js        (uses CHROME_PATH like engine/render.js; needs the playwright package)
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {});
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.join(__dirname, 'thumb.html'));
  await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
  const url = await page.evaluate(() => window.renderAt(0.4));
  await browser.close();
  const big = path.join(__dirname, 'out', 'thumbnail-1920.png');
  fs.writeFileSync(big, Buffer.from(String(url).split(',')[1], 'base64'));
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', big, '-vf', 'scale=1280:720:flags=lanczos', path.join(__dirname, 'out', 'thumbnail.png')]);
  console.log('out/thumbnail.png  1280x720');
})();
