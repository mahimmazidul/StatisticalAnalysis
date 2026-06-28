import matplotlib.pyplot as plt
import numpy as np
import statsmodels.formula.api as smf

from src.utils.io import load_analytic
from src.utils.style import scaled, PALETTE, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic().copy()
    df["SexFemale"] = (df["Sex"] == "Female").astype(int)
    df["CurrentSmokerN"] = df["CurrentSmoker"].astype("float")
    z = df.copy()
    for c in ["Age", "EnergyKcal", "FiberG", "IncomePovertyRatio"]:
        z[c] = (z[c] - z[c].mean()) / z[c].std(ddof=1)
    model = smf.ols(
        "BMI ~ Age + SexFemale + EnergyKcal + FiberG + IncomePovertyRatio + CurrentSmokerN",
        data=z,
    ).fit()
    params = model.params.drop("Intercept")
    conf = model.conf_int().drop("Intercept")
    names = list(params.index)
    y = np.arange(len(params))[::-1]
    fig, ax = plt.subplots(figsize=scaled(7.5, 4.5))
    ax.errorbar(params.values, y, xerr=[params.values - conf[0].values, conf[1].values - params.values],
                fmt="o", color=PALETTE[0], ecolor=PALETTE[2], elinewidth=2, capsize=4, markersize=7)
    ax.axvline(0, color="#888888", linestyle="--", linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.set_xlabel("Standardized regression coefficient (95% CI)")
    ax.set_title("Standardized Predictors of BMI (Multiple Linear Regression)")
    return save_figure(fig, "coefficient_plot_linear", "Coefficient plot linear regression")


if __name__ == "__main__":
    build()
