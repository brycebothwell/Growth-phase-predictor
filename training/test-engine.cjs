const fs=require('fs'),assert=require('assert'),path=require('path'),root=path.join(__dirname,'..'),engine=require('../phv-engine.js');
const model=JSON.parse(fs.readFileSync(path.join(root,'phv-model.json'))),cases=JSON.parse(fs.readFileSync(path.join(__dirname,'parity-cases.json')));
let max=0;for(const c of cases){const r=engine.predict(c.data,c.sex,model);max=Math.max(max,Math.abs(r.peak-c.expected));assert(Math.abs(r.peak-c.expected)<1e-9)}
assert.throws(()=>engine.predict([{age:11,h:140},{age:11,h:142},{age:12,h:150}],'male',model),/distinct/);
assert.throws(()=>engine.predict([{age:11,h:140},{age:11.05,h:142},{age:12,h:150}],'male',model),/intervals/);
assert.throws(()=>engine.predict([{age:5,h:110},{age:5.5,h:113},{age:6,h:116}],'male',model),/8–17/);
const extra=Array.from({length:9},(_,i)=>({age:10+i*.4,h:140+i*2}));assert.equal(engine.selectWindow(extra).data.length,7);
console.log(JSON.stringify({heldoutParityCases:cases.length,maximumPythonJavaScriptDifference:max,validationTests:'passed'}));
