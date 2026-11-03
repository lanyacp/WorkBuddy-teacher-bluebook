const { chromium } = require('playwright');
const path = require('path');
const CHROME = 'C:/Users/Administrator/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe';
const FILE = 'file:///' + encodeURI(path.resolve(__dirname, 'index.html').replace(/\\/g, '/'));

(async () => {
  for (const args of [
    ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
    ['--enable-unsafe-swiftshader'],
    []
  ]) {
    const browser = await chromium.launch({ executablePath: CHROME, args });
    const page = await browser.newPage({ viewport: { width: 1200, height: 700 } });
    const errs = [];
    page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
    page.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });
    await page.goto(FILE);
    await page.waitForTimeout(2500);
    const info = await page.evaluate(async () => {
      const c = document.querySelector('#cv');
      const out = { w: c.width, h: c.height };
      const g = c.getContext('webgl');
      out.hasCtx = !!g;
      if (g) {
        const dbg = g.getExtension('WEBGL_debug_renderer_info');
        out.renderer = dbg ? g.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : g.getParameter(g.RENDERER);
        out.version = g.getParameter(g.VERSION);
        out.err = g.getError();
        const px = new Uint8Array(4);
        g.readPixels(Math.floor(c.width / 2), Math.floor(c.height / 2), 1, 1, g.RGBA, g.UNSIGNED_BYTE, px);
        out.centerPixel = Array.from(px);
      }
      // 单独测一张图能否加载
      out.imgResult = await new Promise(r => {
        const im = new Image();
        im.onload = () => r({ ok: true, w: im.naturalWidth, h: im.naturalHeight });
        im.onerror = () => r({ ok: false });
        im.src = 'assets/pano_1_wanchun.jpg';
      });
      // 页面内是否已有纹理（通过检查 canvas 截图之外的间接证据）
      out.hotCount = document.querySelectorAll('.hot').length;
      out.hotVisible = Array.from(document.querySelectorAll('.hot')).map(e => e.style.display);
      return out;
    });
    console.log('args:', args.join(' ') || '(无)');
    console.log(JSON.stringify({ ...info, errs: errs.slice(0, 6) }, null, 2));
    await browser.close();
    console.log('---');
  }
})();
