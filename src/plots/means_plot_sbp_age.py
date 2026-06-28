import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from src.utils.io import load_analytic
from src.utils.style import scaled, SEX_PALETTE, apply_style, save_figure

AGE_ORDER = ["20-39", "40-59", "60-79", "80+"]


def build():
    apply_style()
    df = load_analytic()
    fig, ax = plt.subplots(figsize=scaled(8, 5))
    for sex, color in SEX_PALETTE.items():
        means, los, his = [], [], []
        for age in AGE_ORDER:
            x = df.loc[(df["Sex"] == sex) & (df["AgeGroup"] == age), "SystolicBP"].dropna()
            m = x.mean()
            se = x.std(ddof=1) / np.sqrt(len(x))
            t = stats.t.ppf(0.975, len(x) - 1)
            means.append(m)
            los.append(t * se)
            his.append(t * se)
        ax.errorbar(AGE_ORDER, means, yerr=[los, his], marker="o", color=color,
                    capsize=4, linewidth=2, label=sex)
    ax.set_xlabel("Age group (years)")
    ax.set_ylabel("Mean systolic BP (mmHg)")
    ax.set_title("Mean Systolic Blood Pressure by Age Group and Sex (95% CI)")
    ax.legend()
    return save_figure(fig, "means_plot_sbp_age", "Means plot systolic BP")


if __name__ == "__main__":
    build()
