import numpy as np
import pandas as pd


def missing_summary(df, columns):
    rows = []
    n = len(df)
    for c in columns:
        if c not in df.columns:
            continue
        miss = df[c].isna().sum()
        rows.append(
            {
                "Variable": c,
                "N_Observed": int(n - miss),
                "N_Missing": int(miss),
                "Percent_Missing": round(100 * miss / n, 2),
            }
        )
    out = pd.DataFrame(rows).sort_values("Percent_Missing", ascending=False)
    return out.reset_index(drop=True)


def little_style_pattern(df, columns):
    indicator = df[columns].isna().astype(int)
    patterns = indicator.apply(lambda r: "".join(r.astype(str)), axis=1)
    counts = patterns.value_counts().rename("Count").reset_index()
    counts.columns = ["Pattern", "Count"]
    counts["N_Missing_Vars"] = counts["Pattern"].apply(lambda s: s.count("1"))
    return counts.sort_values("Count", ascending=False).reset_index(drop=True)


def median_impute(df, columns):
    df = df.copy()
    for c in columns:
        if c in df.columns:
            df[c] = df[c].fillna(df[c].median())
    return df
