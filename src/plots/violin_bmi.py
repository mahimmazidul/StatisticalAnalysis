import matplotlib.pyplot as plt
import seaborn as sns

from src.utils.io import load_analytic
from src.utils.style import scaled, PALETTE, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic()
    order = ["20-39", "40-59", "60-79", "80+"]
    fig, ax = plt.subplots(figsize=scaled(8, 4.5))
    sns.violinplot(data=df, x="AgeGroup", y="BMI", order=order, hue="AgeGroup",
                   palette=PALETTE[:4], legend=False, inner="quartile", cut=0, ax=ax)
    ax.set_xlabel("Age group (years)")
    ax.set_ylabel("Body Mass Index (kg/m$^2$)")
    ax.set_title("Violin Plot of BMI Across Age Groups")
    return save_figure(fig, "violin_bmi", "Violin plot of BMI by age group")


if __name__ == "__main__":
    build()
