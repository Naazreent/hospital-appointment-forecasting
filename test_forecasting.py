import unittest,json
from pathlib import Path
import numpy as np,pandas as pd
from forecasting import features,predict,MODELS,metrics
from run import extract
ROOT=Path(__file__).resolve().parent
class ForecastTests(unittest.TestCase):
 def test_no_future_leakage(self):
  cfg=json.loads((ROOT/'experiment.json').read_text()); dates=pd.date_range('2000-01-01',periods=50,freq='MS');y=np.arange(50,dtype=float)+100;t=35;altered=y.copy();altered[t:]=1e9
  self.assertEqual(features(y,dates,t),features(altered,dates,t))
  for m in MODELS:self.assertEqual(predict(y,dates,t,m,cfg),predict(altered,dates,t,m,cfg))
 def test_calendar_and_extraction(self):
  d=extract(ROOT/'raw/nhs_activity.xls');self.assertEqual(len(d),146);self.assertEqual(str(d.date.iloc[0].date()),'2008-04-01');self.assertEqual(str(d.date.iloc[-1].date()),'2020-05-01');self.assertEqual(d.attendances.iloc[0],1189155)
 def test_metric_recomputation(self):
  p=pd.read_csv(ROOT/'predictions.csv');s=pd.read_csv(ROOT/'metrics.csv')
  self.assertTrue((pd.to_datetime(p.train_end)<pd.to_datetime(p.date)).all())
  for _,r in s.iterrows():
   g=p[(p.model==r.model)&(p.split==r.split)]
   for k,v in metrics(g.actual,g.prediction).items():self.assertAlmostEqual(v,r[k],places=6)
 def test_metric_units(self):
  m=metrics([100,200],[110,180]);self.assertEqual(m['mae'],15);self.assertAlmostEqual(m['wape'],.1)
if __name__=='__main__':unittest.main()
