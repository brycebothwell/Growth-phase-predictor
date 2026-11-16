"""Additional descriptive held-out metrics. Run after train.py and comparison.cjs.
Does not tune or refit the deployed beta.
"""
from pathlib import Path
import json,numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];RAW=ROOT/'training/raw';SEED=20261116

def summarize(d):
 if not len(d):return None
 d=d.copy();d['weight']=1/d.groupby('id').id.transform('size')/d.id.nunique();w=d.weight.to_numpy();e=d.error.to_numpy();z={'children':int(d.id.nunique()),'windows':len(d),'mae_months':float(np.sum(w*abs(e))*12),'rmse_months':float(np.sqrt(np.sum(w*e**2))*12),'bias_months':float(np.sum(w*e)*12)}
 for m in [3,6,12]:z['within_'+str(m)+'_months']=float(np.sum(w*(abs(e)<=m/12)))
 actual=np.where(d.latest_age<d.reference_age-.5,0,np.where(d.latest_age>d.reference_age+.5,2,1));pred=np.where(d.latest_age<d.prediction-.5,0,np.where(d.latest_age>d.prediction+.5,2,1));matrix=np.zeros((3,3));raw=np.zeros((3,3),dtype=int)
 for a,p,ww in zip(actual,pred,w):matrix[a,p]+=ww;raw[a,p]+=1
 z['phase_order']=['pre','near +/-6mo','post'];z['phase_confusion_subject_weighted']=matrix.tolist();z['phase_confusion_window_counts']=raw.tolist();z['phase_accuracy']=float(np.trace(matrix));z['phase_sensitivity']={};z['phase_specificity']={}
 for i,k in enumerate(z['phase_order']):
  tp=matrix[i,i];fn=matrix[i,:].sum()-tp;fp=matrix[:,i].sum()-tp;tn=matrix.sum()-tp-fn-fp
  z['phase_sensitivity'][k]=float(tp/(tp+fn)) if tp+fn else None;z['phase_specificity'][k]=float(tn/(tn+fp)) if tn+fp else None
 z['range_coverage']=float(np.sum(w*d.covered));return z

def main():
 d=pd.read_csv(RAW/'heldout_predictions.csv');r=json.load(open(ROOT/'training/report.json'));out={'interpretation':'Descriptive evaluation only; repeated windows are weighted equally per child. Biological PHV is approximated by reference splines. No calibrated phase probabilities are produced.','by_sex':{},'paired_model_comparison':{},'matched_measurement_counts':{}}
 for sex,g in d.groupby('sex'):
  out['by_sex'][sex]={'three_points':summarize(g[g.n==3]),'all_points':summarize(g),'prospective_three_points':summarize(g[(g.n==3)&g.prospective]),'by_count':{str(int(n)):summarize(v) for n,v in g.groupby('n')},'by_cohort':{co:summarize(v[v.n==3]) for co,v in g.groupby('cohort')}}
  # Fixed, descriptive maturation bins; not estimated from test outcomes.
  center=13.5 if sex=='male' else 11.5
  g=g.copy();g['maturation']=np.where(g.reference_age<center-1,'early',np.where(g.reference_age>center+1,'late','middle'));g['age_bin']=pd.cut(g.latest_age,[8,10,12,14,17],include_lowest=True)
  out['by_sex'][sex]['maturation']={k:summarize(v[v.n==3]) for k,v in g.groupby('maturation')};out['by_sex'][sex]['index_age']={str(k):summarize(v[v.n==3]) for k,v in g.groupby('age_bin',observed=True)}
  # Same child and index age; average over any eligible stride variants at n.
  pivot=g.assign(abs_error=abs(g.error)).groupby(['id','latest_age','n']).abs_error.mean().unstack('n');out['matched_measurement_counts'][sex]={}
  for n in [4,5,6,7]:
   paired=pivot[[3,n]].dropna();per=(paired[n]-paired[3]).groupby('id').mean()
   if len(per):
    rng=np.random.default_rng(SEED);boot=np.mean(rng.choice(per.to_numpy(),(2000,len(per)),replace=True),axis=1)*12
    out['matched_measurement_counts'][sex][str(n)]={'children':len(per),'matched_index_dates':len(paired),'change_mae_months_vs_three':float(per.mean()*12),'bootstrap95_change_months':np.quantile(boot,[.025,.975]).tolist(),'note':'Same index date and child; longer histories can still differ in spacing. Not a randomized measurement benefit.'}
 if (RAW/'v1-comparison-results.json').exists():
  c=pd.read_json(RAW/'v1-comparison-results.json')
  for sex,g in c.groupby('sex'):
   per=g.assign(delta=abs(g.trained-g.reference)-abs(g.legacy-g.reference)).groupby('id').delta.mean();rng=np.random.default_rng(SEED);boot=np.mean(rng.choice(per.to_numpy(),(5000,len(per)),replace=True),axis=1)*12
   out['paired_model_comparison'][sex]={'children':len(per),'windows':len(g),'legacy_mae_months':float(g.assign(e=abs(g.legacy-g.reference)).groupby('id').e.mean().mean()*12),'trained_mae_months':float(g.assign(e=abs(g.trained-g.reference)).groupby('id').e.mean().mean()*12),'delta_mae_months_trained_minus_v1':float(per.mean()*12),'bootstrap95_delta_months':np.quantile(boot,[.025,.975]).tolist(),'interpretation':'Negative favors trained beta; interval spanning zero does not demonstrate improvement.'}
 # Spacing and span from input cases, not reference outcome.
 if (RAW/'evaluation_cases.json').exists():
  cases=json.load(open(RAW/'evaluation_cases.json'));meta=pd.DataFrame([{'id':c['id'],'sex':c['sex'],'n':len(c['data']),'latest_age':c['data'][-1]['age'],'span':c['data'][-1]['age']-c['data'][0]['age'],'mean_interval':(c['data'][-1]['age']-c['data'][0]['age'])/(len(c['data'])-1),'prediction':c['prediction'],'reference_age':c['reference'],'error':c['prediction']-c['reference'],'covered':abs(c['prediction']-c['reference'])<=r['models'][c['sex']]['calibration_radius_months']/12} for c in cases]);meta['interval_bin']=pd.cut(meta.mean_interval,[.19,.375,.75,1.11],labels=['approximately 3 months','approximately 6 months','approximately 12 months']);meta['span_bin']=pd.cut(meta.span,[.49,1,2,3.02],labels=['0.5–1 year','1–2 years','2–3 years'])
  for sex,g in meta.groupby('sex'):
   out['by_sex'][sex]['spacing_three_points']={str(k):summarize(v[v.n==3]) for k,v in g.groupby('interval_bin',observed=True)};out['by_sex'][sex]['span_three_points']={str(k):summarize(v[v.n==3]) for k,v in g.groupby('span_bin',observed=True)}
 (ROOT/'training/extended-metrics.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['paired_model_comparison'],indent=2));print(json.dumps(out['matched_measurement_counts'],indent=2))
if __name__=='__main__':main()
