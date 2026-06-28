import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson

from src.utils.io import load_analytic, save_table


def diagnostics(model, label):
    resid = model.resid
    fitted = model.fittedvalues
    sw_w, sw_p = stats.shapiro(resid.sample(min(5000, len(resid)), random_state=1))
    bp = het_breuschpagan(resid, model.model.exog)
    dw = durbin_watson(resid)
    infl = model.get_influence()
    cooks = infl.cooks_distance[0]
    leverage = infl.hat_matrix_diag
    n = int(model.nobs)
    p = model.df_model + 1
    cook_thresh = 4 / n
    return {
        "Model": label,
        "N": n,
        "Shapiro_resid_W": round(sw_w, 4),
        "Shapiro_resid_p": f"{sw_p:.2e}",
        "BreuschPagan_LM": round(bp[0], 3),
        "BreuschPagan_p": f"{bp[1]:.2e}",
        "DurbinWatson": round(dw, 3),
        "Mean_Leverage": round(leverage.mean(), 4),
        "N_HighCooks": int((cooks > cook_thresh).sum()),
        "Max_Cooks": round(cooks.max(), 4),
        "Homoscedastic_at_5pct": "No" if bp[1] < 0.05 else "Yes",
        "Normal_Resid_at_5pct": "No" if sw_p < 0.05 else "Yes",
    }


def main():
    df = load_analytic().copy()
    df["SexFemale"] = (df["Sex"] == "Female").astype(int)
    df["CurrentSmokerN"] = df["CurrentSmoker"].astype("float")

    m1 = smf.ols("BMI ~ WaistCircumference", data=df).fit()
    m2 = smf.ols(
        "BMI ~ Age + SexFemale + EnergyKcal + FiberG + IncomePovertyRatio + CurrentSmokerN",
        data=df,
    ).fit()
    m3 = smf.ols("SystolicBP ~ Age + BMI + SexFemale + SodiumMg", data=df).fit()

    out = pd.DataFrame(
        [
            diagnostics(m1, "BMI ~ Waist"),
            diagnostics(m2, "BMI ~ demographic + diet"),
            diagnostics(m3, "SystolicBP ~ Age + BMI + Sex + Sodium"),
        ]
    )
    save_table(out, "regression_diagnostics", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
