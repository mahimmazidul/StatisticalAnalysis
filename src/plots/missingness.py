import matplotlib.pyplot as plt
import missingno as msno

from src.data_cleaning.rename import BINARY, CONTINUOUS
from src.utils.io import load_analytic
from src.utils.paths import FIGURES
from src.utils.style import apply_style


def _save(fig, stem):
    FIGURES.mkdir(parents=True, exist_ok=True)
    png = FIGURES / f"{stem}.png"
    svg = FIGURES / f"{stem}.svg"
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(svg, bbox_inches="tight")
    plt.close(fig)
    return png, svg


def build():
    apply_style()
    df = load_analytic()
    cols = [c for c in CONTINUOUS + BINARY if c in df.columns]
    sub = df[cols]

    ax = msno.matrix(sub, color=(0.16, 0.31, 0.40), figsize=(20, 11), fontsize=15, labels=True)
    fig = ax.get_figure()
    ax.set_title("Missing Value Matrix", fontweight="bold", fontsize=22, pad=90)
    _save(fig, "missing_matrix")

    ax = msno.bar(sub, color="#2a9d8f", figsize=(20, 10), fontsize=15)
    fig = ax.get_figure()
    ax.set_title("Observed Counts by Variable", fontweight="bold", fontsize=22, pad=90)
    _save(fig, "missing_bar")

    ax = msno.heatmap(sub, cmap="RdBu", figsize=(18, 14), fontsize=14)
    fig = ax.get_figure()
    ax.set_title("Missingness Correlation Heatmap", fontweight="bold", fontsize=22, pad=40)
    return _save(fig, "missing_heatmap")


if __name__ == "__main__":
    build()
