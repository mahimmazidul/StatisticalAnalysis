import numpy as np
import pandas as pd


def zscore_columns(df, columns, suffix="_z"):
    df = df.copy()
    for c in columns:
        if c in df.columns:
            s = df[c]
            sd = s.std(ddof=1)
            if sd and not np.isnan(sd):
                df[f"{c}{suffix}"] = (s - s.mean()) / sd
    return df
