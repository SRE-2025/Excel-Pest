/* Exercise real rendered links with analytics intercepted and navigation stopped.
   Optional browser QA; no customer forms are submitted and no events are sent. */
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../site');
const live = process.env.EXCEL_QA_LIVE === '1';
const production = 'https://www.excelpest-lawncontrol.com';
const preview = 'https://sre-2025.github.io';
const mime = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.webp':'image/webp','.woff2':'font/woff2'};

(async()=>{
  const browser = await chromium.launch({headless:true,channel:process.env.EXCEL_BROWSER_CHANNEL || 'chrome'});
  const results = [];
  try {
    for (const [origin, width] of [[production,390],[production,760],[production,1440],[preview,390]]) {
      const context = await browser.newContext({viewport:{width,height:844},reducedMotion:'reduce'});
      const blocked = [];
      await context.route('**/*', async route=>{
        const request = route.request(), url = new URL(request.url());
        // Never load Google tags, remote form backends, or other third-party hosts.
        if (request.method() !== 'GET' || url.origin !== origin) {
          blocked.push(request.url()); return route.abort();
        }
        if (live) return route.continue();
        const pathname = decodeURIComponent(url.pathname.replace(/^\/Excel-Pest(?=\/)/,''));
        const file = path.resolve(root, '.' + (pathname === '/' ? '/index.html' : pathname));
        if (!file.startsWith(root + path.sep) || !fs.existsSync(file)) return route.fulfill({status:404,body:'Not found'});
        return route.fulfill({status:200,contentType:mime[path.extname(file)] || 'application/octet-stream',body:fs.readFileSync(file)});
      });
      const page = await context.newPage();
      const errors=[]; page.on('pageerror',e=>errors.push(e.message));
      await page.goto(origin + (origin===preview?'/Excel-Pest/':'/'),{waitUntil:'load'});
      await page.evaluate(()=>{
        window.testEvents=[];
        window.gtag=(type,name,data)=>window.testEvents.push({type,name,data});
        // Stop tel:/mailto: handlers and navigation, but let the event bubble to tracking.
        document.addEventListener('click',event=>{if(event.target.closest('a'))event.preventDefault();},true);
      });
      const selectors = width < 821
        ? ['.mobile-actionbar .mab--call','.mobile-actionbar .mab--est']
        : ['header .btn--call','header .btn--primary'];
      for (const selector of selectors) {
        const link=page.locator(selector).first();
        assert(await link.isVisible(),selector+' must be visible');
        // Actual pointer hit-testing verifies that the visible bar, not covered legacy markup, is tested.
        await link.click();
      }
      // The estimate action must also be measurable when activated with a keyboard.
      await page.locator(selectors[1]).first().focus(); await page.keyboard.press('Enter');
      const events=await page.evaluate(()=>window.testEvents);
      if (origin===production) {
        const expected = width < 821 ? 'mobile_bar' : 'header';
        assert.deepEqual(events.map(e=>[e.name,e.data.link_placement]),[
          ['phone_click',expected],['estimate_cta_click',expected],['estimate_cta_click',expected]
        ]);
        assert(events.every(e=>!Object.keys(e.data).some(k=>/phone|email|name|zip|message|url/i.test(k))));
      } else assert.deepEqual(events,[], 'preview must not record production events');
      assert.deepEqual(errors,[]);
      results.push({origin,width,mode:live?'live':'local files',events:events.map(e=>[e.name,e.data.link_placement]),blockedThirdPartyRequests:blocked.length});
      await context.close();
    }
    console.log(JSON.stringify(results,null,2));
    console.log('PASS: visible mobile and desktop buttons, keyboard activation and preview isolation. No leads or analytics sent.');
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});
