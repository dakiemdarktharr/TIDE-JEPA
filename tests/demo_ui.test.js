// Execute the shipped page script in an isolated DOM simulation (no browser).
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '../tide_jepa/demo.html'), 'utf8');
const source = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const elements = Object.fromEntries([
  'form', 'submit', 'source', 'source-language', 'language', 'first', 'second',
  'output', 'status', 'submitted', 'checkpoint', 'quality-notice',
].map(id => [id, {value: '', disabled: false, textContent: '', className: ''}]));
elements.source.value = 'Original synthetic fixture';
elements['source-language'].value = elements.language.value = 'en';
elements.first.value = 'TIME:PAST';
const controls = ['source', 'source-language', 'language', 'first', 'second'].map(id => elements[id]);
elements.form.querySelectorAll = () => controls;
elements.form.addEventListener = (_event, handler) => { elements.form.submit = handler; };
let finishGeneration, requestCount = 0, captured;
const document = {
  querySelector: selector => elements[selector.slice(1)],
  getElementById: id => elements[id],
};
const fetch = (url, options) => {
  if (url === '/health') return Promise.resolve({json: async () => ({
    pilot_version: 'synthetic-ui-fixture', mode: 'tide', seed: 17,
    primary_quality_mode: 'tide', validation_gate_status: 'fail', max_new_tokens: 11,
  })});
  requestCount++;
  captured = JSON.parse(options.body);
  return new Promise(resolve => { finishGeneration = resolve; });
};
vm.runInNewContext(source, {document, fetch, console});
const flush = () => new Promise(resolve => setImmediate(resolve));

(async () => {
  await flush();
  assert.match(elements['quality-notice'].textContent, /không đạt cổng validation/);
  const submitted = elements.form.submit({preventDefault() {}});
  assert.equal(elements.submit.disabled, true);
  assert.ok(controls.every(control => !control.disabled), 'inputs remain editable while inference is pending');
  assert.equal(captured.max_new_tokens, 11);
  const originalSource = captured.source;
  elements.source.value = 'Changed synthetic fixture while pending';
  await elements.form.submit({preventDefault() {}});
  assert.equal(requestCount, 1, 'duplicate submission must not race the first reply');
  assert.ok(elements.submitted.textContent.includes(originalSource));
  finishGeneration({ok: true, json: async () => ({generated_text: 'synthetic reply', valid_utf8: true})});
  await submitted;
  assert.match(elements.output.textContent, /Kết quả thuộc yêu cầu trước/);
  assert.match(elements.output.textContent, /synthetic reply/);
  assert.match(elements.status.textContent, /biểu mẫu hiện tại chưa được xử lý/);
  assert.equal(elements.status.className, 'status stale');
  assert.equal(elements.submit.disabled, false);
  assert.ok(controls.every(control => !control.disabled));

  const failed = elements.form.submit({preventDefault() {}});
  finishGeneration({ok: false, json: async () => ({error: 'synthetic server failure'})});
  await failed;
  assert.equal(elements.status.textContent, 'synthetic server failure');
  assert.equal(elements.submit.disabled, false);
  assert.ok(controls.every(control => !control.disabled));
  console.log('Demo DOM checks passed: delayed reply, duplicate submit, budget, error recovery.');
})().catch(error => { console.error(error); process.exitCode = 1; });
