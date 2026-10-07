# Prespecified experiment contract
Question: Do lag-based models improve one-month-ahead prediction of England first outpatient attendance activity over seasonal-naive forecasts?
Target: commissioner-based All 1st Outpatient Attendances (G&A), national monthly counts.
Primary metric: MAE on January 2018–December 2019. Secondary: WAPE, RMSE, signed error and 90% interval coverage/width. Validation January 2016–December 2017 selects a model. January–May 2020 is a separately reported stress period, not used for selection.
Models: last month, same month last year, seasonal drift, fixed Ridge and Random Forest. No hyperparameter search. Fit each model using only observations before each origin; historical outcomes become available sequentially. Forecast horizon one month. First origin January 2016. Lags 1,2,3,6,12,13, rolling means 3/12, calendar month sin/cos, month length and trend.
Intervals: fixed absolute validation-error quantile with finite-sample correction, separately for each model. These are empirical bands; serial dependence and distribution shift preclude a coverage guarantee.
Acceptance: contiguous positive monthly target; unique origins; no future features; saved predictions independently reproduce metrics; unchanged historical predictions when future values are altered. Null model improvements retained. No significance or novelty claim.
Budget: CPU, under 5 minutes. Fixed seed 42; temporal origins provide evaluation repetition. No patient records.
