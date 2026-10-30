const { chromium } = require('playwright');
const path = require('path');
const CHROME = 'C:/Users/Administrator/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe';
const SRC = path.resolve(__dirname, '专题_360VR互动网页_零基础操作手册.html');
const OUT = path.resolve(__dirname, '专题_360VR互动网页_零基础操作手册.pdf');
(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  const page = await browser.newPage();
  await page.goto('file:///' + encodeURI(SRC.replace(/\\/g, '/')), { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  await page.pdf({
    path: OUT,
    format: 'A4',
    printBackground: true,
    margin: { top: '14mm', bottom: '14mm', left: '12mm', right: '12mm' },
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;text-align:center;font-size:9px;color:#9aa4b2;">第 <span class="pageNumber"></span> / <span class="totalPages"></span> 页 · 做一个能转的 360 课堂网页 · 零基础操作手册</div>'
  });
  await browser.close();
  const fs = require('fs');
  console.log('PDF 已生成', (fs.statSync(OUT).size / 1024 / 1024).toFixed(2), 'MB');
})();
