import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

from src.utils.io import load_analytic, save_table


def coef_table(model):
    summ = pd.DataFrame(
        {
            "Coefficient": model.params,
            "Std_Error": model.bse,
            "t": model.tvalues,
            "p_value": model.pvalues,
            "CI_Low": model.conf_int()[0],
            "CI_High": model.conf_int()[1],
        }
    )
    summ = summ.round(4)
    summ["p_value"] = model.pvalues.apply(lambda v: f"{v:.2e}")
    summ.insert(0, "Term", summ.index)
    return summ.reset_index(drop=True)


def fit_summary(model, label):
    return {
        "Model": label,
        "N": int(model.nobs),
        "R2": round(model.rsquared, 4),
        "Adj_R2": round(model.rsquared_adj, 4),
        "F": round(model.fvalue, 3),
        "F_p": f"{model.f_pvalue:.2e}",
        "AIC": round(model.aic, 1),
        "BIC": round(model.bic, 1),
    }


def vif_table(df, terms):
    sub = df[terms].dropna()
    X = sm.add_constant(sub)
    rows = []
    for i, name in enumerate(X.columns):
        if name == "const":
            continue
        rows.append({"Variable": name, "VIF": round(variance_inflation_factor(X.values, i), 3)})
    return pd.DataFrame(rows)


def main():
    df = load_analytic().copy()
    df["SexFemale"] = (df["Sex"] == "Female").astype(int)
    df["CurrentSmokerN"] = df["CurrentSmoker"].astype("float")

    simple = smf.ols("BMI ~ WaistCircumference", data=df).fit()
    save_table(coef_table(simple), "linreg_simple_bmi_waist", index=False)

    multi = smf.ols(
        "BMI ~ Age + SexFemale + EnergyKcal + FiberG + IncomePovertyRatio + CurrentSmokerN",
        data=df,
    ).fit()
    save_table(coef_table(multi), "linreg_multiple_bmi", index=False)

    sbp = smf.ols("SystolicBP ~ Age + BMI + SexFemale + SodiumMg", data=df).fit()
    save_table(coef_table(sbp), "linreg_systolic", index=False)

    fits = pd.DataFrame(
        [
            fit_summary(simple, "BMI ~ Waist (simple)"),
            fit_summary(multi, "BMI ~ demographic + diet (multiple)"),
            fit_summary(sbp, "SystolicBP ~ Age + BMI + Sex + Sodium"),
        ]
    )
    save_table(fits, "linreg_model_fit", index=False)

    vif = vif_table(df, ["Age", "BMI", "EnergyKcal", "FiberG", "IncomePovertyRatio", "SodiumMg"])
    save_table(vif, "linreg_vif", index=False)

    print(fits.to_string(index=False))
    print()
    print(vif.to_string(index=False))


if __name__ == "__main__":
    main()
