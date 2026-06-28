import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

from src.utils.io import load_analytic
from src.utils.style import scaled, PALETTE, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic().copy()
    df["SexFemale"] = (df["Sex"] == "Female").astype(int)
    model = smf.ols("SystolicBP ~ Age + BMI + SexFemale + SodiumMg", data=df).fit()
    fitted = model.fittedvalues
    resid = model.resid
    infl = model.get_influence()
    std_resid = infl.resid_studentized_internal
    leverage = infl.hat_matrix_diag
    cooks = infl.cooks_distance[0]

    fig, axes = plt.subplots(2, 2, figsize=scaled(11, 9))

    ax = axes[0, 0]
    ax.scatter(fitted, resid, s=8, alpha=0.3, color=PALETTE[1])
    ax.axhline(0, color="#e63946", linewidth=1.5)
    ax.set_xlabel("Fitted values")
    ax.set_ylabel("Residuals")
    ax.set_title("Residuals vs Fitted")

    ax = axes[0, 1]
    sm.qqplot(resid, line="45", fit=True, ax=ax, markerfacecolor=PALETTE[1],
              markeredgecolor=PALETTE[0], alpha=0.3)
    ax.set_title("Normal Q-Q of Residuals")

    ax = axes[1, 0]
    ax.scatter(fitted, np.sqrt(np.abs(std_resid)), s=8, alpha=0.3, color=PALETTE[3])
    ax.set_xlabel("Fitted values")
    ax.set_ylabel(r"$\sqrt{|Standardized\ residuals|}$")
    ax.set_title("Scale-Location")

    ax = axes[1, 1]
    ax.scatter(leverage, std_resid, s=8, alpha=0.3, color=PALETTE[4])
    ax.axhline(0, color="#888888", linewidth=1)
    big = np.argsort(cooks)[-3:]
    ax.scatter(leverage[big], std_resid[big], s=40, facecolors="none", edgecolors="#e63946")
    ax.set_xlabel("Leverage")
    ax.set_ylabel("Standardized residuals")
    ax.set_title("Residuals vs Leverage (Cook's distance flagged)")

    fig.suptitle("Regression Diagnostics: SystolicBP ~ Age + BMI + Sex + Sodium", fontweight="bold")
    fig.tight_layout()
    return save_figure(fig, "residual_plot", "Regression diagnostics panel")


if __name__ == "__main__":
    build()
