Kenya lacks a public drought monitor that works at county level for all 47 counties. Tools that exist either fail at county resolution or publish so late the harvest is already lost.

We present a composite stress index built from CHIRPS satellite rainfall, Sentinel-2 vegetation health, and ERA5-Land soil moisture. The index compares each county-month to that county's own historical climatology, so no calibration or training data is required.

Applied to the 2022 Horn of Africa drought, the index identified severe stress without calibration. Of 31 counties with severe drought in 2022, only 8 had it while maize was growing.

Cross-checked against NDMA's drought classifications, the index flagged a different set of counties. Zero overlap. Both systems were right: NDMA tracks pastoral drought in 23 ASAL counties; the index tracks crop-region vegetation stress in all 47.

Soil moisture anomaly leads NDVI anomaly by one month (r = 0.461, 95% CI [0.436, 0.485]).

We also tested whether the index predicts maize yield loss. It does not. We document the null result.

The full pipeline is open source at github.com/alexharonyandega-dev/kenya-climate-data-lab.
