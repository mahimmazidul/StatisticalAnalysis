import numpy as np
import pandas as pd
from scipy import stats

from src.data_cleaning.rename import CONTINUOUS
from src.utils.io import load_analytic, save_table


def shapiro_safe(x):
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    if len(x) > 5000:
        rng = np.random.default_rng(2024)
        x = rng.choice(x, 5000, replace=False)
    w, p = stats.shapiro(x)
    return w, p, len(x)


def ks_normal(x):
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    z = (x - x.mean()) / x.std(ddof=1)
    d, p = stats.kstest(z, "norm")
    return d, p


def anderson_normal(x):
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    res = stats.anderson(x, dist="norm")
    crit = res.critical_values[2]
    return res.statistic, crit


def normality_report(df, columns):
    rows = []
    for c in columns:
        if c not in df.columns:
            continue
        x = df[c].dropna()
        if len(x) < 8:
            continue
        w, wp, n_used = shapiro_safe(x)
        d, dp = ks_normal(x)
        a_stat, a_crit = anderson_normal(x)
        rows.append(
            {
                "Variable": c,
                "N": int(len(x)),
                "Shapiro_W": round(w, 4),
                "Shapiro_p": f"{wp:.2e}",
                "KS_D": round(d, 4),
                "KS_p": f"{dp:.2e}",
                "Anderson_A2": round(a_stat, 3),
                "Anderson_crit_5pct": round(a_crit, 3),
                "Skewness": round(stats.skew(x), 3),
                "Kurtosis": round(stats.kurtosis(x), 3),
                "Normal_at_5pct": "No" if wp < 0.05 else "Yes",
            }
        )
    return pd.DataFrame(rows)


def main():
    df = load_analytic()
    cont = [c for c in CONTINUOUS if c in df.columns]
    rep = normality_report(df, cont)
    save_table(rep, "normality_tests", index=False)
    print(rep[["Variable", "Shapiro_W", "Shapiro_p", "Normal_at_5pct"]].to_string(index=False))


if __name__ == "__main__":
    main()
