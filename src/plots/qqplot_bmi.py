import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

from src.utils.io import load_analytic
from src.utils.style import scaled, PALETTE, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic()
    fig, axes = plt.subplots(1, 2, figsize=scaled(11, 4.5))
    for ax, col, title in zip(axes, ["BMI", "BMI"], ["BMI (raw)", "log(BMI)"]):
        data = df[col].dropna()
        if "log" in title:
            data = np.log(data)
        sm.qqplot(data, line="45", fit=True, ax=ax, markerfacecolor=PALETTE[1],
                  markeredgecolor=PALETTE[0], alpha=0.4)
        ax.set_title(f"Normal Q-Q: {title}")
    fig.suptitle("Quantile-Quantile Assessment of Normality for BMI", fontweight="bold")
    fig.tight_layout()
    return save_figure(fig, "qqplot_bmi", "QQ plot of BMI")


if __name__ == "__main__":
    build()
