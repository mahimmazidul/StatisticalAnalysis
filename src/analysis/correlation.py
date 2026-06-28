import numpy as np
import pandas as pd
from scipy import stats

from src.data_cleaning.rename import CONTINUOUS
from src.utils.io import load_analytic, save_table
from src.utils.stats_helpers import interpret_r, stars


def pearson_ci(r, n, conf=0.95):
    z = np.arctanh(r)
    se = 1 / np.sqrt(n - 3)
    zc = stats.norm.ppf(1 - (1 - conf) / 2)
    lo, hi = np.tanh(z - zc * se), np.tanh(z + zc * se)
    return lo, hi


def pairwise_correlations(df, pairs):
    rows = []
    for a, b in pairs:
        sub = df[[a, b]].dropna()
        x, y = sub[a].values, sub[b].values
        if len(x) < 5:
            continue
        r, rp = stats.pearsonr(x, y)
        rho, sp = stats.spearmanr(x, y)
        tau, tp = stats.kendalltau(x, y)
        lo, hi = pearson_ci(r, len(x))
        rows.append(
            {
                "Var1": a,
                "Var2": b,
                "N": len(x),
                "Pearson_r": round(r, 3),
                "Pearson_CI95": f"[{lo:.2f}, {hi:.2f}]",
                "Pearson_p": f"{rp:.2e}",
                "Spearman_rho": round(rho, 3),
                "Spearman_p": f"{sp:.2e}",
                "Kendall_tau": round(tau, 3),
                "Strength": interpret_r(r),
                "Decision": stars(rp),
            }
        )
    return pd.DataFrame(rows)


def partial_correlation(df, x, y, covar):
    sub = df[[x, y] + covar].dropna()
    import statsmodels.api as sm

    def resid(target):
        X = sm.add_constant(sub[covar])
        return sm.OLS(sub[target], X).fit().resid

    rx, ry = resid(x), resid(y)
    r, p = stats.pearsonr(rx, ry)
    return {
        "X": x,
        "Y": y,
        "Adjusted_For": ", ".join(covar),
        "N": len(sub),
        "Partial_r": round(r, 3),
        "p": f"{p:.2e}",
        "Decision": stars(p),
    }


def correlation_matrix(df, columns, method="pearson"):
    sub = df[columns].dropna()
    return sub.corr(method=method).round(3)


def main():
    df = load_analytic()
    pairs = [
        ("BMI", "WaistCircumference"),
        ("BMI", "EnergyKcal"),
        ("BMI", "Age"),
        ("BMI", "SystolicBP"),
        ("BMI", "HDL"),
        ("EnergyKcal", "ProteinG"),
        ("EnergyKcal", "SodiumMg"),
        ("Age", "SystolicBP"),
        ("FiberG", "EnergyKcal"),
        ("SugarG", "EnergyKcal"),
        ("FastingGlucose", "BMI"),
        ("IncomePovertyRatio", "BMI"),
    ]
    save_table(pairwise_correlations(df, pairs), "correlation_pairwise", index=False)

    partials = pd.DataFrame(
        [
            partial_correlation(df, "BMI", "SystolicBP", ["Age"]),
            partial_correlation(df, "BMI", "EnergyKcal", ["Age", "Sex_num"])
            if "Sex_num" in df.columns
            else partial_correlation(df, "BMI", "EnergyKcal", ["Age"]),
            partial_correlation(df, "EnergyKcal", "BMI", ["Height"]),
            partial_correlation(df, "Age", "HDL", ["BMI"]),
        ]
    )
    save_table(partials, "correlation_partial", index=False)

    cont = [c for c in CONTINUOUS if c in df.columns]
    save_table(correlation_matrix(df, cont, "pearson"), "correlation_matrix_pearson")
    save_table(correlation_matrix(df, cont, "spearman"), "correlation_matrix_spearman")
    print(pairwise_correlations(df, pairs)[["Var1", "Var2", "Pearson_r", "Strength", "Decision"]].to_string(index=False))


if __name__ == "__main__":
    main()
