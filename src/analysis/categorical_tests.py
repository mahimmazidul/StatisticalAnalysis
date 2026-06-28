import numpy as np
import pandas as pd
from scipy import stats

from src.utils.io import load_analytic, save_table
from src.utils.stats_helpers import cramers_v, interpret_cramers_v, stars


def chi_square(df, row, col):
    sub = df.dropna(subset=[row, col])
    table = pd.crosstab(sub[row], sub[col])
    chi2, p, dof, expected = stats.chi2_contingency(table)
    min_expected = expected.min()
    v = cramers_v(table.values)
    use_fisher = table.shape == (2, 2) and min_expected < 5
    fisher_p = np.nan
    if table.shape == (2, 2):
        fisher_p = stats.fisher_exact(table.values)[1]
    return {
        "Row": row,
        "Col": col,
        "N": int(table.values.sum()),
        "Chi2": round(chi2, 3),
        "df": int(dof),
        "Chi2_p": f"{p:.2e}",
        "Min_Expected": round(min_expected, 2),
        "Fisher_p": f"{fisher_p:.2e}" if not np.isnan(fisher_p) else "NA",
        "Cramers_V": round(v, 3),
        "Effect_Magnitude": interpret_cramers_v(v, dof),
        "Recommended": "Fisher exact" if use_fisher else "Chi-square",
        "Decision": stars(fisher_p if use_fisher else p),
    }


def main():
    df = load_analytic()
    pairs = [
        ("Sex", "BMICategory"),
        ("SmokingStatus", "BMICategory"),
        ("IncomeGroup", "Obese"),
        ("Education", "Obese"),
        ("AgeGroup", "Hypertensive"),
        ("SmokingStatus", "Hypertensive"),
        ("Sex", "Obese"),
        ("Sex", "CurrentSmoker"),
        ("IncomeGroup", "CurrentSmoker"),
    ]
    rows = [chi_square(df, r, c) for r, c in pairs if r in df.columns and c in df.columns]
    out = pd.DataFrame(rows)
    save_table(out, "categorical_tests", index=False)
    print(out[["Row", "Col", "Chi2", "df", "Chi2_p", "Cramers_V", "Decision"]].to_string(index=False))


if __name__ == "__main__":
    main()
