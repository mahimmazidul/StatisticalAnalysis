import numpy as np
import pandas as pd
from scipy import stats

from src.utils.io import load_analytic, save_table
from src.utils.stats_helpers import (
    hedges_g,
    interpret_d,
    mean_ci,
    rank_biserial_from_u,
    stars,
)


def two_group_test(df, value, group, g1, g2):
    sub = df.dropna(subset=[value, group])
    a = sub.loc[sub[group] == g1, value].values
    b = sub.loc[sub[group] == g2, value].values
    n1, n2 = len(a), len(b)

    lev_p = stats.levene(a, b, center="median")[1]
    equal_var = lev_p >= 0.05

    t_stat, t_p = stats.ttest_ind(a, b, equal_var=equal_var)
    welch_t, welch_p = stats.ttest_ind(a, b, equal_var=False)
    u_stat, u_p = stats.mannwhitneyu(a, b, alternative="two-sided")

    g = hedges_g(a, b)
    rb = rank_biserial_from_u(u_stat, n1, n2)

    diff = a.mean() - b.mean()
    sp = np.sqrt(((n1 - 1) * a.var(ddof=1) + (n2 - 1) * b.var(ddof=1)) / (n1 + n2 - 2))
    se = sp * np.sqrt(1 / n1 + 1 / n2)
    dof = n1 + n2 - 2
    tcrit = stats.t.ppf(0.975, dof)
    ci_lo, ci_hi = diff - tcrit * se, diff + tcrit * se

    chosen = "Welch t-test" if not equal_var else "Student t-test"
    chosen_p = welch_p if not equal_var else t_p

    return {
        "Outcome": value,
        "Group": f"{g1} vs {g2}",
        "N1": n1,
        "N2": n2,
        "Mean1": round(a.mean(), 2),
        "Mean2": round(b.mean(), 2),
        "MeanDiff": round(diff, 2),
        "CI95_Low": round(ci_lo, 2),
        "CI95_High": round(ci_hi, 2),
        "Levene_p": round(lev_p, 4),
        "Student_t": round(t_stat, 3),
        "Student_p": f"{t_p:.2e}",
        "Welch_t": round(welch_t, 3),
        "Welch_p": f"{welch_p:.2e}",
        "MannWhitney_U": round(u_stat, 1),
        "MannWhitney_p": f"{u_p:.2e}",
        "Chosen_Test": chosen,
        "Hedges_g": round(g, 3),
        "Effect_Magnitude": interpret_d(g),
        "RankBiserial": round(rb, 3),
        "Decision": stars(chosen_p),
    }


def main():
    df = load_analytic()
    rows = [
        two_group_test(df, "BMI", "Sex", "Male", "Female"),
        two_group_test(df, "EnergyKcal", "Sex", "Male", "Female"),
        two_group_test(df, "WaistCircumference", "Sex", "Male", "Female"),
        two_group_test(df, "HDL", "Sex", "Male", "Female"),
        two_group_test(df, "SystolicBP", "Sex", "Male", "Female"),
        two_group_test(df, "FiberG", "Sex", "Male", "Female"),
        two_group_test(df, "BMI", "CurrentSmoker", 0, 1),
        two_group_test(df, "SodiumMg", "Sex", "Male", "Female"),
    ]
    out = pd.DataFrame(rows)
    save_table(out, "two_group_tests", index=False)
    print(out[["Outcome", "Group", "MeanDiff", "Chosen_Test", "Hedges_g", "Decision"]].to_string(index=False))


if __name__ == "__main__":
    main()
