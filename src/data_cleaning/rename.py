RENAME = {
    "RIDAGEYR": "Age",
    "INDFMPIR": "IncomePovertyRatio",
    "BMXBMI": "BMI",
    "BMXWT": "Weight",
    "BMXHT": "Height",
    "BMXWAIST": "WaistCircumference",
    "DR1TKCAL": "EnergyKcal",
    "DR1TPROT": "ProteinG",
    "DR1TCARB": "CarbohydrateG",
    "DR1TSUGR": "SugarG",
    "DR1TTFAT": "TotalFatG",
    "DR1TFIBE": "FiberG",
    "DR1TSODI": "SodiumMg",
    "BPXSY1": "SystolicBP",
    "BPXDI1": "DiastolicBP",
    "LBDHDD": "HDL",
    "LBXGLU": "FastingGlucose",
}

CONTINUOUS = [
    "Age", "IncomePovertyRatio", "BMI", "Weight", "Height", "WaistCircumference",
    "EnergyKcal", "ProteinG", "CarbohydrateG", "SugarG", "TotalFatG", "FiberG",
    "SodiumMg", "SystolicBP", "DiastolicBP", "HDL", "FastingGlucose",
]

CATEGORICAL = [
    "Sex", "RaceEthnicity", "Education", "SmokingStatus", "BMICategory",
    "AgeGroup", "IncomeGroup",
]

BINARY = ["Obese", "Hypertensive", "CurrentSmoker"]


def rename_columns(df):
    return df.rename(columns=RENAME)
