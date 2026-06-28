import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from src.utils.io import load_analytic
from src.utils.style import scaled, SEX_PALETTE, apply_style, save_figure


def build():
    apply_style()
    df = load_analytic().copy()
    df["SexFemale"] = (df["Sex"] == "Female").astype(int)
    model = smf.ols("SystolicBP ~ Age + BMI + SexFemale + SodiumMg", data=df).fit()

    ages = np.linspace(20, 80, 100)
    fig, ax = plt.subplots(figsize=scaled(7.5, 5))
    for sex, female in [("Male", 0), ("Female", 1)]:
        newdata = pd.DataFrame(
            {
                "Age": ages,
                "BMI": df["BMI"].median(),
                "SexFemale": female,
                "SodiumMg": df["SodiumMg"].median(),
            }
        )
        pred = model.get_prediction(newdata).summary_frame(alpha=0.05)
        ax.plot(ages, pred["mean"], color=SEX_PALETTE[sex], linewidth=2, label=sex)
        ax.fill_between(ages, pred["mean_ci_lower"], pred["mean_ci_upper"],
                        color=SEX_PALETTE[sex], alpha=0.18)
    ax.set_xlabel("Age (years)")
    ax.set_ylabel("Predicted systolic BP (mmHg)")
    ax.set_title("Predicted Systolic Blood Pressure by Age and Sex (at median BMI and sodium)")
    ax.legend()
    return save_figure(fig, "prediction_plot", "Prediction plot of systolic BP")


if __name__ == "__main__":
    build()
