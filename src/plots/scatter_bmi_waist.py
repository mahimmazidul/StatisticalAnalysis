import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from src.utils.io import load_analytic
from src.utils.style import scaled, PALETTE, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic()
    sub = df[["WaistCircumference", "BMI", "Sex"]].dropna()
    fig, ax = plt.subplots(figsize=scaled(7, 5))
    colors = {"Male": PALETTE[0], "Female": PALETTE[4]}
    for sex, c in colors.items():
        s = sub[sub["Sex"] == sex]
        ax.scatter(s["WaistCircumference"], s["BMI"], s=8, alpha=0.3, color=c, label=sex)
    x = sub["WaistCircumference"].values
    y = sub["BMI"].values
    slope, intercept, r, p, se = stats.linregress(x, y)
    xs = np.linspace(x.min(), x.max(), 100)
    ax.plot(xs, intercept + slope * xs, color="#111111", linewidth=2,
            label=f"OLS: y={intercept:.1f}+{slope:.2f}x\nr={r:.2f}")
    ax.set_xlabel("Waist circumference (cm)")
    ax.set_ylabel("Body Mass Index (kg/m$^2$)")
    ax.set_title("Association Between Waist Circumference and BMI")
    ax.legend()
    return save_figure(fig, "scatter_bmi_waist", "Scatter of BMI vs waist")


if __name__ == "__main__":
    build()
