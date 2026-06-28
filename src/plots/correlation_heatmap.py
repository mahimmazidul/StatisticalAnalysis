import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.data_cleaning.rename import CONTINUOUS
from src.utils.io import load_analytic
from src.utils.style import scaled, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic()
    cols = [c for c in CONTINUOUS if c in df.columns]
    corr = df[cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    fig, ax = plt.subplots(figsize=scaled(10, 8.5))
    sns.heatmap(corr, mask=mask, cmap="RdBu_r", center=0, vmin=-1, vmax=1,
                annot=True, fmt=".2f", annot_kws={"size": 9.5}, square=True,
                linewidths=0.5, cbar_kws={"label": "Pearson r", "shrink": 0.7}, ax=ax)
    ax.set_title("Pearson Correlation Matrix of Anthropometric, Dietary and Clinical Variables")
    fig.tight_layout()
    return save_figure(fig, "correlation_heatmap", "Correlation heatmap")


if __name__ == "__main__":
    build()
