import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from src.utils.io import load_analytic
from src.utils.style import scaled, PALETTE, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic()
    x = df["BMI"].dropna()
    fig, ax = plt.subplots(figsize=scaled(7, 4.5))
    ax.hist(x, bins=40, color=PALETTE[1], edgecolor="white", alpha=0.85, density=True)
    grid = np.linspace(x.min(), x.max(), 300)
    ax.plot(grid, stats.gaussian_kde(x)(grid), color=PALETTE[4], linewidth=2, label="Kernel density")
    ax.axvline(x.mean(), color=PALETTE[0], linestyle="--", linewidth=1.5, label=f"Mean = {x.mean():.1f}")
    ax.axvline(x.median(), color=PALETTE[3], linestyle=":", linewidth=1.5, label=f"Median = {x.median():.1f}")
    ax.set_xlabel("Body Mass Index (kg/m$^2$)")
    ax.set_ylabel("Density")
    ax.set_title("Distribution of Body Mass Index in U.S. Adults")
    ax.legend()
    return save_figure(fig, "histogram_bmi", "Distribution of BMI")


if __name__ == "__main__":
    build()
