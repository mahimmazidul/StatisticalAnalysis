<p align="center">
  <img src="figures/banner.png" alt="Applied Statistical Analysis in Food Safety, Nutrition and Public Health" width="100%">
</p>

<h1 align="center">Applied Statistical Analysis in Food Safety, Nutrition and Public Health</h1>

<p align="center">
  <em>A reproducible classical biostatistics project built on real NHANES 2017&ndash;2018 survey data.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="python">
  <img src="https://img.shields.io/badge/statistics-classical-1f3a44" alt="classical statistics">
  <img src="https://img.shields.io/badge/reproducible-yes-2a9d8f" alt="reproducible">
  <img src="https://img.shields.io/badge/figures-300%20DPI-e9c46a" alt="figures">
  <img src="https://img.shields.io/badge/dataset-NHANES%202017--2018-457b9d" alt="dataset">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
</p>

> A full statistical analysis of one NHANES cycle, from cleaning to a written report. The aim is clear statistical thinking, honest reporting, and clean reproducible code, in the way a real nutrition or public health lab works with data.

---

## Table of Contents

1. [Overview](#overview)
2. [Research Questions](#research-questions)
3. [Dataset](#dataset)
4. [How the Analysis Flows](#how-the-analysis-flows)
5. [Quick Start](#quick-start)
6. [Figures](#figures)
7. [Statistical Methods](#statistical-methods)
8. [What We Found](#what-we-found)
9. [Limitations](#limitations)
10. [References](#references)
11. [FAQ](#faq)
12. [Credit](#credit)

---

## Overview

Diet, body weight, and blood pressure are central topics in nutrition science and public health. NHANES is the survey the U.S. Centers for Disease Control and Prevention (CDC) runs to track these things across the population. This project takes one NHANES cycle and works through a full analysis from start to finish.

What it does:

- downloads the real NHANES files from the CDC, with a built-in offline copy so the code always runs;
- cleans the data in small, readable scripts and explains every choice;
- runs descriptive, comparison, and regression analyses, and checks the assumptions before each test;
- produces 28 figures at 300 DPI (PNG and SVG) and 45 result tables (CSV and Markdown);
- writes a short report in [`report/report.md`](report/report.md) and [`report/report.pdf`](report/report.pdf) that explains each result in plain words.

The final sample is **5,175 adults aged 20 and older with a measured BMI**.

---

## Research Questions

| # | Question | Main method |
|---|----------|-------------|
| RQ1 | Does BMI differ between men and women? | Welch t test, Mann&ndash;Whitney U |
| RQ2 | Is higher energy intake linked to higher BMI? | Correlation, linear regression |
| RQ3 | Does smoking relate to body weight and diet? | ANOVA, Kruskal&ndash;Wallis, logistic regression |
| RQ4 | Are income and education linked to obesity? | Chi square, logistic regression |
| RQ5 | Does age predict higher blood pressure? | ANOVA, linear and logistic regression |
| RQ6 | What hidden patterns sit behind these variables? | Principal Component Analysis |

---

## Dataset

| Item | Detail |
|------|--------|
| Source | CDC, National Center for Health Statistics, **NHANES 2017&ndash;2018** |
| How it is fetched | [`src/download_data.py`](src/download_data.py), with [`src/make_offline_data.py`](src/make_offline_data.py) as a backup |
| Files combined | demographics, body measures, day one diet recall, smoking, blood pressure, alcohol, HDL cholesterol, fasting glucose |
| Linking key | `SEQN`, the participant id |
| Final sample | **5,175 adults and 28 analysis variables** |

NHANES is public and de-identified, so secondary analysis like this needs no ethics approval. The full data dictionary is in [`data/processed/data_dictionary.csv`](data/processed/data_dictionary.csv).

---

## How the Analysis Flows

```mermaid
flowchart TD
    A[CDC NHANES files] -->|download_data.py| B[data/raw]
    A2[Offline backup copy] -.->|make_offline_data.py| B
    B -->|load.py| C[Merge files on SEQN]
    C -->|clean.py| D[Keep adults and screen odd values]
    D -->|encode.py| E[Labelled, ready dataset]
    E -->|preprocess.py| F[data/processed]
    F --> G[Descriptive stats]
    F --> H[Missing data check]
    F --> I[Assumption checks]
    I --> J[Comparison tests]
    J --> K[Regression and diagnostics]
    F --> L[PCA]
    G --> M[figures and tables]
    H --> M
    J --> M
    K --> M
    L --> M
    M --> N[report.md and report.pdf]
```

---

## Quick Start

```bash
# 1. set up the environment
pip install -r requirements.txt

# 2. get the data (real download, with an automatic offline backup)
python -m src.download_data || python -m src.make_offline_data

# 3. build the cleaned dataset
python -m src.preprocess

# 4. run every table and figure in one go
python -m src.run_all
```

Or run everything at once with `make all`.

---

## Figures

Every figure is made by one script in [`src/plots/`](src/plots) and saved at 300 DPI as both PNG and SVG. Each one is explained in [`report/report.md`](report/report.md).

### Figure 1. How BMI is spread across adults
![Histogram of BMI](figures/histogram_bmi.png)

BMI leans to the right, with a long tail of higher values. The mean (29.9) sits above the median (28.6), the classic sign of a skewed variable. This is the main reason the project leans on Welch and rank based tests later on.
Code: [`src/plots/histogram_bmi.py`](src/plots/histogram_bmi.py)

### Figure 2. BMI by sex, and Figure 3. BMI by age group
<p align="center">
  <img src="figures/density_bmi.png" width="49%">
  <img src="figures/violin_bmi.png" width="49%">
</p>

The two sexes have very similar BMI curves. Across age, BMI rises into midlife and then eases a little in the oldest group.
Code: [`src/plots/density_bmi.py`](src/plots/density_bmi.py) and [`src/plots/violin_bmi.py`](src/plots/violin_bmi.py)

### Figure 4. Waist size against BMI
![Scatter of BMI vs waist](figures/scatter_bmi_waist.png)

Waist size and BMI move together almost perfectly (r = 0.90). They both measure body fat, so this is expected. It is also why the two are never used as separate predictors in the same model.
Code: [`src/plots/scatter_bmi_waist.py`](src/plots/scatter_bmi_waist.py)

### Figure 5. How the variables relate to each other
![Correlation heatmap](figures/correlation_heatmap.png)

The diet variables form one cluster, the body size variables form another, and age tracks blood pressure. HDL cholesterol moves in the opposite direction to body size.
Code: [`src/plots/correlation_heatmap.py`](src/plots/correlation_heatmap.py)

### Figure 6. The two main patterns behind the data (PCA biplot)
![PCA biplot](figures/pca_biplot.png)

The first two components explain about 54% of the variation. The first is a body size and blood pressure axis, and the second is a food intake axis. Weight categories line up neatly along the first axis.
Code: [`src/plots/pca_biplot.py`](src/plots/pca_biplot.py)

### Figure 7. What is linked to obesity (forest plot)
![Forest plot](figures/forest_plot.png)

After adjusting for the other variables, more dietary fiber and higher income both go with lower odds of obesity. Women have somewhat higher odds than men. Current smoking shows lower odds, a known pattern that is heavily confounded and should not be read as a benefit of smoking.
Code: [`src/plots/forest_plot.py`](src/plots/forest_plot.py)

### Figure 8. Checking the regression model
![Regression diagnostics](figures/residual_plot.png)

These four panels check the blood pressure model: residuals against fitted values, a normal Q-Q plot, a scale location plot, and a leverage plot. They are shown openly, including where the model is not perfect.
Code: [`src/plots/residual_plot.py`](src/plots/residual_plot.py)

<details>
<summary><strong>See the other 20 figures</strong></summary>

### Figure 9. Boxplot of BMI by sex
![Boxplot of BMI by sex](figures/boxplot_bmi.png)

The boxes show the middle half of the data. Both sexes sit in a similar range, with women slightly higher and a few high outliers on each side.
Code: [`src/plots/boxplot_bmi.py`](src/plots/boxplot_bmi.py)

### Figure 10. Cumulative distribution of BMI by sex (ECDF)
![ECDF of BMI by sex](figures/ecdf_bmi.png)

This curve reads off what share of people fall below any BMI value. The two lines almost overlap, which again shows how close the sexes are.
Code: [`src/plots/ecdf_bmi.py`](src/plots/ecdf_bmi.py)

### Figure 11. Q-Q plot of BMI
![Q-Q plot of BMI](figures/qqplot_bmi.png)

If BMI were a perfect bell curve the points would sit on the straight line. The upper tail bends away, confirming the right skew we saw in the histogram.
Code: [`src/plots/qqplot_bmi.py`](src/plots/qqplot_bmi.py)

### Figure 12. Ridgeline of BMI by age group
![Ridgeline of BMI by age](figures/ridgeline_bmi_age.png)

Each ridge is the BMI shape for one age band, stacked for easy comparison. The peak shifts to the right into midlife and then settles back a little.
Code: [`src/plots/ridgeline_bmi_age.py`](src/plots/ridgeline_bmi_age.py)

### Figure 13. Energy intake against BMI (hexbin)
![Energy vs BMI hexbin](figures/scatter_bmi_energy.png)

Darker cells hold more people. The cloud is flat, which matches the near-zero link between one day of energy intake and BMI.
Code: [`src/plots/scatter_bmi_energy.py`](src/plots/scatter_bmi_energy.py)

### Figure 14. HDL cholesterol across weight classes
![HDL across weight classes](figures/strip_rug_hdl.png)

HDL, the protective cholesterol, drops steadily as weight class rises. This is one of the clearer health signals in the data.
Code: [`src/plots/strip_rug_hdl.py`](src/plots/strip_rug_hdl.py)

### Figure 15. How common each weight class is
![BMI category prevalence](figures/bar_bmicategory.png)

Most adults fall in the overweight or obese groups, which lines up with national patterns.
Code: [`src/plots/bar_bmicategory.py`](src/plots/bar_bmicategory.py)

### Figure 16. Obesity by age group and sex
![Obesity by age and sex](figures/grouped_bar_obesity.png)

Obesity is common across all adult ages, with women a little higher than men in most bands.
Code: [`src/plots/grouped_bar_obesity.py`](src/plots/grouped_bar_obesity.py)

### Figure 17. Weight class by smoking status
![Weight class by smoking status](figures/stacked_bar_smoking_bmi.png)

Each bar splits one smoking group into its weight classes. Current smokers carry a slightly smaller obese share, the same pattern the forest plot picks up.
Code: [`src/plots/stacked_bar_smoking_bmi.py`](src/plots/stacked_bar_smoking_bmi.py)

### Figure 18. Sex by weight class (mosaic)
![Mosaic of sex by weight class](figures/mosaic_sex_bmicategory.png)

Box width shows group size and box height shows the weight-class split, so you can read both at once.
Code: [`src/plots/mosaic_sex_bmicategory.py`](src/plots/mosaic_sex_bmicategory.py)

### Figure 19. Clustered correlation heatmap
![Clustered correlation heatmap](figures/correlation_clustered.png)

The same correlations as before, but reordered so related variables sit together. The diet block and the body-size block stand out clearly.
Code: [`src/plots/correlation_clustered.py`](src/plots/correlation_clustered.py)

### Figure 20. Pairwise relationships among diet and body measures
![Pairwise relationships](figures/pairplot_diet.png)

A grid of scatter plots and density curves. The nutrient variables rise together, while BMI stays fairly flat against them.
Code: [`src/plots/pairplot_diet.py`](src/plots/pairplot_diet.py)

### Figure 21. Scree plot for PCA
![PCA scree plot](figures/pca_scree.png)

The bars show how much each component explains, and the line shows the running total. The drop after the first two components is why we keep two.
Code: [`src/plots/pca_scree.py`](src/plots/pca_scree.py)

### Figure 22. PCA loadings
![PCA loadings](figures/pca_loadings.png)

This shows how strongly each variable feeds into each component. It is what lets us name the first axis "body size" and the second "food intake".
Code: [`src/plots/pca_loadings.py`](src/plots/pca_loadings.py)

### Figure 23. Standardised predictors of BMI
![Standardised predictors of BMI](figures/coefficient_plot_linear.png)

With all predictors put on the same scale, the bars show which ones move BMI most in the linear model, with their confidence intervals.
Code: [`src/plots/coefficient_plot_linear.py`](src/plots/coefficient_plot_linear.py)

### Figure 24. Predicted blood pressure by age
![Predicted blood pressure by age](figures/prediction_plot.png)

The model's predicted systolic blood pressure rises with age for both sexes, with the shaded band showing the uncertainty.
Code: [`src/plots/prediction_plot.py`](src/plots/prediction_plot.py)

### Figure 25. Mean blood pressure by age and sex
![Mean blood pressure by age and sex](figures/means_plot_sbp_age.png)

The raw group means tell the same story as the model: blood pressure climbs steadily with age.
Code: [`src/plots/means_plot_sbp_age.py`](src/plots/means_plot_sbp_age.py)

### Figure 26. Missing value matrix
![Missing value matrix](figures/missing_matrix.png)

White streaks mark missing entries. Fasting glucose is mostly missing by design, while diet, blood pressure, and income have moderate gaps.
Code: [`src/plots/missingness.py`](src/plots/missingness.py)

### Figure 27. Observed counts per variable
![Observed counts per variable](figures/missing_bar.png)

A simple bar count of how many real values each variable has, which is the quick way to spot the gaps.
Code: [`src/plots/missingness.py`](src/plots/missingness.py)

### Figure 28. Missingness correlation
![Missingness correlation](figures/missing_heatmap.png)

This checks whether variables tend to go missing together. The lack of strong structure supports the simple complete-case approach.
Code: [`src/plots/missingness.py`](src/plots/missingness.py)

</details>

---

## Statistical Methods

Every test is run after the assumptions are checked, and every result comes with an effect size and a confidence interval. Full notes for each table are in [`tables/README.md`](tables/README.md).

| Family | What is included | Script |
|--------|------------------|--------|
| Descriptive | mean, median, mode, SD, variance, CV, range, IQR, quartiles, percentiles, skewness, kurtosis, frequency and cross tables | [`descriptive_statistics.py`](src/analysis/descriptive_statistics.py) |
| Normality | Shapiro&ndash;Wilk, Kolmogorov&ndash;Smirnov, Anderson&ndash;Darling | [`normality_tests.py`](src/analysis/normality_tests.py) |
| Equal variance | Levene, Bartlett | [`variance_tests.py`](src/analysis/variance_tests.py) |
| Two groups | Student t, Welch t, Mann&ndash;Whitney U, with Hedges g | [`group_tests_two.py`](src/analysis/group_tests_two.py) |
| Several groups | one way ANOVA with Tukey, two way ANOVA, Kruskal&ndash;Wallis | [`anova.py`](src/analysis/anova.py) |
| Categories | chi square, Fisher exact, Cram&eacute;r's V | [`categorical_tests.py`](src/analysis/categorical_tests.py) |
| Association | Pearson, Spearman, Kendall, partial correlation | [`correlation.py`](src/analysis/correlation.py) |
| Regression | simple and multiple linear, logistic with odds ratios | [`linear_regression.py`](src/analysis/linear_regression.py), [`logistic_regression.py`](src/analysis/logistic_regression.py) |
| Diagnostics | residual normality, Breusch&ndash;Pagan, Durbin&ndash;Watson, Cook's distance, leverage, VIF | [`regression_diagnostics.py`](src/analysis/regression_diagnostics.py) |
| Patterns | PCA on the correlation matrix | [`pca.py`](src/analysis/pca.py) |

---

## What We Found

- **Sex and BMI.** Women had slightly higher BMI than men (30.3 vs 29.4). The difference was real in the statistical sense (p < 0.001) but very small in practice (Hedges g = 0.12). With a sample this large, even tiny differences turn significant, which is why effect sizes matter.
- **Energy and BMI.** A single day of diet recall showed no link with BMI (r = 0.01). This is expected, since one day of food intake is a noisy snapshot and people with high BMI may already be eating less.
- **Smoking.** BMI differed across smoking groups, and current smokers had lower odds of obesity in the adjusted model. This is a known and heavily confounded pattern, not a health benefit of smoking.
- **Income and education.** Both were linked to obesity. Higher income went with lower odds of obesity even after adjustment.
- **Age and blood pressure.** This was the strongest signal in the project. Blood pressure climbed sharply with age, and the link between age and high blood pressure was the largest categorical effect we saw.
- **Hidden patterns.** PCA found two clear and separate stories: how much body fat a person carries, and how much they eat.

---

## Limitations

- **Survey weights are not used.** NHANES is built from a complex sample design. This project runs an unweighted analysis to keep it clear, so the numbers describe this sample rather than the whole country. This is the most important thing to keep in mind.
- The data is **cross sectional**, so nothing here proves cause and effect.
- Diet rests on a **single 24 hour recall**, a noisy measure of normal eating.
- Smoking and income are **self reported**.

---

## References

The full list is in [`references/references.md`](references/references.md). Key sources: CDC NHANES 2017&ndash;2018; WHO (2000); Cohen (1988); Whitlock and Schluter (2020); Seabold and Perktold (2010).

---

## FAQ

<details>
<summary><strong>Will it run without internet?</strong></summary>

Yes. The pipeline first tries the live CDC download. If a file cannot be reached, it quietly builds a fixed offline copy and carries on, so the whole thing still runs.
</details>

<details>
<summary><strong>Why are some significant results called small?</strong></summary>

With about 5,000 people, tiny differences become statistically significant. Reporting effect sizes next to p values tells you whether a result actually matters, not just whether it is detectable.
</details>

---

## Credit

<p align="center">
  Made by <strong>Mazidul Islam Mahim</strong>.<br>
  With the help of an AI.
</p>
