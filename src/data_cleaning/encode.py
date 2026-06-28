import numpy as np
import pandas as pd

SEX_MAP = {1: "Male", 2: "Female"}
RETH_MAP = {
    1: "Mexican American",
    2: "Other Hispanic",
    3: "Non-Hispanic White",
    4: "Non-Hispanic Black",
    6: "Non-Hispanic Asian",
    7: "Other/Multi",
}
EDUC_MAP = {
    1: "< 9th grade",
    2: "9-11th grade",
    3: "High school/GED",
    4: "Some college",
    5: "College graduate+",
}
EDUC_ORDER = ["< 9th grade", "9-11th grade", "High school/GED", "Some college", "College graduate+"]
SMOKE_ORDER = ["Never", "Former", "Current"]
BMI_ORDER = ["Underweight", "Normal", "Overweight", "Obese"]
AGE_ORDER = ["20-39", "40-59", "60-79", "80+"]
PIR_ORDER = ["< 1.30", "1.30-3.49", ">= 3.50"]


def _smoking_status(row):
    if pd.isna(row["SMQ020"]):
        return np.nan
    if row["SMQ020"] == 2:
        return "Never"
    if row["SMQ040"] in (1, 2):
        return "Current"
    return "Former"


def _bmi_category(b):
    if pd.isna(b):
        return np.nan
    if b < 18.5:
        return "Underweight"
    if b < 25:
        return "Normal"
    if b < 30:
        return "Overweight"
    return "Obese"


def _age_group(a):
    if a < 40:
        return "20-39"
    if a < 60:
        return "40-59"
    if a < 80:
        return "60-79"
    return "80+"


def _pir_group(p):
    if pd.isna(p):
        return np.nan
    if p < 1.30:
        return "< 1.30"
    if p < 3.50:
        return "1.30-3.49"
    return ">= 3.50"


def encode(df):
    df = df.copy()
    df["Sex"] = df["RIAGENDR"].map(SEX_MAP)
    df["RaceEthnicity"] = df["RIDRETH3"].map(RETH_MAP)
    df["Education"] = df["DMDEDUC2"].map(EDUC_MAP)
    df["SmokingStatus"] = df.apply(_smoking_status, axis=1)
    df["BMICategory"] = df["BMI"].apply(_bmi_category)
    df["AgeGroup"] = df["Age"].apply(_age_group)
    df["IncomeGroup"] = df["IncomePovertyRatio"].apply(_pir_group)

    df["Obese"] = (df["BMI"] >= 30).astype("Int64")
    df.loc[df["BMI"].isna(), "Obese"] = pd.NA
    df["Hypertensive"] = ((df["SystolicBP"] >= 130) | (df["DiastolicBP"] >= 80)).astype("Int64")
    df.loc[df["SystolicBP"].isna() & df["DiastolicBP"].isna(), "Hypertensive"] = pd.NA
    df["CurrentSmoker"] = (df["SmokingStatus"] == "Current").astype("Int64")
    df.loc[df["SmokingStatus"].isna(), "CurrentSmoker"] = pd.NA

    df["Education"] = pd.Categorical(df["Education"], categories=EDUC_ORDER, ordered=True)
    df["SmokingStatus"] = pd.Categorical(df["SmokingStatus"], categories=SMOKE_ORDER, ordered=True)
    df["BMICategory"] = pd.Categorical(df["BMICategory"], categories=BMI_ORDER, ordered=True)
    df["AgeGroup"] = pd.Categorical(df["AgeGroup"], categories=AGE_ORDER, ordered=True)
    df["IncomeGroup"] = pd.Categorical(df["IncomeGroup"], categories=PIR_ORDER, ordered=True)
    return df
