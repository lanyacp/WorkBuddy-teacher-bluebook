// 数字人助教原型自检：加载页面、查 JS 报错、验证题库/口型/字幕逻辑
const { chromium } = require('playwright');
const path = require('path');

const CHROME = 'C:/Users/Administrator/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe';
const FILE = 'file:///' + path.resolve(__dirname, '数字人助教_单文件版.html').replace(/\\/g, '/');

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  const page = await browser.newPage({ viewport: { width: 1440, height: 980 } });

  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));

  await page.goto(FILE);
  await page.waitForTimeout(800);

  // 1) 题库渲染
  const qaCount = await page.locator('#qaList .qaItem').count();
  const tagCount = await page.locator('#quickTags .tag').count();

  // 2) 口型引擎是否真的在动：读 svgMouth 的 ry，连续采样
  const sample = async () => page.evaluate(() =>
    parseFloat(document.querySelector('#svgMouth').getAttribute('ry')));
  const r0 = await sample();

  // 手动触发一次张嘴脉冲（模拟语音边界事件）
  await page.evaluate(() => { window.pulse && window.pulse(); });
  await page.waitForTimeout(120);
  const r1 = await sample();
  await page.waitForTimeout(600);
  const r2 = await sample();

  // 3) 点击"试说一句"，看字幕与状态
  await page.click('#btnDemo');
  await page.waitForTimeout(500);
  const sub = await page.locator('#subtitle').textContent();
  const status = await page.locator('#status').textContent();

  // 4) 点第一个题库条目，看是否填入答案
  await page.locator('#quickTags .tag').first().click();
  await page.waitForTimeout(300);
  const answerText = await page.locator('#answer').inputValue();

  // 5) 语音列表
  const voiceInfo = await page.evaluate(() => ({
    has: 'speechSynthesis' in window,
    n: (window.speechSynthesis ? speechSynthesis.getVoices() : []).length
  }));

  await page.screenshot({ path: path.resolve(__dirname, '自检截图.png'), fullPage: false });

  // 6) 全屏投屏布局（再截一张 1920x1080）
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.resolve(__dirname, '自检截图_1080p.png') });

  // 7) 投屏模式：右侧应隐藏，数字人+字幕居中放大
  await page.click('#btnProj');
  await page.waitForTimeout(400);
  const proj = await page.evaluate(() => ({
    hasClass: document.body.classList.contains('projector'),
    rightHidden: getComputedStyle(document.querySelector('.colRight')).display === 'none',
    settingHidden: getComputedStyle(document.querySelector('.settingCard')).display === 'none',
    subFontSize: getComputedStyle(document.querySelector('#subtitle')).fontSize,
    projBarVisible: getComputedStyle(document.querySelector('#projBar')).display !== 'none'
  }));
  // 投屏下控制按钮已隐藏，直接用投屏输入条走一次提问（验证闭环）
  await page.fill('#projAsk', '什么是光的折射？');
  await page.press('#projAsk', 'Enter');
  await page.waitForTimeout(600);
  const projSub = await page.locator('#subtitle').textContent();
  await page.screenshot({ path: path.resolve(__dirname, '自检截图_投屏模式.png') });
  // Esc 退出
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
  const projOff = await page.evaluate(() => !document.body.classList.contains('projector'));

  console.log(JSON.stringify({
    jsErrors: errors,
    qaCount, tagCount,
    mouthRy: { init: r0, afterPulse: r1, afterDecay: r2 },
    mouthWorks: r1 > r0,
    subtitle: sub,
    status,
    answerFilled: answerText.slice(0, 30),
    voiceInfo,
    projector: proj,
    projectorAskResult: projSub,
    projectorExitByEsc: projOff
  }, null, 2));

  await browser.close();
})();
