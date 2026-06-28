import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.utils.io import load_analytic
from src.utils.style import scaled, PALETTE, apply_style, save_figure

BMI_ORDER = ["Underweight", "Normal", "Overweight", "Obese"]


def build():
    apply_style()
    df = load_analytic()
    sub = df.dropna(subset=["HDL", "BMICategory"]).copy()
    sample = sub.groupby("BMICategory", observed=True).apply(
        lambda d: d.sample(min(250, len(d)), random_state=3)
    ).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=scaled(8, 5))
    sns.stripplot(data=sample, x="BMICategory", y="HDL", order=BMI_ORDER, hue="BMICategory",
                  palette=PALETTE[:4], legend=False, size=3, alpha=0.5, jitter=0.28, ax=ax)
    sns.boxplot(data=sub, x="BMICategory", y="HDL", order=BMI_ORDER, width=0.4,
                showcaps=True, boxprops={"facecolor": "none"}, showfliers=False, ax=ax)
    for i in range(len(BMI_ORDER)):
        vals = sub.loc[sub["BMICategory"] == BMI_ORDER[i], "HDL"]
        ax.plot(np.full(len(vals), -0.45), vals, "|", color="#444444", alpha=0.05)
    ax.set_xlabel("WHO BMI category")
    ax.set_ylabel("HDL cholesterol (mg/dL)")
    ax.set_title("HDL Cholesterol Across BMI Categories (Strip + Box)")
    return save_figure(fig, "strip_rug_hdl", "Strip and box HDL by BMI category")


if __name__ == "__main__":
    build()
