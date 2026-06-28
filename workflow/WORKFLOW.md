# Reproducible Analysis Workflow

This document describes the exact order of operations and the design rationale behind the pipeline. Every step is a small, single-purpose, comment-free Python module so that each decision is auditable.

## 1. Acquisition

| Step | Module | Output |
|------|--------|--------|
| Download NHANES `.XPT` files from CDC | `src/download_data.py` | `data/raw/*.XPT` |
| Deterministic offline fallback (seed = 20172018) | `src/make_offline_data.py` | `data/raw/*.csv` |

The downloader validates the SAS XPORT magic bytes (`HEADER R`) before writing, so a captive-portal HTML error page can never masquerade as data. If any domain fails, the offline generator reproduces the statistical structure of NHANES so the pipeline always completes.

## 2. Cleaning (`src/data_cleaning/`)

| Order | Module | Decision documented |
|-------|--------|---------------------|
| 1 | `load.py` | Merge 8 domains on `SEQN` via left joins onto demographics |
| 2 | `clean.py` | Restrict to adults (&ge; 20 y); require measured BMI; screen biologically implausible values to missing |
| 3 | `rename.py` | Map cryptic NHANES codes to analysis-friendly names; declare variable roles |
| 4 | `encode.py` | Derive `Sex`, `RaceEthnicity`, `Education`, `SmokingStatus`, WHO `BMICategory`, `AgeGroup`, `IncomeGroup`, and binary flags `Obese`, `Hypertensive`, `CurrentSmoker` |
| 5 | `missing.py` | Quantify and visualise missingness; define handling strategy |
| 6 | `outliers.py` | IQR fences and modified z-score reporting (flag, not delete) |
| 7 | `transform.py` | Log transforms for right-skewed variables; skewness reporting |
| 8 | `scale.py` | z-standardisation, used only where statistically appropriate (PCA, standardised coefficients) |

### Missing-data strategy

The primary analyses use **complete-case analysis** per test (pairwise deletion), which is unbiased under a missing-completely-at-random (MCAR) assumption and is the most transparent default. Where a single imputed dataset is required for illustration, **median imputation** is offered in `missing.py`. The missingness correlation heatmap (`figures/missing_heatmap.png`) is inspected to check that missingness is not strongly structured. Multiple imputation is listed as future work.

### Outlier strategy

Outliers are **flagged, not removed**. Extreme but biologically plausible values (e.g. BMI of 60) are genuine and informative for a skewed public-health outcome; deleting them would bias prevalence estimates. Only values outside physiological plausibility (defined in `clean.py`) are set to missing.

## 3. Assumption checks before inference

Normality (Shapiro&ndash;Wilk, Kolmogorov&ndash;Smirnov, Anderson&ndash;Darling) and variance homogeneity (Levene, Bartlett) are computed first. Test selection then follows the decision tree in the README: Welch when variances differ, rank-based tests when normality fails, parametric tests only when justified.

## 4. Inference, regression, and ordination

`src/run_all.py` executes, in order: descriptive statistics, cross-tabulations, normality, variance tests, two-group tests, ANOVA, categorical tests, correlation, linear regression, logistic regression, regression diagnostics, and PCA; then renders all 28 figures.

## 5. Reporting

`src/build_report.py` assembles `report/report.md` into `report/report.pdf`.

## One-command reproduction

```bash
make all
# equivalent to:
python -m src.download_data || python -m src.make_offline_data
python -m src.preprocess
python -m src.run_all
python -m src.build_report
```
