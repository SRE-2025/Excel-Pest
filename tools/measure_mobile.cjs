/* Repeatable lab measurement, not a Lighthouse score or field Core Web Vitals. */
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const path = require('node:path');
(async()=>{
  const browser = await chromium.launch({headless:true,channel:process.env.EXCEL_BROWSER_CHANNEL || 'chrome'});
  const samples=[];
  try {
    const targets = process.env.EXCEL_BASELINE_URL ? [['before',process.env.EXCEL_BASELINE_URL],['after','http://127.0.0.1:8765/']] : [['after','http://127.0.0.1:8765/']];
    for(const [version,url] of targets) for(let run=1;run<=3;run++) {
      const context=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true});
      const page=await context.newPage();
      const session=await context.newCDPSession(page);
      await session.send('Network.enable');
      await session.send('Network.setCacheDisabled',{cacheDisabled:true});
      await session.send('Network.emulateNetworkConditions',{offline:false,latency:150,downloadThroughput:200000,uploadThroughput:93750,connectionType:'cellular4g'});
      await session.send('Emulation.setCPUThrottlingRate',{rate:4});
      let transferred=0; const failures=[];
      session.on('Network.dataReceived',e=>transferred+=e.encodedDataLength);
      page.on('requestfailed',r=>failures.push({url:r.url(),error:r.failure().errorText}));
      await page.addInitScript(()=>{
        window.lab={lcp:0,cls:0,longTaskMs:0};
        new PerformanceObserver(list=>list.getEntries().forEach(e=>window.lab.lcp=e.startTime)).observe({type:'largest-contentful-paint',buffered:true});
        new PerformanceObserver(list=>list.getEntries().forEach(e=>{if(!e.hadRecentInput)window.lab.cls+=e.value;})).observe({type:'layout-shift',buffered:true});
        new PerformanceObserver(list=>list.getEntries().forEach(e=>window.lab.longTaskMs+=e.duration)).observe({type:'longtask',buffered:true});
      });
      await page.goto(url,{waitUntil:'domcontentloaded'});
      await page.waitForTimeout(10000);
      const lab=await page.evaluate(()=>({...window.lab,firstContentfulPaint:performance.getEntriesByName('first-contentful-paint')[0]?.startTime,videoPlaying:!!document.querySelector('video')?.currentTime}));
      const sample={version,run,...lab,transferredBytesAt10s:transferred,failures};samples.push(sample);console.log(JSON.stringify(sample));
      await context.close();
    }
    fs.writeFileSync(path.resolve(__dirname,'../../seo-qa/mobile-lab.json'),JSON.stringify({conditions:'Chrome; 390x844 DPR2; 4x CPU; 1.6 Mbps down/0.75 Mbps up, 150ms simulated latency; fresh context/cache disabled; sample 10s after DOMContentLoaded. Local HTML; before version retains external font/media origins. Lab observations, not field data.',samples},null,2));
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
