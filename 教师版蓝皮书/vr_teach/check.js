const { chromium } = require('playwright');
const path = require('path');
const CHROME = 'C:/Users/Administrator/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe';
const FILE = 'file:///' + encodeURI(path.resolve(__dirname, 'index.html').replace(/\\/g, '/'));
(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });
  await page.goto(FILE);
  await page.waitForTimeout(3500);
  const r = await page.evaluate(() => {
    const out = {};
    out.hasDATA = typeof DATA !== 'undefined';
    out.scenesBtn = document.querySelectorAll('.scn').length;
    out.hotsChildren = document.getElementById('hots') ? document.getElementById('hots').children.length : -1;
    out.texReady = (typeof tex !== 'undefined') ? !!tex : 'no-tex-var';
    try { out.resolvedPrefix = resolveSrc('pano_1').slice(0, 24); } catch (e) { out.resolvedErr = e.message; }
    try {
      const el = document.getElementById('pano_1');
      out.blockLen = el.textContent.length;
      out.blockTrimmedLen = el.textContent.trim().length;
    } catch (e) { out.blockErr = e.message; }
    // 手动触发一次 loadTex 看能否成功
    return out;
  });
  console.log(JSON.stringify({ r, errs: errs.slice(0, 8) }, null, 2));
  await browser.close();
})();
