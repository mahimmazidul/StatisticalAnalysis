import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from src.utils.io import load_analytic
from src.utils.style import scaled, PALETTE, apply_style, save_figure

AGE_ORDER = ["20-39", "40-59", "60-79", "80+"]


def build():
    apply_style()
    df = load_analytic()
    fig, ax = plt.subplots(figsize=scaled(8, 5.5))
    grid = np.linspace(12, 60, 400)
    offset = 0.0
    step = 0.9
    for i, age in enumerate(AGE_ORDER):
        x = df.loc[df["AgeGroup"] == age, "BMI"].dropna()
        kde = stats.gaussian_kde(x)(grid)
        kde = kde / kde.max()
        ax.fill_between(grid, offset, offset + kde, color=PALETTE[i], alpha=0.75, edgecolor="white")
        ax.text(13, offset + 0.1, f"{age} (n={len(x)})", fontsize=9, fontweight="bold")
        offset += step
    ax.set_yticks([])
    ax.set_xlabel("Body Mass Index (kg/m$^2$)")
    ax.set_title("Ridgeline Plot of BMI Distributions Across Age Groups")
    ax.spines["left"].set_visible(False)
    return save_figure(fig, "ridgeline_bmi_age", "Ridgeline of BMI by age group")


if __name__ == "__main__":
    build()
