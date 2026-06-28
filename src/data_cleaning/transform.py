import numpy as np
import pandas as pd
from scipy import stats

LOG_CANDIDATES = ["EnergyKcal", "SodiumMg", "FastingGlucose", "BMI"]


def add_log_transforms(df, columns=None):
    df = df.copy()
    columns = columns or LOG_CANDIDATES
    for c in columns:
        if c in df.columns:
            df[f"log_{c}"] = np.log(df[c].where(df[c] > 0))
    return df


def skewness_report(df, columns):
    rows = []
    for c in columns:
        if c not in df.columns:
            continue
        x = df[c].dropna()
        if len(x) < 8:
            continue
        rows.append(
            {
                "Variable": c,
                "Skewness": round(stats.skew(x), 3),
                "Kurtosis_Excess": round(stats.kurtosis(x), 3),
            }
        )
    return pd.DataFrame(rows).reset_index(drop=True)
