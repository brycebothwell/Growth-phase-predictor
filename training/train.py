"""PHV timing research model, v2. Python: numpy pandas scipy scikit-learn rdata.
Usage: python training/train.py [--download]
Raw data remain ignored locally. Public sources and retrieval implemented below.
"""
from pathlib import Path
import json, re, urllib.request, zipfile, io, hashlib, sys, warnings
import numpy as np
import pandas as pd
from scipy.interpolate import UnivariateSpline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupKFold
import rdata
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'training/raw'; RAW.mkdir(exist_ok=True)
SEED=20261116
FEATURES=['latest_age','latest_height_cm','overall_velocity','latest_velocity','previous_velocity','velocity_change','span_years','observation_count','height_line_residual_sd']
def download():
 urllib.request.urlretrieve('https://raw.githubusercontent.com/cran/sitar/master/data/berkeley.rda',RAW/'berkeley.rda')
 base='https://datacatalogue.ukdataservice.ac.uk'
 def get(u):return urllib.request.urlopen(u,timeout=60).read()
 page=get(base+'/studies/study/9330').decode(); asset=re.search(r'src="([^"]+index[^\"]+\.js)"',page)[1]
 main=get(base+asset).decode();cfg=re.search(r'import\("\./(amplifyconfig_prod[^\"]+\.js)"',main)[1]
 config=get(base+'/assets/'+cfg).decode();endpoint=re.findall(r'endpoint:"([^"]+)"',config)[-1];key=re.findall(r'apiKey:"([^"]+)"',config)[-1]
 def gql(query,variables):
  req=urllib.request.Request(endpoint,json.dumps(dict(query=query,variables=variables)).encode(),{'Content-Type':'application/json','x-api-key':key})
  return json.load(urllib.request.urlopen(req,timeout=60))['data']
 items=gql('query($BucketName:String!,$FriendlyId:String!){getFileList(BucketName:$BucketName,FriendlyId:$FriendlyId){Format Key Size}}',{'BucketName':'','FriendlyId':'9330'})['getFileList']
 item=next(i for i in items if i['Format']=='TAB');url=gql('query($BucketName:String!,$Key:String!){getFileUrl(BucketName:$BucketName,Key:$Key)}',{'BucketName':'','Key':item['Key']})['getFileUrl']
 z=zipfile.ZipFile(io.BytesIO(get(url)));name=next(n for n in z.namelist() if n.endswith('harpenden_ukds.tab'));(RAW/'harpenden.tab').write_bytes(z.read(name))
def features(data):
 a=np.array([r['age'] for r in data]);h=np.array([r['h'] for r in data]);dt=np.diff(a);v=np.diff(h)/dt
 line=np.polyfit(a-a[0],h,1);res=h-np.polyval(line,a-a[0])
 return [a[-1],h[-1],(h[-1]-h[0])/(a[-1]-a[0]),v[-1],v[-2],v[-1]-v[-2],a[-1]-a[0],len(a),np.sqrt(np.mean(res**2))]
def subjects():
 with warnings.catch_warnings():
  warnings.simplefilter('ignore');b=rdata.read_rda(RAW/'berkeley.rda')['berkeley'].rename(columns={'height':'h'})
 h=pd.read_csv(RAW/'harpenden.tab',sep='\t',na_values=[' ']).rename(columns={'ht':'h'})
 people=[];exclusions={};source_counts={}
 for name,d in [('Berkeley',b),('Harpenden',h)]:
  counts={};source_counts[name]={'participants':int(d.id.nunique()),'rows':len(d)}
  for ident,g in d.groupby('id',observed=True):
   g=g[['sex','age','h']].dropna().sort_values('age');g=g[(g.age>=7)&(g.age<=19)]
   segs=np.split(np.arange(len(g)),np.where(np.diff(g.age)>1.1)[0]+1);why='coverage'
   for ix in sorted(segs,key=len,reverse=True):
    z=g.iloc[ix]
    if len(z)<8:continue
    a=z.age.to_numpy();ht=z.h.to_numpy();sex=int(z.sex.iloc[0])
    if a[0]>(11.5 if sex==1 else 10.5) or a[-1]<(15.5 if sex==1 else 14) or a[-1]-a[0]<4:continue
    if np.any(np.diff(a)<=0):why='duplicate';continue
    v=np.diff(ht)/np.diff(a)
    if min(v)<-1 or max(v)>18:why='implausible_velocity';continue
    grid=np.arange(a[0]+.5,a[-1]-.5,.01);peaks=[];vs=[]
    for sd in [.2,.3,.5]:
     s=UnivariateSpline(a,ht,s=len(a)*sd**2);vals=s.derivative()(grid);peaks.append(float(grid[np.argmax(vals)]));vs.append(vals)
    peak=peaks[1];pv=max(vs[1])
    if peak<a[0]+1 or peak>a[-1]-1 or vs[1][-1]>3.5 or pv<(6 if sex==1 else 5):why='unbracketed';continue
    if max(peaks)-min(peaks)>.75:why='unstable_reference';continue
    cases=[];seen=set()
    for end in range(2,len(z)):
     for n in [3,4,5,6,7]:
      for stride in [1,2]:
       start=end-(n-1)*stride
       if start<0:continue
       idx=tuple(range(start,end+1,stride))
       if idx in seen:continue
       seen.add(idx);aa=a[list(idx)];hh=ht[list(idx)]
       # Common input domain for both sexes, actual measured points only.
       if aa[0]<8 or aa[-1]>17 or aa[-1]-aa[0]<.5 or aa[-1]-aa[0]>3.01 or min(np.diff(aa))<.2 or max(np.diff(aa))>1.1:continue
       data=[{'age':float(x),'h':float(y)} for x,y in zip(aa,hh)]
       cases.append({'data':data,'x':features(data),'n':n,'latest_age':float(aa[-1])})
    if not cases:why='no_input_windows';continue
    people.append({'id':name+':'+str(ident),'cohort':name,'sex':'male' if sex==1 else 'female','peak':peak,'peak_velocity':float(pv),'reference_sensitivity':max(peaks)-min(peaks),'cases':cases});why='included';break
   counts[why]=counts.get(why,0)+1
  exclusions[name]=counts
 return people,exclusions,source_counts
def split_people(people):
 rng=np.random.default_rng(SEED)
 for cohort in ['Berkeley','Harpenden']:
  for sex in ['male','female']:
   group=sorted([p for p in people if p['cohort']==cohort and p['sex']==sex],key=lambda p:p['id']);rng.shuffle(group);n=len(group);a=int(n*.6);b=a+int(n*.2)
   for i,p in enumerate(group):p['split']='train' if i<a else 'calibration' if i<b else 'test'
def flatten(people):
 X=[];y=[];groups=[];weights=[];meta=[]
 for p in people:
  for c in p['cases']:
   X.append(c['x']);y.append(p['peak']);groups.append(p['id']);weights.append(1/len(p['cases']));meta.append((p,c))
 return np.array(X),np.array(y),np.array(groups),np.array(weights),meta
def fit(people,params):
 X,y,g,w,m=flatten(people)
 return RandomForestRegressor(n_estimators=100,random_state=SEED,n_jobs=1,**params).fit(X,y,sample_weight=w)
def metrics(records):
 if not records:return None
 d=pd.DataFrame(records);per=d.groupby('id').error.apply(lambda x:abs(x).mean());rng=np.random.default_rng(SEED);boot=np.mean(rng.choice(per.to_numpy(),(2000,len(per)),replace=True),axis=1)
 return {'participants':len(per),'windows':len(d),'mae_months_subject_weighted':float(per.mean()*12),'mae_bootstrap95_months':[float(x*12) for x in np.quantile(boot,[.025,.975])],'bias_months_subject_weighted':float(d.groupby('id').error.mean().mean()*12),'within6months_subject_weighted':float(d.assign(ok=abs(d.error)<=.5).groupby('id').ok.mean().mean()),'coverage_subject_weighted':float(d.groupby('id').covered.mean().mean()),'baseline_mae_months_subject_weighted':float(d.groupby('id').baseline_error.apply(lambda x:abs(x).mean()).mean()*12)}
def tree_json(t):
 tr=t.tree_
 return {'f':tr.feature.tolist(),'t':tr.threshold.tolist(),'l':tr.children_left.tolist(),'r':tr.children_right.tolist(),'v':tr.value[:,0,0].tolist()}
def main():
 if '--download' in sys.argv:download()
 people,exclusions,counts=subjects();split_people(people)
 artifact={'version':'2.0.0','date':'2026-11-16','target':'age at smoothed statural peak height velocity','features':FEATURES,'domain':{'minimum_age':8,'maximum_age':17,'minimum_interval':.2,'maximum_interval':1.1,'minimum_span':.5,'maximum_span':3.01,'minimum_points':3,'maximum_points':7},'models':{}}
 report={'seed':SEED,'source_counts':counts,'exclusions':exclusions,'splits':{},'models':{},'test_metrics':{},'data_sha256':{n:hashlib.sha256((RAW/n).read_bytes()).hexdigest() for n in ['berkeley.rda','harpenden.tab']}}
 all_records=[];parity=[];evaluation_cases=[]
 for sex in ['male','female']:
  ps=[p for p in people if p['sex']==sex];train=[p for p in ps if p['split']=='train'];cal=[p for p in ps if p['split']=='calibration'];test=[p for p in ps if p['split']=='test']
  report['splits'][sex]={co:{sp:sum(p['cohort']==co and p['split']==sp for p in ps) for sp in ['train','calibration','test']} for co in ['Berkeley','Harpenden']}
  X,y,g,w,meta=flatten(train);candidates=[]
  for depth,leaf in [(3,10),(5,10),(7,10),(5,20)]:
   losses=[]
   for tr,va in GroupKFold(4).split(X,y,g):
    m=RandomForestRegressor(n_estimators=100,max_depth=depth,min_samples_leaf=leaf,random_state=SEED,n_jobs=1).fit(X[tr],y[tr],sample_weight=w[tr]);e=abs(m.predict(X[va])-y[va]);losses.append(pd.DataFrame({'g':g[va],'e':e}).groupby('g').e.mean().mean())
   candidates.append((float(np.mean(losses)),{'max_depth':depth,'min_samples_leaf':leaf}))
  score,params=min(candidates,key=lambda z:z[0]);model=fit(train,params);baseline=float(np.mean([p['peak'] for p in train]))
  # Calibration uses the maximum error over each child's eligible input windows.
  # Conformal unit is a child, so repeated windows cannot inflate calibration N.
  scores=[]
  for p in cal:
   pred=model.predict(np.array([c['x'] for c in p['cases']]));scores.append(float(max(abs(pred-p['peak']))))
  rank=min(len(scores),int(np.ceil((len(scores)+1)*.9)));radius=sorted(scores)[rank-1]
  artifact['models'][sex]={'trees':[tree_json(t) for t in model.estimators_],'radius_years':radius,'baseline_age':baseline,'training_participants':len(train),'calibration_participants':len(cal),'training_feature_min':X.min(axis=0).tolist(),'training_feature_max':X.max(axis=0).tolist()}
  report['models'][sex]={'parameters':params,'train_cv_mae_months':score*12,'baseline_age':baseline,'calibration_radius_months':radius*12,'calibration_participants':len(cal),'cv_candidates':[{'mae_months':v*12,**p} for v,p in candidates]}
  rows=[]
  for p in test:
   pred=model.predict(np.array([c['x'] for c in p['cases']]))
   for c,z in zip(p['cases'],pred):
    evaluation_cases.append({'id':p['id'],'sex':sex,'data':c['data'],'reference':p['peak'],'prediction':float(z)})
    rows.append({'id':p['id'],'cohort':p['cohort'],'sex':sex,'n':c['n'],'latest_age':c['latest_age'],'reference_age':p['peak'],'prediction':float(z),'error':float(z-p['peak']),'baseline_error':baseline-p['peak'],'covered':bool(abs(z-p['peak'])<=radius),'prospective':c['latest_age']<p['peak']})
   for c,z in list(zip(p['cases'],pred))[::max(1,len(pred)//3)]:parity.append({'sex':sex,'data':c['data'],'expected':float(z)})
  all_records+=rows
  report['test_metrics'][sex]={'all':metrics(rows),'three_points':metrics([r for r in rows if r['n']==3]),'three_points_before_peak':metrics([r for r in rows if r['n']==3 and r['prospective']]),'four_plus':metrics([r for r in rows if r['n']>3]),'simultaneous_all_windows_coverage':float(pd.DataFrame(rows).groupby('id').covered.all().mean()),'by_cohort':{co:metrics([r for r in rows if r['cohort']==co and r['n']==3]) for co in ['Berkeley','Harpenden']}}
  # Development-only cross-cohort transport diagnostics; final test untouched here.
  report['models'][sex]['cross_cohort_development']={}
  for co in ['Berkeley','Harpenden']:
   source=[p for p in train if p['cohort']==co];dest=[p for p in train if p['cohort']!=co];m=fit(source,params);errors=[np.mean(abs(m.predict(np.array([c['x'] for c in p['cases']]))-p['peak'])) for p in dest]
   report['models'][sex]['cross_cohort_development'][co+'_to_other']={'train_children':len(source),'evaluation_children':len(dest),'mae_months':float(np.mean(errors)*12)}
 (ROOT/'phv-model.json').write_text(json.dumps(artifact,separators=(',',':'))+'\n')
 (ROOT/'training/report.json').write_text(json.dumps(report,indent=2)+'\n')
 (ROOT/'training/parity-cases.json').write_text(json.dumps(parity,separators=(',',':'))+'\n')
 (RAW/'split_manifest.json').write_text(json.dumps([{k:p[k] for k in ['id','cohort','sex','split','peak','reference_sensitivity']} for p in people],indent=2))
 (RAW/'evaluation_cases.json').write_text(json.dumps(evaluation_cases))
 pd.DataFrame(all_records).to_csv(RAW/'heldout_predictions.csv',index=False)
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
