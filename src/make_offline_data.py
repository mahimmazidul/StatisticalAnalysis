import numpy as np
import pandas as pd

from src.utils.paths import DATA_RAW, ensure_dirs

SEED = 20172018
N = 9254


def _generate():
    rng = np.random.default_rng(SEED)
    seqn = np.arange(93703, 93703 + N)

    sex = rng.choice([1, 2], size=N, p=[0.492, 0.508])
    age = np.clip(rng.gamma(2.0, 17, size=N), 0, 80).round().astype(int)

    reth = rng.choice([1, 2, 3, 4, 6, 7], size=N, p=[0.148, 0.089, 0.340, 0.229, 0.126, 0.068])

    pir = np.clip(rng.gamma(2.4, 1.0, size=N), 0, 5).round(2)

    educ = np.full(N, np.nan)
    adult = age >= 20
    educ_codes = rng.choice([1, 2, 3, 4, 5], size=N, p=[0.085, 0.114, 0.236, 0.317, 0.248])
    educ[adult] = educ_codes[adult]

    base_bmi = 18 + 0.18 * np.minimum(age, 60) + 2.2 * (pir < 2)
    bmi = base_bmi + rng.normal(0, 5.5, size=N)
    bmi = np.clip(bmi, 12.3, 86.2).round(1)
    child = age < 16
    bmi[child] = np.clip(14 + 0.4 * age[child] + rng.normal(0, 2.5, size=child.sum()), 12.3, 40).round(1)
    height = np.clip(150 + 14 * (sex == 1) + rng.normal(0, 8, size=N), 90, 200).round(1)
    height[child] = np.clip(70 + 5.5 * age[child] + rng.normal(0, 5, size=child.sum()), 70, 185).round(1)
    weight = (bmi * (height / 100) ** 2).round(1)
    waist = np.clip(0.5 * height + 0.8 * (bmi - 22) + rng.normal(0, 6, size=N), 50, 175).round(1)

    kcal_mu = np.exp(7.35 + 0.10 * (sex == 1) - 0.004 * np.maximum(age - 50, 0))
    kcal = np.clip(rng.lognormal(np.log(kcal_mu), 0.42), 200, 12500).round(0)
    prot = np.clip(kcal * rng.normal(0.16, 0.03, size=N) / 4, 5, None).round(1)
    carb = np.clip(kcal * rng.normal(0.48, 0.05, size=N) / 4, 10, None).round(1)
    tfat = np.clip(kcal * rng.normal(0.34, 0.05, size=N) / 9, 3, None).round(1)
    sugr = np.clip(carb * rng.normal(0.42, 0.12, size=N), 1, None).round(1)
    fibe = np.clip(kcal / 1000 * rng.normal(8.5, 3.0, size=N), 0.5, None).round(1)
    sodi = np.clip(kcal * rng.normal(1.55, 0.35, size=N), 100, None).round(0)

    miss_diet = rng.random(N) < 0.06
    for arr in [kcal, prot, carb, tfat, sugr, fibe, sodi]:
        arr[miss_diet] = np.nan

    sbp = np.clip(95 + 0.45 * age + 0.35 * (bmi - 25) + rng.normal(0, 11, size=N), 70, 230).round(0)
    dbp = np.clip(60 + 0.10 * age + 0.20 * (bmi - 25) + rng.normal(0, 9, size=N), 40, 140).round(0)
    miss_bp = (rng.random(N) < 0.10) | (age < 8)
    sbp[miss_bp] = np.nan
    dbp[miss_bp] = np.nan

    smq020 = np.full(N, np.nan)
    p_smoke = 1 / (1 + np.exp(-(-1.0 + 0.015 * (age - 40) - 0.25 * (pir > 3))))
    ever = (rng.random(N) < p_smoke).astype(float)
    smq020[adult] = np.where(ever[adult] == 1, 1, 2)
    smq040 = np.full(N, np.nan)
    ever_adult = adult & (smq020 == 1)
    cur = rng.choice([1, 2, 3], size=N, p=[0.40, 0.07, 0.53])
    smq040[ever_adult] = cur[ever_adult]

    alq121 = np.full(N, np.nan)
    alq_elig = age >= 18
    alq121[alq_elig] = rng.choice(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], size=alq_elig.sum(),
        p=[0.18, 0.05, 0.06, 0.07, 0.08, 0.10, 0.12, 0.10, 0.10, 0.07, 0.07],
    )

    hdl = np.clip(rng.normal(54 - 6 * (sex == 1) - 0.10 * (bmi - 25), 13, size=N), 15, 150).round(0)
    miss_hdl = rng.random(N) < 0.20
    hdl[miss_hdl] = np.nan

    glu = np.clip(rng.lognormal(np.log(98 + 0.25 * age + 0.6 * (bmi - 25)), 0.18, size=N), 55, 400).round(0)
    miss_glu = rng.random(N) < 0.67
    glu[miss_glu] = np.nan

    demo = pd.DataFrame(
        {"SEQN": seqn, "RIAGENDR": sex, "RIDAGEYR": age, "RIDRETH3": reth,
         "DMDEDUC2": educ, "INDFMPIR": pir}
    )
    bmx = pd.DataFrame(
        {"SEQN": seqn, "BMXWT": weight, "BMXHT": height, "BMXBMI": bmi, "BMXWAIST": waist}
    )
    dr = pd.DataFrame(
        {"SEQN": seqn, "DR1TKCAL": kcal, "DR1TPROT": prot, "DR1TCARB": carb,
         "DR1TSUGR": sugr, "DR1TTFAT": tfat, "DR1TFIBE": fibe, "DR1TSODI": sodi}
    )
    smq = pd.DataFrame({"SEQN": seqn, "SMQ020": smq020, "SMQ040": smq040})
    bpx = pd.DataFrame({"SEQN": seqn, "BPXSY1": sbp, "BPXDI1": dbp})
    alq = pd.DataFrame({"SEQN": seqn, "ALQ121": alq121})
    hdlf = pd.DataFrame({"SEQN": seqn, "LBDHDD": hdl})
    gluf = pd.DataFrame({"SEQN": seqn, "LBXGLU": glu})
    return demo, bmx, dr, smq, bpx, alq, hdlf, gluf


def main():
    ensure_dirs()
    demo, bmx, dr, smq, bpx, alq, hdlf, gluf = _generate()
    mapping = {
        "DEMO_J": demo, "BMX_J": bmx, "DR1TOT_J": dr, "SMQ_J": smq,
        "BPX_J": bpx, "ALQ_J": alq, "HDL_J": hdlf, "GLU_J": gluf,
    }
    for name, df in mapping.items():
        df.to_csv(DATA_RAW / f"{name}.csv", index=False)
    print(f"Generated reproducible offline NHANES-style data for {len(mapping)} domains.")
    print(f"Records: {len(demo)} (seed={SEED}).")


if __name__ == "__main__":
    main()
