# Machakos Earth Dams — Hydrological Assessment

## Overview

This repository supports technical review and reproducibility of hydrological analyses for existing earth dams in Machakos County, Kenya. The currently published implementation covers **Kwale Earth Dam**. Additional dam analyses may be added separately.

The Kwale model processes catchment-average **CHIRPS Version 3 daily precipitation (1981–2025)** and estimates **uncalibrated gross surface runoff**, not observed discharge, reservoir inflow, or dependable yield.

## Repository contents

| File | Description |
| --- | --- |
| `Kwale_Annex_Model_V1.py` | Python implementation of the Kwale daily rainfall–runoff model |
| `Machakos_CHIRPS_Daily_1981_2025_Consolidated.csv` | Consolidated daily rainfall input for the Machakos catchments |
| `Kwale_Model_V1_Daily.csv` | Kwale daily rainfall and modelled runoff |
| `Kwale_Model_V1_Monthly.csv` | Monthly aggregated rainfall and modelled runoff |
| `Kwale_Model_V1_Annual.csv` | Annual aggregated rainfall and modelled runoff |

## Model specification

For each day, the runoff depth is calculated as:

`Q_mm = K * max(P_mm - T_mm, 0)`

Runoff volume is calculated as:

`Q_m3 = Q_mm * area_km2 * 1000`

| Scenario | K | T (mm/day) |
| --- | ---: | ---: |
| Low | 0.107 | 11.90 |
| Central | 0.223 | 7.94 |
| High | 0.278 | 6.38 |

These are uncalibrated regional-analogue parameter scenarios, not site-calibrated coefficients. The model uses the full-precision `area_km2` value from the source CSV rather than the rounded area displayed in the report.

## Requirements

- Python 3.10 or later recommended
- No third-party Python libraries required
- The input CSV must contain `site`, `date`, `rainfall_mm`, and `area_km2` columns
- Dates must use ISO format (`YYYY-MM-DD`)
- The Kwale records must have `site` equal to `Kwale_catchment`

## Running the model

Download the Python script and input CSV into the same folder. From a terminal in that folder, run:

```bash
python Kwale_Annex_Model_V1.py Machakos_CHIRPS_Daily_1981_2025_Consolidated.csv
```

The script validates that the Kwale input has **16,436 unique daily records** spanning 1 January 1981 to 31 December 2025, with no missing dates, and writes the three `Kwale_Model_V1_*.csv` outputs in the directory containing the script. It prints the mean annual central-scenario runoff.

**Warning:** Running the script in the repository directory overwrites output files with the same names. For verification, use a separate test directory.

## Reproducibility check

1. Download the Python script and consolidated rainfall input CSV.
2. Run the model in a clean test directory.
3. Confirm that it generates 16,436 daily, 540 monthly, and 45 annual records.
4. Compare generated CSV files with the published outputs, allowing for insignificant floating-point formatting differences.
5. Confirm the modelled mean annual runoff values against the hydrological assessment report.

The existence of the files in this repository does not by itself establish that a fresh independent execution has reproduced every published value.

## Data provenance and limitations

- **Rainfall source:** CHIRPS Version 3 daily precipitation, processed to catchment-average rainfall.
- **Catchment area:** Source CSV `area_km2` metadata derived from catchment delineation; the model itself does not perform GIS delineation.
- **Temporal coverage:** 1981–2025 inclusive.
- **Limitations:** No streamflow calibration, reservoir routing, abstraction, evaporation, seepage, transmission-loss, sedimentation or downstream reserve calculation is implemented in this model. Gross runoff should not be equated to dependable reservoir yield.
- **Validation:** Independent rainfall gauge comparisons and their spatial/temporal limitations should be consulted in the corresponding hydrological assessment report.

## Citation

Machakos Earth Dams Hydrological Assessment — Kwale Earth Dam, Python Daily Rainfall–Runoff Model V1. Source repository: https://github.com/Jmutinda/Machakos-Earth-Dams-Hydrology

For a submitted report, cite a specific commit hash so that the referenced code and data version remains identifiable.
