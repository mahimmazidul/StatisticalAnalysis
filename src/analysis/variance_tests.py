import pandas as pd
from scipy import stats

from src.utils.io import load_analytic, save_table


def _groups(df, value, group):
    g = df.dropna(subset=[value, group])
    return [sub[value].values for _, sub in g.groupby(group, observed=True)]


def homogeneity_report(df, comparisons):
    rows = []
    for value, group in comparisons:
        if value not in df.columns or group not in df.columns:
            continue
        groups = _groups(df, value, group)
        if len(groups) < 2:
            continue
        lev_stat, lev_p = stats.levene(*groups, center="median")
        bar_stat, bar_p = stats.bartlett(*groups)
        rows.append(
            {
                "Outcome": value,
                "Grouping": group,
                "K_groups": len(groups),
                "Levene_W": round(lev_stat, 3),
                "Levene_p": round(lev_p, 4),
                "Bartlett_chi2": round(bar_stat, 3),
                "Bartlett_p": f"{bar_p:.2e}",
                "Equal_Variance_at_5pct": "No" if lev_p < 0.05 else "Yes",
            }
        )
    return pd.DataFrame(rows)


def main():
    df = load_analytic()
    comparisons = [
        ("BMI", "Sex"),
        ("BMI", "SmokingStatus"),
        ("BMI", "AgeGroup"),
        ("EnergyKcal", "Sex"),
        ("EnergyKcal", "AgeGroup"),
        ("SystolicBP", "AgeGroup"),
        ("HDL", "Sex"),
    ]
    rep = homogeneity_report(df, comparisons)
    save_table(rep, "variance_homogeneity_tests", index=False)
    print(rep.to_string(index=False))


if __name__ == "__main__":
    main()
