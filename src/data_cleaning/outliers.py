import numpy as np
import pandas as pd


def iqr_bounds(series, k=1.5):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr


def modified_zscore(series):
    x = series.dropna()
    med = x.median()
    mad = (x - med).abs().median()
    if mad == 0:
        return pd.Series(np.zeros(len(series)), index=series.index)
    return 0.6745 * (series - med) / mad


def outlier_report(df, columns):
    rows = []
    for c in columns:
        if c not in df.columns:
            continue
        s = df[c]
        lo, hi = iqr_bounds(s)
        iqr_out = ((s < lo) | (s > hi)).sum()
        mz = modified_zscore(s)
        mz_out = (mz.abs() > 3.5).sum()
        rows.append(
            {
                "Variable": c,
                "Lower_Fence": round(lo, 2),
                "Upper_Fence": round(hi, 2),
                "N_IQR_Outliers": int(iqr_out),
                "Pct_IQR_Outliers": round(100 * iqr_out / s.notna().sum(), 2),
                "N_ModZ_Outliers": int(mz_out),
            }
        )
    return pd.DataFrame(rows).reset_index(drop=True)
