/* Run with node tools/test_tracking.cjs. All network/analytics calls are mocked. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const script = fs.readFileSync(path.join(__dirname, '../site/js/main.js'), 'utf8');

function harness(options = {}) {
  const events = [], requests = [], handlers = {}, formHandlers = {}, timers = [];
  let nativePosts = 0;
  const location = { hostname: options.hostname || 'www.excelpest-lawncontrol.com', pathname: (options.base || '') + '/contact.html', search: options.search || '', href: '' };
  const values = { name: 'Test Person', email: 'test@example.test', phone: '5551234567', zip: '78610', message: 'private message', service: 'Not sure / other' };
  const form = {
    elements: Object.fromEntries(Object.entries(values).map(([k,v]) => [k, {value: v, focus(){}}])),
    getAttribute(name) { return { 'data-ajax-endpoint': 'https://mock.invalid/ajax', 'data-lead-sheet': 'https://mock.invalid/sheet', action: 'https://mock.invalid/post' }[name]; },
    querySelector(selector) { return selector === '.hp' ? { value: options.bot ? 'spam' : '' } : {textContent: ''}; },
    addEventListener(name, fn) { formHandlers[name] = fn; },
    checkValidity() { return !options.invalid; }, reportValidity() {},
  };
  const document = { addEventListener(name, fn) { handlers[name] = fn; }, querySelector(s) { return s === 'form[data-estimate]' ? form : null; }, querySelectorAll() { return []; } };
  const fetch = async (url) => {
    requests.push(url);
    if (options.reject && url.endsWith('/ajax')) throw Error('offline');
    return {ok: options.httpError ? false : true, json: async () => ({ success: options.success === undefined ? true : options.success })};
  };
  const window = { __BASE__: options.base || '', location, fetch, setTimeout(fn){ timers.push(fn); }, gtag(type, name, data){ events.push({type,name,data}); } };
  vm.runInNewContext(script, {window, location, document, fetch, URLSearchParams, FormData: class {append(){}}, HTMLFormElement: {prototype:{submit(){nativePosts++;}}}, Date, Object, String});
  return {form, events, requests, location, timers, nativePosts:()=>nativePosts,
    input(){formHandlers.input();}, submit(){formHandlers.submit({preventDefault(){}});},
    click(href, place='content') { handlers.click({ target: { closest(){ return {getAttribute(){return href;}, pathname: href.startsWith('/') ? href : '', closest(selector){return selector.split(',').some(s=>s.trim() === place);}};}}}); }
  };
}
const flush = () => new Promise(resolve => setImmediate(resolve));
(async () => {
  const html = fs.readFileSync(path.join(__dirname,'../site/contact.html'),'utf8');
  assert(html.includes('class="mobile-actionbar"'), 'test must cover the current rendered mobile bar');
  const headScript = html.match(/<!-- Google Analytics 4[^]*?<script>([^]*?)<\/script>/)[1];
  for (const hostname of ['localhost','sre-2025.github.io','www.excelpest-lawncontrol.com','excelpest-lawncontrol.com']) {
    const appended=[];
    const runtime = {location:{hostname}, document:{createElement(){return {};},head:{appendChild(e){appended.push(e);}}},Date};
    runtime.window=runtime;
    vm.runInNewContext(headScript,runtime);
    assert.equal(appended.length,hostname.includes('excelpest-lawncontrol.com') ? 1 : 0);
    assert.equal(runtime.dataLayer.length,appended.length ? 2 : 0);
  }
  // Match both the current visible mobile bar and the retained legacy markup.
  // These are click placements, not completed calls or booked jobs.
  for (const [container, expected] of [['.mobile-actionbar','mobile_bar'],['.mobile-bar','mobile_bar'],['header','header'],['footer','footer'],['content','content']]) {
    const placed = harness();
    placed.click('tel:+15122915900',container);
    placed.click('/contact.html',container);
    assert.deepEqual(placed.events.map(e=>[e.name,e.data.link_placement]),[
      ['phone_click',expected],['estimate_cta_click',expected]
    ], 'incorrect attribution for '+container);
    assert.equal(placed.requests.length,0);
  }
  let h = harness({search:'?service=rodent-exclusion'});
  assert.equal(h.form.elements.service.value, 'Rodents & Wildlife');
  h.input(); h.input();
  h.click('tel:+15122915900','header'); h.click('sms:+15122915900'); h.click('mailto:office@example.test'); h.click('/contact.html');
  assert.deepEqual(h.events.map(e=>e.name), ['estimate_form_start','phone_click','sms_click','email_click','estimate_cta_click']);
  h.submit(); h.submit(); await flush();
  assert.equal(h.requests.length, 2, 'only one email attempt and one sheet attempt');
  assert.equal(h.events.filter(e=>e.name === 'generate_lead').length, 1);
  assert.equal(h.events.at(-1).data.service_category, 'rodent-exclusion');
  assert(!JSON.stringify(h.events).includes('test@example.test'));
  assert(!JSON.stringify(h.events).includes('private message'));
  h.events.at(-1).data.event_callback(); h.timers.forEach(fn=>fn());
  assert.equal(h.location.href, '/thank-you.html');
  for (const options of [{bot:true}, {invalid:true}]) {
    h = harness(options); h.submit(); await flush();
    assert.equal(h.requests.length, 0); assert.equal(h.events.length, 0);
  }
  for (const options of [{success:false}, {success:'false'}, {httpError:true}, {reject:true}]) {
    h = harness(options); h.submit(); await flush();
    assert.equal(h.nativePosts(), 1); assert.equal(h.events.at(-1).name, 'estimate_form_fallback');
    assert(!h.events.some(e=>e.name === 'generate_lead'));
  }
  h = harness({success:'true'}); h.submit(); await flush();
  assert.equal(h.events.at(-1).name, 'generate_lead');
  h = harness({hostname:'sre-2025.github.io',base:'/Excel-Pest',search:'?service=unknown'});
  assert.equal(h.form.elements.service.value,'Not sure / other');
  h.click('tel:+15122915900'); h.submit(); await flush();
  assert.equal(h.events.length,0); assert.equal(h.location.href,'/Excel-Pest/thank-you.html');
  console.log('PASS: contact clicks, one-time form start, preselection, accepted/rejected responses, double-submit protection, honeypot, validation, fallback, privacy and preview paths. No real emails or analytics sent.');
})().catch(error=>{console.error(error);process.exitCode=1;});
