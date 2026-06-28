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
    scores = res["scores"]
    load = res["loadings"]
    idx = res["index"]
    bmicat = df.loc[idx, "BMICategory"].astype(str).values

    fig, ax = plt.subplots(figsize=scaled(8.5, 7))
    cmap = {"Underweight": PALETTE[6], "Normal": PALETTE[1], "Overweight": PALETTE[2], "Obese": PALETTE[4]}
    for cat, c in cmap.items():
        m = bmicat == cat
        ax.scatter(scores[m, 0], scores[m, 1], s=7, alpha=0.25, color=c, label=cat)

    scale = np.abs(scores[:, :2]).max() * 0.9
    label_offsets = {
        "BMI": (0.0, 0.45),
        "WaistCircumference": (-0.2, -0.35),
        "Weight": (-0.3, 0.0),
        "EnergyKcal": (0.0, -0.45),
        "ProteinG": (-0.1, 0.4),
        "SodiumMg": (0.4, 0.1),
        "SystolicBP": (-0.4, 0.3),
        "DiastolicBP": (0.0, -0.4),
        "Age": (0.35, 0.25),
        "HDL": (0.3, -0.2),
        "FiberG": (0.35, 0.0),
    }
    for i, name in enumerate(cols):
        ax.arrow(0, 0, load[i, 0] * scale, load[i, 1] * scale, color="#222222",
                 width=0.003, head_width=0.12, alpha=0.8, length_includes_head=True)
        dx, dy = label_offsets.get(name, (0.0, 0.0))
        ax.text(load[i, 0] * scale * 1.12 + dx, load[i, 1] * scale * 1.12 + dy, name,
                fontsize=8, color="#111111", ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.7))
    ax.axhline(0, color="#cccccc", linewidth=0.8)
    ax.axvline(0, color="#cccccc", linewidth=0.8)
    ax.set_xlabel(f"PC1 ({res['explained'][0]*100:.1f}%)")
    ax.set_ylabel(f"PC2 ({res['explained'][1]*100:.1f}%)")
    ax.set_title("PCA Biplot of Anthropometric, Dietary and Clinical Variables")
    ax.legend(title="BMI category", markerscale=2)
    return save_figure(fig, "pca_biplot", "PCA biplot")


if __name__ == "__main__":
    build()
