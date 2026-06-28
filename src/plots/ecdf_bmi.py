import matplotlib.pyplot as plt
import numpy as np

from src.utils.io import load_analytic
from src.utils.style import scaled, SEX_PALETTE, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic()
    fig, ax = plt.subplots(figsize=scaled(7, 4.5))
    for sex, color in SEX_PALETTE.items():
        x = np.sort(df.loc[df["Sex"] == sex, "BMI"].dropna().values)
        y = np.arange(1, len(x) + 1) / len(x)
        ax.step(x, y, where="post", color=color, linewidth=2, label=sex)
    ax.axvline(30, color="#888888", linestyle="--", linewidth=1, label="Obesity threshold")
    ax.set_xlabel("Body Mass Index (kg/m$^2$)")
    ax.set_ylabel("Cumulative proportion")
    ax.set_title("Empirical Cumulative Distribution of BMI by Sex")
    ax.legend()
    return save_figure(fig, "ecdf_bmi", "ECDF of BMI by sex")


if __name__ == "__main__":
    build()
