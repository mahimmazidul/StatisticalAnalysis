import matplotlib.pyplot as plt
import seaborn as sns

from src.utils.io import load_analytic
from src.utils.style import scaled, SEX_PALETTE, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic()
    fig, ax = plt.subplots(figsize=scaled(7, 4.5))
    sns.boxplot(data=df, x="Sex", y="BMI", hue="Sex", palette=SEX_PALETTE,
                legend=False, width=0.5, fliersize=2, ax=ax)
    ax.set_xlabel("Sex")
    ax.set_ylabel("Body Mass Index (kg/m$^2$)")
    ax.set_title("Boxplot of BMI by Sex")
    return save_figure(fig, "boxplot_bmi", "Boxplot of BMI by sex")


if __name__ == "__main__":
    build()
