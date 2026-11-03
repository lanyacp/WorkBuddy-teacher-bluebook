// 验证"自定义形象 + 嘴部标记 + 口型开合"
const { chromium } = require('playwright');
const path = require('path');

const CHROME = 'C:/Users/Administrator/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe';
const FILE = 'file:///' + path.resolve(__dirname, '数字人助教_单文件版.html').replace(/\\/g, '/');
const IMG = path.resolve(__dirname, '示例形象_女教师.png');

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  const page = await browser.newPage({ viewport: { width: 1440, height: 980 } });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });

  await page.goto(FILE);
  await page.waitForTimeout(500);

  // 1) 上传自定义形象
  await page.setInputFiles('#fileImg', IMG);
  await page.waitForTimeout(800);
  const mode = await page.evaluate(() => ({
    useImage, imgShown: getComputedStyle(document.querySelector('#faceImg')).display,
    svgHidden: getComputedStyle(document.querySelector('#svgFace')).display,
    overlay: getComputedStyle(document.querySelector('#mouthOverlay')).display
  }));

  // 2) 点击嘴部位置（图片纵向约 44%，横向 50%）
  const box = await page.locator('#stage').boundingBox();
  await page.mouse.click(box.x + box.width * 0.5, box.y + box.height * 0.44);
  await page.waitForTimeout(200);
  const mark = await page.locator('#capHint').textContent();
  const pos = await page.evaluate(() => mouthPos);

  // 3) 闭嘴态
  await page.evaluate(() => { mouthTarget = 0; mouthCur = 0; });
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.resolve(__dirname, '口型对比_闭.png') });

  // 4) 张嘴态：持续触发脉冲，抓一张开口的画面
  await page.evaluate(() => { window.__hold = setInterval(() => { mouthTarget = 1; }, 20); });
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.resolve(__dirname, '口型对比_开.png') });
  const openSize = await page.evaluate(() => {
    const o = document.querySelector('#mouthOverlay');
    return { w: o.style.width, h: o.style.height, left: o.style.left, top: o.style.top };
  });
  await page.evaluate(() => clearInterval(window.__hold));

  // 5) 投屏模式下再来一张
  await page.click('#btnProj');
  await page.waitForTimeout(300);
  await page.evaluate(() => { window.__hold2 = setInterval(() => { mouthTarget = 1; }, 20); });
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.resolve(__dirname, '自定义形象_投屏.png') });
  await page.evaluate(() => clearInterval(window.__hold2));

  console.log(JSON.stringify({ errs, mode, mark, pos, openSize }, null, 2));
  await browser.close();
})();
