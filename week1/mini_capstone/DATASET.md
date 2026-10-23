# Dataset attribution and limits

This teaching subset is derived from **Seoul Bike Sharing Demand** (Sathishkumar V. E. et al., UCI Machine Learning Repository, DOI [10.24432/C5F62R](https://doi.org/10.24432/C5F62R)), licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. The original contains 8,760 hourly observations. This repository keeps the 365 rows recorded at Hour 12 (one noon observation per date) and renames columns to short snake_case names; no target values were generated or changed.

Use this attribution in student reports:

> Seoul Bike Sharing Demand [Dataset]. (2020). UCI Machine Learning Repository. https://doi.org/10.24432/C5F62R. Subset and column names adapted for MDC-301 Week 1 under CC BY 4.0.

Data columns include the date, noon rental count, temperature, humidity, wind speed, visibility, dew point, solar radiation, rainfall, snowfall, season, holiday, and functioning-day flag. The Week 1 classifier uses above-median bike demand as its label; rainfall is neither a target nor a predictor in that classifier.

**Scope limitation:** this 365-row noon-only subset is for an introductory model-comparison exercise. Its observations are time ordered and are not a random sample of every hour. The high-demand label is defined using the median rental count in the training dates only, then applied unchanged to the held-out dates. This is a contemporaneous pattern exercise, not a future-demand forecast and not a rainfall classification project. Results do not establish causation.
