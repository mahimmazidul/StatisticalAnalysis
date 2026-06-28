import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.analysis.pca import PCA_VARS, run_pca
from src.utils.io import load_analytic
from src.utils.style import scaled, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic()
    cols = [c for c in PCA_VARS if c in df.columns]
    res = run_pca(df, cols)
    k = 4
    load = res["loadings"][:, :k]
    fig, ax = plt.subplots(figsize=scaled(7.5, 7))
    sns.heatmap(load, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
                vmin=-1, vmax=1, yticklabels=cols,
                xticklabels=[f"PC{i+1}" for i in range(k)],
                linewidths=0.5, cbar_kws={"label": "Loading"}, ax=ax)
    ax.set_title("PCA Loading Matrix (First Four Components)")
    fig.tight_layout()
    return save_figure(fig, "pca_loadings", "PCA loadings")


if __name__ == "__main__":
    build()
