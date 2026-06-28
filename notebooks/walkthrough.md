# Narrative Walkthrough

This notebook-style walkthrough explains how to reproduce the analysis interactively and how to read the outputs. It mirrors `src/run_all.py` step by step. (Provided as Markdown so it renders without a Jupyter kernel; copy each block into a cell to run live.)

## 0. Setup

```python
import pandas as pd
from src.utils.io import load_analytic
df = load_analytic()
df.shape
```

The analytic dataset has 5,175 adults and 28 variables.

## 1. Build the data (only needed once)

```python
from src import download_data, make_offline_data, preprocess
ok, fail = download_data.download()
if fail:
    make_offline_data.main()
preprocess.main()
```

## 2. Descriptive statistics

```python
from src.analysis.descriptive_statistics import describe_continuous
from src.data_cleaning.rename import CONTINUOUS
describe_continuous(df, [c for c in CONTINUOUS if c in df.columns]).head()
```

Read the skewness column: BMI (+1.27), sugar (+1.80) and glucose (+3.73) are strongly right-skewed, which justifies robust tests later.

## 3. Check assumptions before testing

```python
from src.analysis.normality_tests import normality_report
normality_report(df, ["BMI", "EnergyKcal", "SystolicBP"])
```

All variables reject normality at this sample size; we therefore prefer Welch and rank-based tests and inspect Q-Q plots rather than trusting a single *p*-value.

## 4. Answer RQ1 (sex difference in BMI)

```python
from src.analysis.group_tests_two import two_group_test
two_group_test(df, "BMI", "Sex", "Male", "Female")
```

The difference is significant (*p* < 0.001) but the effect size is negligible (Hedges *g* = -0.12) - a key lesson in distinguishing statistical from practical significance.

## 5. Multivariable models

```python
import statsmodels.formula.api as smf
d = df.copy()
d["SexFemale"] = (d["Sex"] == "Female").astype(int)
d["CurrentSmokerN"] = d["CurrentSmoker"].astype(float)
model = smf.logit("Obese ~ Age + SexFemale + EnergyKcal + FiberG + IncomePovertyRatio + CurrentSmokerN",
                  data=d.assign(Obese=d["Obese"].astype(float))).fit(disp=False)
import numpy as np
np.exp(model.params)
```

Fiber and income are independently protective against obesity.

## 6. Reproduce everything

```python
from src import run_all
run_all.main()
```

This regenerates all 45 tables and 28 figures, then you can render the report:

```python
from src import build_report
build_report.main()
```
