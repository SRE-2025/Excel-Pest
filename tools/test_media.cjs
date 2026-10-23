/* Local browser QA only: never sends leads or analytics. */
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const output = process.env.EXCEL_QA_OUTPUT || path.resolve(__dirname, '../../seo-qa');
const origin = process.env.EXCEL_QA_URL || 'http://127.0.0.1:8765/';
fs.mkdirSync(output, {recursive:true});
(async()=>{
  const browser = await chromium.launch({headless:true, channel:process.env.EXCEL_BROWSER_CHANNEL || 'chrome'});
  const report = [];
  try {
    for (const mode of ['desktop','mobile','reduced','save-data','slow-2g','failed-video','no-js']) {
      const mobile = mode !== 'desktop';
      const context = await browser.newContext({viewport:{width:mobile?390:1440,height:900},
        deviceScaleFactor:mobile?2:1, isMobile:mobile, hasTouch:mobile,
        reducedMotion:mode === 'reduced'?'reduce':'no-preference', javaScriptEnabled:mode !== 'no-js'});
      const requests = [], errors = [];
      await context.route('**/*', route=>{
        const url = new URL(route.request().url());
        if (url.hostname !== new URL(origin).hostname) return route.abort();
        requests.push(url.pathname);
        if (mode === 'failed-video' && url.pathname.endsWith('.mp4')) return route.abort();
        return route.continue();
      });
      if (mode === 'save-data' || mode === 'slow-2g') await context.addInitScript(({mode})=>{
        Object.defineProperty(navigator,'connection',{value:{saveData:mode==='save-data',effectiveType:mode==='slow-2g'?'2g':'4g'},configurable:true});
      }, {mode});
      const page = await context.newPage();
      page.on('pageerror',e=>errors.push(e.message));
      await page.goto(origin,{waitUntil:'load'});
      const poster = page.locator('.hero-poster img');
      await poster.evaluate(img=>img.decode());
      assert(await poster.isVisible(),mode+' poster missing');
      assert.equal(await page.locator('[data-intro]').count(),0);
      const video = page.locator('video');
      if (['desktop','mobile'].includes(mode)) {
        await page.waitForFunction(()=>document.querySelector('video').currentTime > .1);
        assert((await video.getAttribute('src')).includes(mode+'.mp4'));
        await page.locator('.hero-motion-toggle').click();
        assert(await video.evaluate(v=>v.paused));
        await page.screenshot({path:path.join(output,'austin-'+mode+'.png')});
        await page.locator('.hero-motion-toggle').focus();
        await page.keyboard.press('Enter');
        await page.waitForFunction(()=>!document.querySelector('video').paused);
        await page.locator('.home-services').scrollIntoViewIfNeeded();
        await page.waitForFunction(()=>document.querySelector('video').paused);
        for (const img of await page.locator('.svc-card__photo').all()) {
          await img.scrollIntoViewIfNeeded(); await img.evaluate(i=>i.decode());
        }
        await page.locator('.home-services').screenshot({path:path.join(output,'cards-'+mode+'.png')});
        const card = page.locator('.home-services .svc-card').first();
        // Click the image corner, not the text link: full-card hit area must work.
        await card.click({position:{x:12,y:12}});
        await page.waitForURL('**/services/pest-control.html');
        assert.equal(requests.filter(p=>p.endsWith('.mp4')).some(p=>!p.endsWith(mode+'.mp4')),false);
      } else if (['reduced','save-data','slow-2g','no-js'].includes(mode)) {
        await page.waitForTimeout(350);
        assert.equal(requests.filter(p=>p.endsWith('.mp4')).length,0,mode+' unexpectedly loaded video');
        if (mode !== 'no-js') {
          await page.locator('.hero-motion-toggle').click();
          await page.waitForFunction(()=>document.querySelector('video').currentTime > .1);
        } else assert.equal(await page.locator('.hero-motion-toggle').isVisible(),false);
      } else {
        await page.waitForFunction(()=>document.querySelector('.hero-motion-toggle').hidden);
        assert.equal(await video.evaluate(v=>getComputedStyle(v).opacity),'0');
        assert(await poster.isVisible());
      }
      assert.deepEqual(errors,[],mode+' script errors');
      report.push({mode,result:'pass',videoRequests:requests.filter(p=>p.endsWith('.mp4'))});
      await context.close();
    }
    // Every service image decodes, and no detail page downloads the home video.
    const context = await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});
    await context.route('**/*',r=>new URL(r.request().url()).hostname===new URL(origin).hostname?r.continue():r.abort());
    const page = await context.newPage();
    const services = fs.readdirSync(path.resolve(__dirname,'../site/services')).filter(f=>f.endsWith('.html'));
    for (const filename of services) {
      await page.goto(origin+'services/'+filename);
      const image = page.locator('.service-image');
      await image.scrollIntoViewIfNeeded(); await image.evaluate(i=>i.decode());
      // naturalWidth is density-corrected when srcset uses width descriptors.
      assert(await image.evaluate(i=>i.naturalWidth>0 && /-(480|960)\.webp$/.test(i.currentSrc)),filename);
      assert.equal(await page.locator('video').count(),0);
    }
    await context.close();
    fs.writeFileSync(path.join(output,'media-browser-results.json'),JSON.stringify(report,null,2));
    console.log('PASS: responsive playback, pause/keyboard, offscreen pause, reduced motion, Save-Data, 2G, video failure, no-JS poster, full-card links and all 12 service images.');
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});
