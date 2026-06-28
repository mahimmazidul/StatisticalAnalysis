import matplotlib.pyplot as plt
import seaborn as sns

from src.data_cleaning.rename import CONTINUOUS
from src.utils.io import load_analytic
from src.utils.style import scaled, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic()
    cols = [c for c in CONTINUOUS if c in df.columns]
    corr = df[cols].corr()
    g = sns.clustermap(corr, cmap="RdBu_r", center=0, vmin=-1, vmax=1,
                       annot=True, fmt=".2f", annot_kws={"size": 9},
                       linewidths=0.4, figsize=scaled(10, 9),
                       cbar_kws={"label": "Pearson r"})
    g.figure.suptitle("Hierarchically Clustered Correlation Heatmap", y=1.02, fontweight="bold")
    from src.utils.paths import FIGURES
    FIGURES.mkdir(parents=True, exist_ok=True)
    png = FIGURES / "correlation_clustered.png"
    svg = FIGURES / "correlation_clustered.svg"
    g.figure.savefig(png, dpi=300, bbox_inches="tight")
    g.figure.savefig(svg, bbox_inches="tight")
    plt.close(g.figure)
    return png, svg


if __name__ == "__main__":
    build()
