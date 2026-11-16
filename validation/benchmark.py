"""Run with Python containing pandas and rdata, and Node.js on PATH.
Downloads public corrected SITAR Berkeley data; does not tune the predictor.
"""
from pathlib import Path
import urllib.request, json, subprocess, tempfile
import pandas as pd
import numpy as np
import rdata
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'berkeley.rda'
 urllib.request.urlretrieve('https://raw.githubusercontent.com/cran/sitar/master/data/berkeley.rda',p)
 df=rdata.read_rda(p)['berkeley']
 cases=[]
 for ident,g in df.groupby('id',observed=True):
  g=g.dropna(subset=['height']).sort_values('age');g=g[(g.age>=8)&(g.age<=18)]
  if len(g)<16 or g.age.min()>8.5 or g.age.max()<17:continue
  a=g.age.to_numpy();h=g.height.to_numpy();dt=np.diff(a);v=np.diff(h)/dt
  if np.any(dt<=0) or np.any(dt>1) or np.any(v<-.5) or np.any(v>18):continue
  sex='male' if str(g.sex.iloc[0])=='1' else 'female'
  # Reference is the midpoint of the largest observed interval velocity.
  mx=np.flatnonzero(np.isclose(v,v.max()))
  if min(mx)==0 or max(mx)==len(v)-1:continue
  ref=float(np.mean((a[mx]+a[mx+1])/2))
  for stage,end in enumerate(([12,13,14] if sex=='male' else [10,11,12])):
   target=[end-1,end-.5,end];data=[]
   for age in target:
    rows=g[np.isclose(g.age,age)]
    if len(rows)!=1:break
    data.append({'age':float(age),'h':float(rows.height.iloc[0])})
   if len(data)==3:cases.append(dict(id=str(ident),sex=sex,stage=stage,end=end,data=data,reference=ref))
 html=(root/'index.html').read_text()
 code=html[html.index('function V('):html.index('function plot(')]
 js=Path(tmp)/'run.cjs'; inp=Path(tmp)/'cases.json';inp.write_text(json.dumps(cases))
 js.write_text("const fs=require('fs');\n"+code+"\nconst cases=JSON.parse(fs.readFileSync(process.argv[2])); for(const c of cases){const r=predict(c.data,c.sex);c.predicted=r.q[1];c.lower=r.q[0];c.upper=r.q[2];c.phase=r.ph.indexOf(Math.max(...r.ph));} console.log(JSON.stringify(cases));")
 out=json.loads(subprocess.check_output(['node',str(js),str(inp)]))
 rows=[]
 for c in out:
  rows.append(dict(subject=c['id'],sex=c['sex'],stage=c['stage'],last_age=c['end'],inputs=json.dumps(c['data']),predicted_age=c['predicted'],reference_age=c['reference'],error_years=c['predicted']-c['reference'],before_peak=c['end']<c['reference'],lower=c['lower'],upper=c['upper']))
 result=pd.DataFrame(rows);result.to_csv(root/'validation/results.csv',index=False)
 for (sex,stage),g in result.groupby(['sex','stage']):
  e=g.error_years
  print(sex,stage,'N',len(g),'MAE',round(abs(e).mean(),3),'bias',round(e.mean(),3),'within6mo',round((abs(e)<=.5).mean()*100,1),'within1y',round((abs(e)<=1).mean()*100,1),'prepeakN',g.before_peak.sum())
 print('unique',result.subject.nunique(),'cases',len(result))
 print('prospective subset')
 for (sex,stage),g in result[result.before_peak].groupby(['sex','stage']):print(sex,stage,len(g),round(abs(g.error_years).mean(),3))
