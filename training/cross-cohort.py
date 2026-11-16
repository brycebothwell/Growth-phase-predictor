"""Exploratory leave-cohort-out transport test, separate from pooled holdout.
Tune only using children in the source cohort; evaluate all eligible children in the other.
Neither cohort is now a pristine final external-validation dataset.
"""
import train,json,numpy as np,pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.ensemble import RandomForestRegressor
people,_,_=train.subjects();results={}
for sex in ['male','female']:
 results[sex]={}
 for co in ['Berkeley','Harpenden']:
  source=[p for p in people if p['sex']==sex and p['cohort']==co];dest=[p for p in people if p['sex']==sex and p['cohort']!=co];X,y,g,w,_=train.flatten(source);options=[]
  for depth,leaf in [(3,10),(5,10),(7,10),(5,20)]:
   losses=[]
   for tr,va in GroupKFold(4).split(X,y,g):
    m=RandomForestRegressor(n_estimators=100,max_depth=depth,min_samples_leaf=leaf,random_state=train.SEED,n_jobs=1).fit(X[tr],y[tr],sample_weight=w[tr]);e=abs(m.predict(X[va])-y[va]);losses.append(pd.DataFrame({'id':g[va],'e':e}).groupby('id').e.mean().mean())
   options.append((np.mean(losses),{'max_depth':depth,'min_samples_leaf':leaf}))
  cv,params=min(options,key=lambda x:x[0]);model=train.fit(source,params);errors=[];bias=[];baseline=[];base=np.mean([p['peak'] for p in source])
  for p in dest:
   cs=[c for c in p['cases'] if c['n']==3];pred=model.predict(np.array([c['x'] for c in cs]));errors.append(np.mean(abs(pred-p['peak'])));bias.append(np.mean(pred-p['peak']));baseline.append(abs(base-p['peak']))
  results[sex][co+'_to_'+dest[0]['cohort']]={'source_children':len(source),'test_children':len(dest),'source_cv_mae_months':float(cv*12),'params':params,'three_point_mae_months':float(np.mean(errors)*12),'bias_months':float(np.mean(bias)*12),'source_mean_baseline_mae_months':float(np.mean(baseline)*12)}
(train.ROOT/'training/cross-cohort-results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
