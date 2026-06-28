import pandas as pd

from src.utils.io import load_analytic, save_table


def crosstab(df, row, col, normalize=False):
    margins = normalize is False
    return pd.crosstab(df[row], df[col], normalize=normalize, margins=margins)


def main():
    df = load_analytic()
    pairs = [
        ("Sex", "BMICategory"),
        ("SmokingStatus", "BMICategory"),
        ("IncomeGroup", "BMICategory"),
        ("AgeGroup", "Hypertensive"),
        ("Education", "Obese"),
        ("SmokingStatus", "Hypertensive"),
    ]
    for row, col in pairs:
        if row in df.columns and col in df.columns:
            ct = crosstab(df, row, col)
            save_table(ct, f"crosstab_{row.lower()}_{col.lower()}")
            ctn = (crosstab(df, row, col, normalize="index") * 100).round(1)
            save_table(ctn, f"crosstab_{row.lower()}_{col.lower()}_rowpct")
    print(f"Saved {len(pairs)} cross-tabulations (counts and row percentages).")


if __name__ == "__main__":
    main()
