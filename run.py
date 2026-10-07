from pathlib import Path
import sys,json,hashlib,platform,time,urllib.request,calendar,subprocess
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT))
import pandas as pd,numpy as np,sklearn,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from forecasting import MODELS,predict,metrics
URL='https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2020/07/MAR_Comm-Timeseries-May-20-qQ0K3.xls'
PAGE='https://www.england.nhs.uk/statistics/statistical-work-areas/hospital-activity/monthly-hospital-activity/mar-'

def extract(path):
    raw=pd.read_excel(path,header=None)
    headers=[i for i in raw.index if str(raw.iloc[i,2]).strip()=='Period']
    if len(headers)!=1: raise ValueError('Unexpected workbook header')
    h=headers[0]; cols=[i for i in raw.columns if str(raw.iloc[h,i]).strip()=='All 1st Outpatient Attendances (G&A)']
    if len(cols)!=1: raise ValueError('Target missing')
    rows=[]; month_map={calendar.month_name[i].upper():i for i in range(1,13)}
    for _,r in raw.iloc[h+1:].iterrows():
        if str(r[2]).strip().upper() not in month_map: continue
        m=month_map[str(r[2]).strip().upper()];start=int(str(r[1])[:4]);year=start+(m<4)
        rows.append((pd.Timestamp(year,m,1),int(r[cols[0]])))
    df=pd.DataFrame(rows,columns=['date','attendances']).sort_values('date')
    if not df.date.is_unique or not (df.attendances>0).all() or not df.date.tolist()==pd.date_range(df.date.min(),df.date.max(),freq='MS').tolist(): raise ValueError('Invalid monthly series')
    return df

def main():
    start=time.time();cfg=json.loads((ROOT/'experiment.json').read_text());p=ROOT/'raw/nhs_activity.xls'
    if not p.exists():
        p.parent.mkdir(parents=True,exist_ok=True);urllib.request.urlretrieve(URL,p)
    df=extract(p);df.to_csv(ROOT/'monthly_activity.csv',index=False)
    dates=pd.DatetimeIndex(df.date);y=df.attendances.to_numpy(dtype=float);records=[]
    for t in range(13,len(df)):
        if dates[t]<pd.Timestamp(cfg['validation_start']): continue
        split='validation' if dates[t]<=pd.Timestamp(cfg['validation_end']) else ('test' if dates[t]<=pd.Timestamp(cfg['test_end']) else 'stress')
        for model in MODELS: records.append(dict(date=str(dates[t].date()),train_end=str(dates[t-1].date()),split=split,model=model,actual=y[t],prediction=predict(y,dates,t,model,cfg)))
    out=pd.DataFrame(records)
    selected=min(MODELS,key=lambda m:metrics(out.query('model==@m and split=="validation"').actual,out.query('model==@m and split=="validation"').prediction)['mae'])
    for model in MODELS:
        v=out.query('model==@model and split=="validation"');e=abs(v.actual-v.prediction).to_numpy();rank=min(len(e),int(np.ceil((len(e)+1)*cfg['interval_level'])));q=np.sort(e)[rank-1]
        mask=out.model==model;out.loc[mask,'lower']=np.maximum(0,out.loc[mask,'prediction']-q);out.loc[mask,'upper']=out.loc[mask,'prediction']+q
    out.to_csv(ROOT/'predictions.csv',index=False)
    summary=[]
    for (split,model),g in out.groupby(['split','model']):
        d=metrics(g.actual,g.prediction);d.update(split=split,model=model,n=len(g))
        d['coverage']=None if split=='validation' else float(((g.actual>=g.lower)&(g.actual<=g.upper)).mean());d['mean_width']=float((g.upper-g.lower).mean());summary.append(d)
    scores=pd.DataFrame(summary);scores.to_csv(ROOT/'metrics.csv',index=False)
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(12,5));g=out.query('model==@selected and split!="validation"');x=pd.to_datetime(g.date)
    ax.plot(x,g.actual/1e6,label='Recorded first attendances',color='#123b54',lw=2);ax.plot(x,g.prediction/1e6,label=f'Forecast: {selected}',color='#df704c',lw=2)
    ax.fill_between(x,g.lower/1e6,g.upper/1e6,color='#df704c',alpha=.15,label='90% empirical band')
    ax.axvline(pd.Timestamp('2020-01-01'),color='gray',ls='--');ax.set(title='Forecasting NHS outpatient activity: test and 2020 stress period',ylabel='Monthly attendances (millions)',xlabel='Month');ax.legend(loc='lower left');fig.tight_layout();fig.savefig(ROOT/'forecast.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4));s=scores.query('split=="test"').sort_values('mae');ax.barh(s.model,s.mae/1000,color='#167d8d');ax.invert_yaxis();ax.set(title='Locked historical test: January 2018–December 2019',xlabel='Mean absolute error (thousands of attendances)');fig.tight_layout();fig.savefig(ROOT/'comparison.png',dpi=180);plt.close(fig)
    sha=hashlib.sha256(p.read_bytes()).hexdigest()
    (ROOT/'manifest.json').write_text(json.dumps(dict(source_url=URL,source_page=PAGE,retrieved_utc=pd.Timestamp.now(tz='UTC').isoformat(),sha256=sha,period=[str(df.date.min().date()),str(df.date.max().date())],rows=len(df),target='All 1st Outpatient Attendances (G&A)',basis='Commissioner; England aggregate',published='2020-07-09',terms='NHS England copyright policy / Open Government Licence; see DATA_SOURCE.md'),indent=2))
    record=dict(status='completed',selected_by_validation=selected,config=cfg,python=platform.python_version(),versions={'pandas':pd.__version__,'numpy':np.__version__,'scikit-learn':sklearn.__version__,'matplotlib':matplotlib.__version__},data_sha256=sha,duration_seconds=time.time()-start,source_sha256=hashlib.sha256(Path(__file__).read_bytes()+(ROOT/'forecasting.py').read_bytes()).hexdigest())
    (ROOT/'run_record.json').write_text(json.dumps(record,indent=2));print(scores[['split','model','mae','wape','coverage']].to_string(index=False));print('Validation-selected:',selected)
if __name__=='__main__':main()
