import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.utils.io import load_analytic
from src.utils.style import scaled, PALETTE, apply_style, save_figure

BMI_ORDER = ["Underweight", "Normal", "Overweight", "Obese"]
SMOKE_ORDER = ["Never", "Former", "Current"]


def build():
    apply_style()
    df = load_analytic()
    ct = pd.crosstab(df["SmokingStatus"], df["BMICategory"], normalize="index") * 100
    ct = ct.reindex(index=SMOKE_ORDER, columns=BMI_ORDER)
    fig, ax = plt.subplots(figsize=scaled(8, 4.8))
    bottom = np.zeros(len(ct))
    for i, cat in enumerate(BMI_ORDER):
        ax.bar(ct.index, ct[cat].values, bottom=bottom, color=PALETTE[i], label=cat, edgecolor="white")
        bottom += ct[cat].values
    ax.set_ylabel("Percent within smoking status (%)")
    ax.set_xlabel("Smoking status")
    ax.set_title("BMI Category Composition by Smoking Status")
    ax.legend(title="BMI category", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    return save_figure(fig, "stacked_bar_smoking_bmi", "Stacked bar smoking by BMI")


if __name__ == "__main__":
    build()
