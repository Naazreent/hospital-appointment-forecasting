# Results and evidence ledger

| Model | MAE (attendances) | WAPE |
|---|---:|---:|
| ridge | 50,083 | 3.15% |
| random_forest | 51,463 | 3.24% |
| seasonal_drift | 56,848 | 3.58% |
| seasonal_naive | 62,501 | 3.94% |
| last_month | 139,086 | 8.76% |

C1: Ridge reduces test MAE by 19.9% versus seasonal naive. Evidence: metrics.csv and predictions.csv, independently recomputed by tests.
C2: Ridge stress WAPE 34.21%, empirical coverage 2/5. Evidence: same files.
No demonstrated staffing saving or waiting-time reduction. Validation-selected model is Ridge; test results did not select the model.
