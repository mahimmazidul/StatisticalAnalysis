import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from src.utils.io import load_analytic
from src.utils.style import scaled, SEX_PALETTE, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic()
    fig, ax = plt.subplots(figsize=scaled(7, 4.5))
    for sex, color in SEX_PALETTE.items():
        x = df.loc[df["Sex"] == sex, "BMI"].dropna()
        grid = np.linspace(x.min(), x.max(), 300)
        kde = stats.gaussian_kde(x)(grid)
        ax.plot(grid, kde, color=color, linewidth=2, label=f"{sex} (n={len(x)})")
        ax.fill_between(grid, kde, color=color, alpha=0.18)
    ax.set_xlabel("Body Mass Index (kg/m$^2$)")
    ax.set_ylabel("Density")
    ax.set_title("Kernel Density of BMI by Sex")
    ax.legend()
    return save_figure(fig, "density_bmi", "Density of BMI by sex")


if __name__ == "__main__":
    build()
