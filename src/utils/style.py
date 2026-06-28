import matplotlib as mpl
import matplotlib.pyplot as plt
from itertools import count

PALETTE = [
    "#264653",
    "#2a9d8f",
    "#e9c46a",
    "#f4a261",
    "#e76f51",
    "#8d99ae",
    "#457b9d",
]

SEX_PALETTE = {"Male": "#264653", "Female": "#e76f51"}

DPI = 300

FIG_SCALE = 1.35

_FIG_COUNTER = count(1)
_FIG_REGISTRY = {}


def scaled(width, height):
    return (width * FIG_SCALE, height * FIG_SCALE)


def apply_style():
    mpl.rcParams.update(
        {
            "figure.dpi": 120,
            "savefig.dpi": DPI,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.25,
            "font.family": "DejaVu Sans",
            "font.size": 13,
            "axes.titlesize": 16,
            "axes.titleweight": "bold",
            "axes.titlepad": 14,
            "axes.labelsize": 13,
            "axes.labelpad": 8,
            "axes.labelweight": "regular",
            "axes.edgecolor": "#333333",
            "axes.linewidth": 1.0,
            "axes.grid": True,
            "grid.color": "#dddddd",
            "grid.linewidth": 0.7,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "legend.frameon": False,
            "legend.fontsize": 12,
            "xtick.labelsize": 11.5,
            "ytick.labelsize": 11.5,
            "xtick.color": "#333333",
            "ytick.color": "#333333",
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )


def next_figure_number(key):
    if key in _FIG_REGISTRY:
        return _FIG_REGISTRY[key]
    n = next(_FIG_COUNTER)
    _FIG_REGISTRY[key] = n
    return n


def save_figure(fig, stem, caption):
    from src.utils.paths import FIGURES

    FIGURES.mkdir(parents=True, exist_ok=True)
    png = FIGURES / f"{stem}.png"
    svg = FIGURES / f"{stem}.svg"
    fig.savefig(png)
    fig.savefig(svg)
    plt.close(fig)
    return png, svg
