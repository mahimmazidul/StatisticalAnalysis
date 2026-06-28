import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from src.utils.io import load_analytic
from src.utils.style import scaled, PALETTE, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic()
    sub = df[["EnergyKcal", "BMI"]].dropna()
    x, y = sub["EnergyKcal"].values, sub["BMI"].values
    fig, ax = plt.subplots(figsize=scaled(7, 5))
    hb = ax.hexbin(x, y, gridsize=35, cmap="viridis", mincnt=1)
    fig.colorbar(hb, ax=ax, label="Count")
    slope, intercept, r, p, se = stats.linregress(x, y)
    xs = np.linspace(x.min(), x.max(), 100)
    ax.plot(xs, intercept + slope * xs, color="#e63946", linewidth=2,
            label=f"OLS slope={slope:.4f}\nr={r:.2f}, p={p:.1e}")
    ax.set_xlabel("Day-1 energy intake (kcal)")
    ax.set_ylabel("Body Mass Index (kg/m$^2$)")
    ax.set_title("Energy Intake and BMI (Hexbin Density)")
    ax.legend()
    return save_figure(fig, "scatter_bmi_energy", "Hexbin of BMI vs energy")


if __name__ == "__main__":
    build()
