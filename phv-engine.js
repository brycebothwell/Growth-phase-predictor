/* PHV v2: trained on Berkeley and Harpenden; see training/README.md. */
(function(root){
'use strict';
function features(data){
 const a=data.map(p=>p.age),h=data.map(p=>p.h),n=a.length,span=a[n-1]-a[0],v=h.slice(1).map((z,i)=>(z-h[i])/(a[i+1]-a[i]));
 const x=a.map(z=>z-a[0]),mx=x.reduce((s,z)=>s+z,0)/n,my=h.reduce((s,z)=>s+z,0)/n;
 const slope=x.reduce((s,z,i)=>s+(z-mx)*(h[i]-my),0)/x.reduce((s,z)=>s+(z-mx)**2,0),intercept=my-slope*mx;
 const sd=Math.sqrt(h.reduce((s,z,i)=>s+(z-intercept-slope*x[i])**2,0)/n);
 return [a[n-1],h[n-1],(h[n-1]-h[0])/span,v[n-2],v[n-3],v[n-2]-v[n-3],span,n,sd];
}
function selectWindow(data){
 const sorted=data.map(p=>({age:Number(p.age),h:Number(p.h)})).sort((a,b)=>a.age-b.age);
 if(sorted.some(p=>!Number.isFinite(p.age)||!Number.isFinite(p.h)||p.h<50||p.h>220))throw Error('Check all ages and heights.');
 if(sorted.some((p,i)=>i&&p.age<=sorted[i-1].age))throw Error('Measurement dates must be distinct.');
 const recent=sorted.filter(p=>p.age>=sorted.at(-1).age-3.01).slice(-7);
 return {data:recent,omitted:sorted.length-recent.length};
}
function predict(input,sex,artifact){
 const selected=selectWindow(input),data=selected.data,d=artifact.domain;
 if(data.length<3)throw Error('At least three measurements within the latest three years are needed.');
 if(data.some(p=>p.age<d.minimum_age||p.age>d.maximum_age))throw Error('The trained model supports measurement ages 8–17 years.');
 const dt=data.slice(1).map((p,i)=>p.age-data[i].age),span=data.at(-1).age-data[0].age;
 if(dt.some(t=>t<d.minimum_interval-1e-6||t>d.maximum_interval+1e-6)||span<d.minimum_span-1e-6)throw Error('Use intervals of about 2.4–13.2 months and a total history of at least six months.');
 const vel=data.slice(1).map((p,i)=>(p.h-data[i].h)/dt[i]);
 if(vel.some(v=>v<-.5||v>18))throw Error('Check heights: an interval gives an implausible velocity.');
 const model=artifact.models[sex];if(!model)throw Error('Select the reference sex.');
 const x=features(data),xf=x.map(Math.fround);
 const estimates=model.trees.map(t=>{let i=0;while(t.l[i]!==-1)i=xf[t.f[i]]<=t.t[i]?t.l[i]:t.r[i];return t.v[i]});
 const peak=estimates.reduce((s,z)=>s+z,0)/estimates.length,r=model.radius_years,latest=data.at(-1).age;
 const outside=x.some((v,i)=>v<model.training_feature_min[i]-1e-5||v>model.training_feature_max[i]+1e-5);
 return {peak,lower:peak-r,upper:peak+r,latest,phase:latest<peak-.5?'Before estimated PHV':latest>peak+.5?'After estimated PHV':'Near estimated PHV',data,vel,omitted:selected.omitted,outside};
}
const api={features,selectWindow,predict};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.PHV=api;
})(typeof globalThis!=='undefined'?globalThis:this);
