/* Optional browser QA. Set PLAYWRIGHT_MODULE to an installed Playwright module. */
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const output = process.env.EXCEL_QA_OUTPUT || path.resolve(__dirname, '../../seo-qa');
fs.mkdirSync(output, {recursive:true});
(async () => {
  const browser = await chromium.launch({headless:true, channel:process.env.EXCEL_BROWSER_CHANNEL || 'chrome'});
  try {
    const context = await browser.newContext({reducedMotion:'reduce'});
    // No form, analytics, maps or video requests leave this local test.
    await context.route('**/*', route => {
      const url = new URL(route.request().url());
      if (url.hostname === '127.0.0.1') return route.continue();
      return route.abort();
    });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    const services = fs.readdirSync(path.resolve(__dirname, '../site/services')).filter(p=>p.endsWith('.html')).map(p=>'services/'+p);
    const routes = ['index.html','pest-library.html','insights/central-texas-pest-calendar.html','insights/fire-ants-central-texas-yard.html','insights/cockroaches-central-texas-kitchen.html','locations/buda.html','contact.html?service=rodent-exclusion', ...services];
    for (const width of [390,1440]) {
      await page.setViewportSize({width,height:900});
      for (const route of routes) {
        const response = await page.goto('http://127.0.0.1:8765/'+route,{waitUntil:'domcontentloaded'});
        assert.equal(response.status(),200);
        assert.equal(await page.locator('h1').count(),1);
        const overflow = await page.evaluate(()=>document.documentElement.scrollWidth > innerWidth + 1);
        if (overflow) {
          console.log(await page.evaluate(()=>Array.from(document.querySelectorAll('body *')).filter(e=>e.getBoundingClientRect().right > innerWidth + 1).map(e=>({tag:e.tagName,class:e.className,width:e.getBoundingClientRect().width})).slice(0,12)));
          await page.screenshot({path:path.join(output,'overflow-'+width+'.png')});
        }
        assert.equal(overflow,false,route+' overflows at '+width);
        assert.equal(await page.locator('script[src*="googletagmanager"]').count(),0,'local test must not load GA4');
        if (route.startsWith('contact')) assert.equal(await page.locator('[name=service]').inputValue(),'Rodents & Wildlife');
      }
      await page.goto('http://127.0.0.1:8765/services/pest-control.html');
      if (width === 1440) {
        const media = await page.locator('.service-side-media .img-slot').boundingBox();
        const prose = await page.locator('.service-layout > .prose').boundingBox();
        assert(media.width <= 431); assert(media.x > prose.x + prose.width);
        assert(Math.abs(media.y-prose.y) < 3);
      }
      await page.locator('.service-layout').screenshot({path:path.join(output,'service-'+width+'.png')});
      await page.goto('http://127.0.0.1:8765/pest-library.html');
      await page.screenshot({path:path.join(output,'library-'+width+'.png'),fullPage:false});
    }
    assert.deepEqual(errors,[]);
    console.log(`PASS: ${routes.length} routes at 390px and 1440px; no overflow or script errors; sidebar size/alignment and service preselection verified. Screenshots: ${output}`);
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});
