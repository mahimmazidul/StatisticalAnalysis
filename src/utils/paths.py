from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
DATA_RAW = DATA / "raw"
DATA_PROCESSED = DATA / "processed"
FIGURES = ROOT / "figures"
TABLES = ROOT / "tables"
REPORT = ROOT / "report"
SRC = ROOT / "src"

PROCESSED_FILE = DATA_PROCESSED / "nhanes_analytic.csv"
CLEAN_FILE = DATA_PROCESSED / "nhanes_clean.csv"


def ensure_dirs():
    for d in [DATA_RAW, DATA_PROCESSED, FIGURES, TABLES, REPORT]:
        d.mkdir(parents=True, exist_ok=True)
