import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from src.utils.io import load_analytic, save_table


def odds_ratio_table(model):
    params = model.params
    conf = model.conf_int()
    out = pd.DataFrame(
        {
            "Term": params.index,
            "Coefficient": params.values.round(4),
            "Std_Error": model.bse.values.round(4),
            "z": model.tvalues.values.round(3),
            "p_value": [f"{p:.2e}" for p in model.pvalues.values],
            "Odds_Ratio": np.exp(params.values).round(3),
            "OR_CI_Low": np.exp(conf[0].values).round(3),
            "OR_CI_High": np.exp(conf[1].values).round(3),
        }
    )
    return out.reset_index(drop=True)


def fit_summary(model, label):
    ll = model.llf
    ll0 = model.llnull
    mcfadden = 1 - ll / ll0
    return {
        "Model": label,
        "N": int(model.nobs),
        "LL": round(ll, 1),
        "LL_null": round(ll0, 1),
        "McFadden_R2": round(mcfadden, 4),
        "LR_chi2": round(model.llr, 2),
        "LR_p": f"{model.llr_pvalue:.2e}",
        "AIC": round(model.aic, 1),
    }


def main():
    df = load_analytic().copy()
    df["SexFemale"] = (df["Sex"] == "Female").astype(int)
    df["CurrentSmokerN"] = df["CurrentSmoker"].astype("float")
    df["ObeseN"] = df["Obese"].astype("float")
    df["HypertensiveN"] = df["Hypertensive"].astype("float")

    obese_model = smf.logit(
        "ObeseN ~ Age + SexFemale + EnergyKcal + FiberG + IncomePovertyRatio + CurrentSmokerN",
        data=df,
    ).fit(disp=False)
    save_table(odds_ratio_table(obese_model), "logit_obesity", index=False)

    htn_model = smf.logit(
        "HypertensiveN ~ Age + BMI + SexFemale + SodiumMg + CurrentSmokerN",
        data=df,
    ).fit(disp=False)
    save_table(odds_ratio_table(htn_model), "logit_hypertension", index=False)

    fits = pd.DataFrame(
        [
            fit_summary(obese_model, "Obesity (BMI>=30)"),
            fit_summary(htn_model, "Hypertension (>=130/80)"),
        ]
    )
    save_table(fits, "logit_model_fit", index=False)
    print(fits.to_string(index=False))
    print()
    print(odds_ratio_table(obese_model)[["Term", "Odds_Ratio", "OR_CI_Low", "OR_CI_High", "p_value"]].to_string(index=False))


if __name__ == "__main__":
    main()
