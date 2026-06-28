import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from src.utils.io import load_analytic, save_table
from src.utils.stats_helpers import epsilon_squared_kruskal, eta_squared_anova, stars


def _groups(df, value, group):
    g = df.dropna(subset=[value, group])
    return [sub[value].values for _, sub in g.groupby(group, observed=True)]


def oneway(df, value, group):
    groups = _groups(df, value, group)
    f, p = stats.f_oneway(*groups)
    h, hp = stats.kruskal(*groups)
    eta2 = eta_squared_anova(groups)
    n = sum(len(g) for g in groups)
    eps2 = epsilon_squared_kruskal(h, n)
    lev_p = stats.levene(*groups, center="median")[1]
    return {
        "Outcome": value,
        "Grouping": group,
        "K": len(groups),
        "df_between": len(groups) - 1,
        "df_within": n - len(groups),
        "F": round(f, 3),
        "ANOVA_p": f"{p:.2e}",
        "Eta_squared": round(eta2, 4),
        "Levene_p": round(lev_p, 4),
        "Kruskal_H": round(h, 3),
        "Kruskal_p": f"{hp:.2e}",
        "Epsilon_squared": round(eps2, 4),
        "Decision": stars(p),
    }


def tukey(df, value, group):
    g = df.dropna(subset=[value, group])
    res = pairwise_tukeyhsd(g[value].values, g[group].astype(str).values)
    table = pd.DataFrame(res.summary().data[1:], columns=res.summary().data[0])
    return table


def two_way(df, value, f1, f2):
    g = df.dropna(subset=[value, f1, f2]).copy()
    g[f1] = g[f1].astype(str)
    g[f2] = g[f2].astype(str)
    model = ols(f"{value} ~ C({f1}) + C({f2}) + C({f1}):C({f2})", data=g).fit()
    aov = sm.stats.anova_lm(model, typ=2)
    aov = aov.reset_index().rename(columns={"index": "Term"})
    aov["Term"] = aov["Term"].str.replace("C(", "", regex=False).str.replace(")", "", regex=False)
    for col in ["sum_sq", "F"]:
        aov[col] = aov[col].round(3)
    aov["PR(>F)"] = aov["PR(>F)"].apply(lambda v: f"{v:.2e}" if pd.notna(v) else "")
    return aov


def main():
    df = load_analytic()
    rows = [
        oneway(df, "BMI", "AgeGroup"),
        oneway(df, "BMI", "SmokingStatus"),
        oneway(df, "BMI", "Education"),
        oneway(df, "BMI", "IncomeGroup"),
        oneway(df, "EnergyKcal", "AgeGroup"),
        oneway(df, "SystolicBP", "AgeGroup"),
        oneway(df, "HDL", "BMICategory"),
        oneway(df, "FastingGlucose", "BMICategory"),
    ]
    save_table(pd.DataFrame(rows), "anova_oneway", index=False)
    save_table(tukey(df, "BMI", "AgeGroup"), "anova_tukey_bmi_agegroup", index=False)
    save_table(tukey(df, "SystolicBP", "AgeGroup"), "anova_tukey_sbp_agegroup", index=False)
    save_table(two_way(df, "BMI", "Sex", "AgeGroup"), "anova_twoway_bmi_sex_agegroup", index=False)
    save_table(two_way(df, "EnergyKcal", "Sex", "SmokingStatus"), "anova_twoway_energy_sex_smoking", index=False)
    print(pd.DataFrame(rows)[["Outcome", "Grouping", "F", "ANOVA_p", "Eta_squared", "Decision"]].to_string(index=False))


if __name__ == "__main__":
    main()
