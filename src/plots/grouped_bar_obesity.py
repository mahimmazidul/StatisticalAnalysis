import matplotlib.pyplot as plt
import numpy as np

from src.utils.io import load_analytic
from src.utils.style import scaled, SEX_PALETTE, apply_style, save_figure

AGE_ORDER = ["20-39", "40-59", "60-79", "80+"]


def build():
    apply_style()
    df = load_analytic()
    g = df.dropna(subset=["Obese"]).groupby(["AgeGroup", "Sex"], observed=True)["Obese"].mean().unstack() * 100
    g = g.reindex(AGE_ORDER)
    x = np.arange(len(AGE_ORDER))
    w = 0.38
    fig, ax = plt.subplots(figsize=scaled(8, 4.8))
    ax.bar(x - w / 2, g["Male"].values, w, color=SEX_PALETTE["Male"], label="Male")
    ax.bar(x + w / 2, g["Female"].values, w, color=SEX_PALETTE["Female"], label="Female")
    ax.set_xticks(x)
    ax.set_xticklabels(AGE_ORDER)
    ax.set_ylabel("Obesity prevalence (%)")
    ax.set_xlabel("Age group (years)")
    ax.set_title("Obesity Prevalence by Age Group and Sex")
    ax.legend()
    return save_figure(fig, "grouped_bar_obesity", "Grouped bar obesity by age and sex")


if __name__ == "__main__":
    build()
