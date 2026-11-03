// 验证 360 互动页 + 截取教程插图
const { chromium } = require('playwright');
const path = require('path');

const CHROME = 'C:/Users/Administrator/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe';
const ROOT = __dirname;
const FILE = 'file:///' + encodeURI(path.resolve(ROOT, 'index.html').replace(/\\/g, '/'));
const SHOTS = path.resolve(ROOT, 'shots');

(async () => {
  const browser = await chromium.launch({
    executablePath: CHROME,
    args: [
      '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
      '--ignore-gpu-blocklist', '--enable-webgl'
    ]
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });

  await page.goto(FILE);
  await page.waitForTimeout(2500);

  // 截图前统一清掉可能残留的文本选区（避免蓝底高亮出现在教程插图里）
  const clearSel = () => page.evaluate(() => {
    const s = window.getSelection();
    if (s) s.removeAllRanges();
  });
  const shoot = async (name) => {
    await clearSel();
    await page.screenshot({ path: path.join(SHOTS, name) });
  };

  // WebGL 是否真的画出了东西（采样画布中心像素）
  const glInfo = await page.evaluate(() => {
    const c = document.querySelector('#cv');
    const g = c.getContext('webgl');
    if (!g) return { webgl: false };
    const px = new Uint8Array(4);
    g.readPixels(Math.floor(c.width/2), Math.floor(c.height/2), 1, 1, g.RGBA, g.UNSIGNED_BYTE, px);
    return { webgl: true, centerPixel: Array.from(px), size: [c.width, c.height] };
  });

  const hotCount = await page.locator('.hot').count();
  const hotVisible = await page.locator('.hot:visible').count();
  const hotPos = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('.hot')).map(e => ({
      label: e.querySelector('.lab').textContent,
      display: e.style.display,
      left: e.style.left, top: e.style.top
    }));
  });

  await shoot('01_主界面.png');

  // 点击一个「可见的」热点 → 卡片
  const vis = page.locator('.hot:visible');
  const visN = await vis.count();
  if (visN > 0) await vis.first().click();
  await page.waitForTimeout(700);
  const cardVisible = await page.locator('#card').isVisible();
  await shoot('02_热点卡片.png');
  await page.click('#cClose');

  // 拖动视角 → 热点重新分布
  const box = await page.locator('#cv').boundingBox();
  await page.mouse.move(box.x + box.width/2, box.y + box.height/2);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width/2 - 420, box.y + box.height/2 - 60, { steps: 20 });
  await page.mouse.up();
  await page.waitForTimeout(900);
  await shoot('03_拖动视角.png');

  // 切场景
  await page.locator('.scn').nth(1).click();
  await page.waitForTimeout(2000);
  await shoot('04_切换场景.png');

  // 折叠面板
  await page.locator('.scn').nth(0).click();
  await page.waitForTimeout(1500);
  await page.click('#tgPanel');
  await page.waitForTimeout(800);
  await shoot('05_收起面板.png');
  await page.click('#tgPanel');

  // 内容编辑弹窗
  await page.click('#btnEdit');
  await page.waitForTimeout(600);
  await shoot('06_内容编辑.png');
  await page.click('#mClose');

  // 热点编辑模式
  await page.click('#btnMode');
  await page.waitForTimeout(600);
  await shoot('07_热点编辑模式.png');
  await page.click('#btnMode');

  // 转到边缘热点（西洋楼远影 u=68，初始视野外）
  await page.locator('.scn').nth(0).click();
  await page.waitForTimeout(1600);
  await page.waitForTimeout(3400);            // 等中央提示框自动消失，避免鼠标落在提示框上
  const b2 = await page.locator('#cv').boundingBox();
  const sx = b2.x + b2.width / 3, sy = b2.y + b2.height / 2;
  await page.mouse.move(sx, sy);
  await page.mouse.down();
  await page.mouse.move(sx + 700, sy, { steps: 25 });
  await page.mouse.up();
  await page.waitForTimeout(900);
  const edgeHot = await page.locator('.hot:visible').count();
  await shoot('08_转到边缘热点.png');

  console.log(JSON.stringify({
    errs: errs.slice(0, 8),
    glInfo,
    hotCount, hotVisible,
    hotPos,
    cardVisible,
    edgeHot
  }, null, 2));

  await browser.close();
})();
