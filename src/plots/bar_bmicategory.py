import matplotlib.pyplot as plt

from src.utils.io import load_analytic
from src.utils.style import scaled, PALETTE, apply_style, save_figure

ORDER = ["Underweight", "Normal", "Overweight", "Obese"]


def build():
    apply_style()
    df = load_analytic()
    counts = df["BMICategory"].value_counts().reindex(ORDER)
    pct = counts / counts.sum() * 100
    fig, ax = plt.subplots(figsize=scaled(7, 4.5))
    bars = ax.bar(ORDER, pct.values, color=PALETTE[:4], edgecolor="white")
    for b, p in zip(bars, pct.values):
        ax.text(b.get_x() + b.get_width() / 2, p + 0.6, f"{p:.1f}%", ha="center", fontsize=9)
    ax.set_ylabel("Percent of adults (%)")
    ax.set_xlabel("WHO BMI category")
    ax.set_title("Prevalence of BMI Categories in U.S. Adults")
    return save_figure(fig, "bar_bmicategory", "BMI category prevalence")


if __name__ == "__main__":
    build()
