import pandas as pd
from src.utils.paths import CLEAN_FILE, PROCESSED_FILE


def load_clean():
    if not CLEAN_FILE.exists():
        raise FileNotFoundError(
            "Cleaned dataset not found. Run src/data_cleaning pipeline first."
        )
    return pd.read_csv(CLEAN_FILE)


def load_analytic():
    if not PROCESSED_FILE.exists():
        raise FileNotFoundError(
            "Analytic dataset not found. Run src/preprocess.py first."
        )
    return pd.read_csv(PROCESSED_FILE)


def dataframe_to_markdown(df, index=True):
    frame = df.reset_index() if index else df.copy()
    headers = [str(c) for c in frame.columns]
    rows = []
    for _, r in frame.iterrows():
        cells = []
        for v in r.tolist():
            if isinstance(v, float):
                cells.append(f"{v:g}")
            else:
                cells.append("" if v is None else str(v))
        rows.append(cells)
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    head = "| " + " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)) + " |"
    sep = "| " + " | ".join("-" * widths[i] for i in range(len(headers))) + " |"
    body = [
        "| " + " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)) + " |"
        for row in rows
    ]
    return "\n".join([head, sep] + body) + "\n"


def save_table(df, name, index=True):
    from src.utils.paths import TABLES

    TABLES.mkdir(parents=True, exist_ok=True)
    csv_path = TABLES / f"{name}.csv"
    md_path = TABLES / f"{name}.md"
    df.to_csv(csv_path, index=index)
    md_path.write_text(dataframe_to_markdown(df, index=index), encoding="utf-8")
    return csv_path, md_path
