import numpy as np

from src.data_cleaning.load import load_merged

ADULT_AGE = 20

PLAUSIBLE = {
    "BMXBMI": (10, 90),
    "BMXWT": (20, 250),
    "BMXHT": (120, 210),
    "BMXWAIST": (40, 180),
    "DR1TKCAL": (300, 8000),
    "DR1TPROT": (0, 400),
    "DR1TCARB": (0, 900),
    "DR1TSUGR": (0, 600),
    "DR1TTFAT": (0, 400),
    "DR1TFIBE": (0, 120),
    "DR1TSODI": (100, 12000),
    "BPXSY1": (70, 240),
    "BPXDI1": (30, 150),
    "INDFMPIR": (0, 5),
    "LBDHDD": (10, 160),
    "LBXGLU": (40, 500),
}


def clean(df):
    df = df.copy()
    df = df[df["RIDAGEYR"] >= ADULT_AGE].copy()
    df = df[df["BMXBMI"].notna()].copy()

    for col, (lo, hi) in PLAUSIBLE.items():
        if col in df.columns:
            df.loc[(df[col] < lo) | (df[col] > hi), col] = np.nan

    df.loc[df["DMDEDUC2"].isin([7, 9]), "DMDEDUC2"] = np.nan
    df.loc[df["SMQ020"].isin([7, 9]), "SMQ020"] = np.nan
    df.loc[df["SMQ040"].isin([7, 9]), "SMQ040"] = np.nan
    df.loc[df["ALQ121"].isin([77, 99]), "ALQ121"] = np.nan

    df = df.reset_index(drop=True)
    return df


def main():
    raw = load_merged()
    cleaned = clean(raw)
    print(f"Adults (>= {ADULT_AGE} y) with measured BMI: {cleaned.shape[0]}")
    print(f"Columns retained: {cleaned.shape[1]}")


if __name__ == "__main__":
    main()
