import numpy as np
import pandas as pd
from scipy import stats

from src.data_cleaning.rename import CONTINUOUS
from src.utils.io import load_analytic, save_table


def describe_continuous(df, columns):
    rows = []
    for c in columns:
        if c not in df.columns:
            continue
        x = df[c].dropna()
        if len(x) < 3:
            continue
        mode = x.mode()
        q1, q2, q3 = x.quantile([0.25, 0.5, 0.75])
        rows.append(
            {
                "Variable": c,
                "N": int(len(x)),
                "Mean": round(x.mean(), 2),
                "Median": round(x.median(), 2),
                "Mode": round(mode.iloc[0], 2) if len(mode) else np.nan,
                "SD": round(x.std(ddof=1), 2),
                "Variance": round(x.var(ddof=1), 2),
                "CV_pct": round(100 * x.std(ddof=1) / x.mean(), 2) if x.mean() else np.nan,
                "Min": round(x.min(), 2),
                "Q1": round(q1, 2),
                "Q3": round(q3, 2),
                "Max": round(x.max(), 2),
                "IQR": round(q3 - q1, 2),
                "Range": round(x.max() - x.min(), 2),
                "P05": round(x.quantile(0.05), 2),
                "P95": round(x.quantile(0.95), 2),
                "Skewness": round(stats.skew(x), 3),
                "Kurtosis": round(stats.kurtosis(x), 3),
            }
        )
    return pd.DataFrame(rows)


def describe_by_group(df, value, group):
    g = df.dropna(subset=[value, group])
    out = g.groupby(group, observed=True)[value].agg(
        N="count", Mean="mean", SD="std", Median="median",
        Min="min", Max="max"
    ).round(2)
    return out.reset_index()


def frequency_table(df, column):
    s = df[column]
    counts = s.value_counts(dropna=False)
    pct = (counts / counts.sum() * 100).round(2)
    out = pd.DataFrame({"Count": counts, "Percent": pct})
    out.index.name = column
    return out.reset_index()


def main():
    df = load_analytic()
    cont = [c for c in CONTINUOUS if c in df.columns]
    desc = describe_continuous(df, cont)
    save_table(desc, "descriptive_continuous", index=False)

    bmi_by_sex = describe_by_group(df, "BMI", "Sex")
    save_table(bmi_by_sex, "descriptive_bmi_by_sex", index=False)

    energy_by_age = describe_by_group(df, "EnergyKcal", "AgeGroup")
    save_table(energy_by_age, "descriptive_energy_by_agegroup", index=False)

    for cat in ["Sex", "RaceEthnicity", "Education", "SmokingStatus", "BMICategory", "IncomeGroup"]:
        if cat in df.columns:
            save_table(frequency_table(df, cat), f"frequency_{cat.lower()}", index=False)

    print(f"Described {len(cont)} continuous variables across {len(df)} adults.")
    print(desc[["Variable", "Mean", "SD", "Skewness"]].to_string(index=False))


if __name__ == "__main__":
    main()
