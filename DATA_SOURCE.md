# Data provenance
Source: NHS England, Monthly Hospital Activity, commissioner-based England time series, published 9 July 2020. April 2008–May 2020, 146 observations. Target is **All 1st Outpatient Attendances (G&A)**. These are recorded first attendances, not all appointments, unique patients, referrals or unconstrained demand.

Source page: https://www.england.nhs.uk/statistics/statistical-work-areas/hospital-activity/monthly-hospital-activity/mar-data/
Workbook: https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2020/07/MAR_Comm-Timeseries-May-20-qQ0K3.xls

Attribution: Contains NHS England information licensed under the Open Government Licence. https://www.england.nhs.uk/terms-and-conditions-2/ and https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
Code licence does not replace source data terms. No NHS logos included. Derived monthly_activity.csv and manifest.json are supplied; original workbook is downloaded by run.py and excluded from Git.

Fiscal years converted to calendar month dates; no imputation or smoothing. Published revised values are used retrospectively. Original publication-vintage values and real-time availability are not reconstructed. The collection ceased in 2020; do not splice later series without checking definitions. This is deliberately a historical benchmark, not a current 2026 forecast.
