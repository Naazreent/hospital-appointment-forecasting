"""Historical one-step forecasts; features depend only on prior observations."""
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor

MODELS = ['last_month','seasonal_naive','seasonal_drift','ridge','random_forest']

def features(y, dates, t):
    assert t >= 13
    d=dates[t]
    return [y[t-k] for k in (1,2,3,6,12,13)] + [np.mean(y[t-3:t]),np.mean(y[t-12:t]),np.sin(2*np.pi*d.month/12),np.cos(2*np.pi*d.month/12),d.days_in_month,t]

def predict(y, dates, t, model, cfg):
    if model=='last_month': return float(y[t-1])
    if model=='seasonal_naive': return float(y[t-12])
    if model=='seasonal_drift': return max(0.,float(y[t-12]+np.mean(y[12:t]-y[:t-12])))
    X=np.array([features(y,dates,i) for i in range(13,t)])
    reg=(make_pipeline(StandardScaler(),Ridge(alpha=cfg['ridge_alpha'])) if model=='ridge' else RandomForestRegressor(n_estimators=cfg['forest_trees'],min_samples_leaf=cfg['forest_min_leaf'],random_state=cfg['seed'],n_jobs=1))
    reg.fit(X,y[13:t])
    return max(0.,float(reg.predict([features(y,dates,t)])[0]))

def metrics(actual,pred):
    err=np.asarray(pred)-np.asarray(actual)
    return dict(mae=float(np.mean(abs(err))),rmse=float(np.sqrt(np.mean(err**2))),wape=float(abs(err).sum()/np.asarray(actual).sum()),bias=float(err.mean()))
