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
    model = smf.logit(
        "Obese ~ Age + SexFemale + EnergyKcal + FiberG + IncomePovertyRatio + CurrentSmokerN",
        data=df.assign(Obese=df["Obese"].astype("float")),
    ).fit(disp=False)
    params = model.params.drop("Intercept")
    conf = model.conf_int().drop("Intercept")
    or_ = np.exp(params)
    lo = np.exp(conf[0])
    hi = np.exp(conf[1])

    labels = {
        "Age": "Age (per year)",
        "SexFemale": "Female vs Male",
        "EnergyKcal": "Energy (per kcal)",
        "FiberG": "Fiber (per g)",
        "IncomePovertyRatio": "Income-poverty ratio",
        "CurrentSmokerN": "Current smoker",
    }
    names = [labels.get(i, i) for i in params.index]
    y = np.arange(len(params))[::-1]

    fig, ax = plt.subplots(figsize=scaled(7.5, 4.5))
    ax.errorbar(or_, y, xerr=[or_ - lo, hi - or_], fmt="o", color=PALETTE[0],
                ecolor=PALETTE[4], elinewidth=2, capsize=4, markersize=7)
    ax.axvline(1, color="#888888", linestyle="--", linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.set_xlabel("Adjusted odds ratio (95% CI)")
    ax.set_title("Adjusted Odds Ratios for Obesity (Logistic Regression)")
    for yi, o, l, h in zip(y, or_, lo, hi):
        ax.text(hi.max() * 1.05, yi, f"{o:.2f} ({l:.2f}-{h:.2f})", va="center", fontsize=8)
    ax.set_xlim(left=min(0.5, lo.min() * 0.9))
    return save_figure(fig, "forest_plot", "Forest plot of odds ratios")


if __name__ == "__main__":
    build()
