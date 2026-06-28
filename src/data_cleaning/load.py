import pandas as pd

from src.utils.paths import DATA_RAW

DOMAINS = {
    "DEMO_J": ["SEQN", "RIAGENDR", "RIDAGEYR", "RIDRETH3", "DMDEDUC2", "INDFMPIR"],
    "BMX_J": ["SEQN", "BMXWT", "BMXHT", "BMXBMI", "BMXWAIST"],
    "DR1TOT_J": ["SEQN", "DR1TKCAL", "DR1TPROT", "DR1TCARB", "DR1TSUGR", "DR1TTFAT", "DR1TFIBE", "DR1TSODI"],
    "SMQ_J": ["SEQN", "SMQ020", "SMQ040"],
    "BPX_J": ["SEQN", "BPXSY1", "BPXDI1"],
    "ALQ_J": ["SEQN", "ALQ121"],
    "HDL_J": ["SEQN", "LBDHDD"],
    "GLU_J": ["SEQN", "LBXGLU"],
}


def _read_domain(name):
    xpt = DATA_RAW / f"{name}.XPT"
    csv = DATA_RAW / f"{name}.csv"
    if xpt.exists() and xpt.stat().st_size > 50000:
        df = pd.read_sas(xpt)
    elif csv.exists():
        df = pd.read_csv(csv)
    else:
        raise FileNotFoundError(
            f"No source for {name}. Run src/download_data.py or src/make_offline_data.py."
        )
    keep = [c for c in DOMAINS[name] if c in df.columns]
    return df[keep].copy()


def load_merged():
    base = _read_domain("DEMO_J")
    for name in ["BMX_J", "DR1TOT_J", "SMQ_J", "BPX_J", "ALQ_J", "HDL_J", "GLU_J"]:
        base = base.merge(_read_domain(name), on="SEQN", how="left")
    base["SEQN"] = base["SEQN"].astype(int)
    return base


def main():
    df = load_merged()
    print(f"Merged NHANES domains -> {df.shape[0]} participants, {df.shape[1]} columns.")
    print(", ".join(df.columns))


if __name__ == "__main__":
    main()
