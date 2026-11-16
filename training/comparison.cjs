// Same-case v1/v2 comparison: no training, fitting or tuning.
const fs=require('fs'),path=require('path'),root=path.join(__dirname,'..'),vm=require('vm');
const html=fs.readFileSync(path.join(root,'archive/height-only-v1.html'),'utf8'),code=html.slice(html.indexOf('function V('),html.indexOf('function plot(')),ctx={};vm.createContext(ctx);vm.runInContext(code,ctx);
const engine=require('../phv-engine.js'),model=JSON.parse(fs.readFileSync(path.join(root,'phv-model.json'))),cases=JSON.parse(fs.readFileSync(path.join(__dirname,'raw/evaluation_cases.json'))).filter(c=>c.data.length===3);
for(const c of cases){c.legacy=ctx.predict(c.data,c.sex).q[1];c.trained=engine.predict(c.data,c.sex,model).peak;}
fs.writeFileSync(path.join(__dirname,'raw/v1-comparison-results.json'),JSON.stringify(cases));console.log(cases.length+' matched three-point cases evaluated.');
