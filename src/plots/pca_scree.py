import matplotlib.pyplot as plt
import numpy as np

from src.analysis.pca import PCA_VARS, run_pca
from src.utils.io import load_analytic
from src.utils.style import scaled, PALETTE, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic()
    cols = [c for c in PCA_VARS if c in df.columns]
    res = run_pca(df, cols)
    n = len(res["eigenvalues"])
    comps = np.arange(1, n + 1)
    fig, ax1 = plt.subplots(figsize=scaled(8, 4.8))
    ax1.bar(comps, res["explained"] * 100, color=PALETTE[1], alpha=0.85, label="Individual")
    ax1.axhline(100 / n, color="#888888", linestyle="--", linewidth=1, label="Kaiser-equivalent")
    ax1.set_xlabel("Principal component")
    ax1.set_ylabel("Explained variance (%)")
    ax2 = ax1.twinx()
    ax2.plot(comps, res["cum_explained"] * 100, color=PALETTE[4], marker="o", linewidth=2, label="Cumulative")
    ax2.set_ylabel("Cumulative variance (%)")
    ax2.grid(False)
    ax1.set_title("Scree Plot and Cumulative Explained Variance")
    ax1.set_xticks(comps)
    lines = ax1.get_legend_handles_labels()[0] + ax2.get_legend_handles_labels()[0]
    labels = ax1.get_legend_handles_labels()[1] + ax2.get_legend_handles_labels()[1]
    ax1.legend(lines, labels, loc="center right")
    return save_figure(fig, "pca_scree", "Scree plot")


if __name__ == "__main__":
    build()
