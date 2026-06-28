import pandas as pd

from src.data_cleaning.clean import clean
from src.data_cleaning.encode import encode
from src.data_cleaning.load import load_merged
from src.data_cleaning.rename import CONTINUOUS, rename_columns
from src.data_cleaning.transform import add_log_transforms
from src.utils.paths import CLEAN_FILE, DATA_PROCESSED, PROCESSED_FILE, ensure_dirs

ANALYTIC_COLUMNS = [
    "SEQN", "Sex", "Age", "AgeGroup", "RaceEthnicity", "Education",
    "IncomePovertyRatio", "IncomeGroup", "SmokingStatus", "CurrentSmoker",
    "BMI", "BMICategory", "Obese", "Weight", "Height", "WaistCircumference",
    "EnergyKcal", "ProteinG", "CarbohydrateG", "SugarG", "TotalFatG",
    "FiberG", "SodiumMg", "SystolicBP", "DiastolicBP", "Hypertensive",
    "HDL", "FastingGlucose",
]


def build():
    ensure_dirs()
    raw = load_merged()
    cleaned = clean(raw)
    renamed = rename_columns(cleaned)
    encoded = encode(renamed)
    analytic = encoded[[c for c in ANALYTIC_COLUMNS if c in encoded.columns]].copy()
    analytic.to_csv(PROCESSED_FILE, index=False)

    transformed = add_log_transforms(analytic)
    transformed.to_csv(CLEAN_FILE, index=False)
    return analytic, transformed


def data_dictionary():
    rows = [
        ("SEQN", "Respondent sequence number", "Identifier", "-"),
        ("Sex", "Biological sex", "Categorical", "Male / Female"),
        ("Age", "Age in years at screening", "Continuous", "20-80"),
        ("AgeGroup", "Age band", "Ordinal", "20-39 / 40-59 / 60-79 / 80+"),
        ("RaceEthnicity", "Race and Hispanic origin", "Categorical", "6 levels"),
        ("Education", "Highest education (adults)", "Ordinal", "5 levels"),
        ("IncomePovertyRatio", "Family income to poverty ratio", "Continuous", "0-5"),
        ("IncomeGroup", "Income-poverty band", "Ordinal", "3 levels"),
        ("SmokingStatus", "Derived smoking status", "Ordinal", "Never / Former / Current"),
        ("CurrentSmoker", "Current smoker flag", "Binary", "0 / 1"),
        ("BMI", "Body mass index", "Continuous", "kg/m^2"),
        ("BMICategory", "WHO BMI class", "Ordinal", "4 levels"),
        ("Obese", "BMI >= 30 flag", "Binary", "0 / 1"),
        ("Weight", "Body weight", "Continuous", "kg"),
        ("Height", "Standing height", "Continuous", "cm"),
        ("WaistCircumference", "Waist circumference", "Continuous", "cm"),
        ("EnergyKcal", "Day-1 energy intake", "Continuous", "kcal"),
        ("ProteinG", "Day-1 protein", "Continuous", "g"),
        ("CarbohydrateG", "Day-1 carbohydrate", "Continuous", "g"),
        ("SugarG", "Day-1 total sugars", "Continuous", "g"),
        ("TotalFatG", "Day-1 total fat", "Continuous", "g"),
        ("FiberG", "Day-1 dietary fiber", "Continuous", "g"),
        ("SodiumMg", "Day-1 sodium", "Continuous", "mg"),
        ("SystolicBP", "Systolic blood pressure", "Continuous", "mmHg"),
        ("DiastolicBP", "Diastolic blood pressure", "Continuous", "mmHg"),
        ("Hypertensive", "BP >= 130/80 flag", "Binary", "0 / 1"),
        ("HDL", "HDL cholesterol", "Continuous", "mg/dL"),
        ("FastingGlucose", "Fasting plasma glucose", "Continuous", "mg/dL"),
    ]
    return pd.DataFrame(rows, columns=["Variable", "Description", "Type", "Units/Levels"])


def main():
    analytic, _ = build()
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    dd = data_dictionary()
    dd.to_csv(DATA_PROCESSED / "data_dictionary.csv", index=False)
    print(f"Analytic dataset: {analytic.shape[0]} adults x {analytic.shape[1]} variables")
    print(f"Continuous variables: {len([c for c in CONTINUOUS if c in analytic.columns])}")
    print(f"Saved: {PROCESSED_FILE.name}, {CLEAN_FILE.name}, data_dictionary.csv")


if __name__ == "__main__":
    main()
