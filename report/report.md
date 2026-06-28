# Applied Statistical Analysis in Food Safety, Nutrition and Public Health

### A classical biostatistical analysis of the NHANES 2017&ndash;2018 cycle

---

## Abstract

**Background.** Obesity, dietary intake, and cardiometabolic risk are central concerns of nutrition science and public health. The National Health and Nutrition Examination Survey (NHANES) is the principal surveillance instrument for these factors in the United States.

**Objective.** To characterise the distribution and determinants of body mass index (BMI), blood pressure, and obesity in U.S. adults using a fully reproducible, assumption-driven classical statistical pipeline, deliberately excluding machine learning.

**Methods.** Eight NHANES 2017&ndash;2018 data domains were merged on the respondent identifier and restricted to 5,175 adults (&ge; 20 years) with a measured BMI. After plausibility screening, encoding, and missing-data assessment, we computed descriptive statistics, checked distributional and variance assumptions, and applied two-group tests (Student/Welch *t*, Mann&ndash;Whitney U), analysis of variance with Tukey HSD, Kruskal&ndash;Wallis tests, chi-square and Fisher's exact tests, Pearson/Spearman/partial correlations, multiple linear regression, and multivariable logistic regression with full diagnostics. Principal component analysis summarised multivariate structure. All inferences were accompanied by effect sizes and 95% confidence intervals.

**Results.** BMI was strongly right-skewed (skewness +1.27; mean 29.9, median 28.6 kg/m&sup2;). Women had marginally higher BMI than men (mean difference &minus;0.91 kg/m&sup2;; Welch *t* = &minus;4.45, *p* < 0.001) but with a negligible effect size (Hedges *g* = &minus;0.12). Energy intake from a single 24-hour recall was not associated with BMI (*r* = 0.01, *p* = 0.55). Systolic blood pressure increased markedly with age (correlation *r* = 0.47; ANOVA &eta;&sup2; = 0.20), and the age&ndash;hypertension association was the strongest categorical effect observed (Cram&eacute;r's V = 0.34). In adjusted logistic regression, dietary fiber (OR 0.97 per gram, 95% CI 0.96&ndash;0.98) and higher income-to-poverty ratio (OR 0.94, 0.91&ndash;0.98) were independently protective against obesity. Two principal components &mdash; an adiposity/blood-pressure axis and a dietary-intake axis &mdash; explained 54.3% of standardised variance.

**Conclusions.** Classical biostatistics, applied transparently and with assumptions verified, yields interpretable and clinically coherent conclusions. Reporting effect sizes alongside *p*-values is essential in large surveys where trivial differences attain significance.

---

## 1. Introduction

Excess adiposity is a leading modifiable risk factor for cardiovascular disease, type 2 diabetes, and several cancers, and it interacts with diet quality, socioeconomic position, and behaviour. Public-health surveillance relies on nationally representative surveys such as NHANES to monitor these factors and to generate hypotheses for laboratory and clinical follow-up. The analytical demands of such surveillance are squarely classical: investigators must compare groups, quantify associations, adjust for confounders, and communicate uncertainty honestly.

This report applies that classical toolkit to the 2017&ndash;2018 NHANES cycle. The work is intentionally free of machine learning; the value on display is statistical reasoning &mdash; choosing the right test for the data, verifying its assumptions, quantifying the magnitude of effects, and interpreting results in scientific rather than purely numerical terms.

---

## 2. Research Questions

1. **RQ1.** Does BMI differ between males and females?
2. **RQ2.** Is higher energy intake associated with BMI?
3. **RQ3.** Do smoking habits influence body composition and dietary quality?
4. **RQ4.** Are socioeconomic variables (income, education) associated with obesity?
5. **RQ5.** Does age predict elevated blood pressure and hypertension prevalence?
6. **RQ6.** What latent dimensions summarise anthropometric, dietary, and clinical variation?

---

## 3. Methods

### 3.1 Dataset

Data are from NHANES 2017&ndash;2018 (cycle J), CDC/NCHS. Eight public-use domains &mdash; Demographics (DEMO_J), Body Measures (BMX_J), Dietary Day-1 Totals (DR1TOT_J), Smoking (SMQ_J), Blood Pressure (BPX_J), Alcohol (ALQ_J), HDL cholesterol (HDL_J), and Fasting Glucose (GLU_J) &mdash; were downloaded as SAS transport files and merged on the respondent sequence number `SEQN`.

### 3.2 Data cleaning

The analytic population was restricted to adults aged &ge; 20 years with a measured BMI, yielding **5,175 participants**. Biologically implausible values were screened to missing using pre-registered physiological bounds (e.g. BMI 10&ndash;90 kg/m&sup2;, systolic BP 70&ndash;240 mmHg). NHANES "refused"/"don't know" codes were recoded to missing. Derived variables included WHO BMI categories, age and income bands, a three-level smoking-status variable, and binary indicators for obesity (BMI &ge; 30), hypertension (&ge; 130/80 mmHg), and current smoking. Each step is implemented as a discrete module under `src/data_cleaning/` and documented in `workflow/WORKFLOW.md`.

### 3.3 Missing data

Missingness was quantified per variable and visualised with a missing-value matrix, observed-count bar chart, and a missingness-correlation heatmap (`figures/missing_matrix.png`, `missing_bar.png`, `missing_heatmap.png`). Fasting glucose was missing for the majority of participants by design (fasting subsample), and dietary, blood-pressure, income, and HDL variables had moderate missingness. Primary analyses used complete-case (pairwise) deletion, valid under MCAR; median imputation and multiple imputation are provided/planned as sensitivity analyses.

### 3.4 Statistical analysis

Distributional assumptions were tested with Shapiro&ndash;Wilk, Kolmogorov&ndash;Smirnov, and Anderson&ndash;Darling tests; variance homogeneity with Levene and Bartlett tests. Test selection followed an explicit decision rule: Welch's *t*-test when variances were unequal, Mann&ndash;Whitney U when normality failed, one-way ANOVA with Tukey HSD (or Kruskal&ndash;Wallis) for multi-group comparisons, and chi-square (or Fisher's exact) tests for categorical associations. Associations between continuous variables used Pearson and Spearman coefficients with Fisher z confidence intervals, plus partial correlations adjusting for age. Multiple linear regression modelled continuous outcomes; multivariable logistic regression modelled binary outcomes, reporting adjusted odds ratios. Regression diagnostics covered residual normality, homoscedasticity (Breusch&ndash;Pagan), independence (Durbin&ndash;Watson), influence (Cook's distance, leverage), and multicollinearity (variance inflation factors). Principal component analysis was performed on the standardised correlation matrix. Effect sizes (Hedges *g*, &eta;&sup2;, &epsilon;&sup2;, Cram&eacute;r's V) accompanied every test. Analyses used Python 3 with NumPy, pandas, SciPy, statsmodels, Matplotlib, and seaborn.

---

## 4. Results

### 4.1 Descriptive statistics

Among 5,175 adults, mean BMI was 29.9 kg/m&sup2; (SD 7.4), mean age 51.2 years, and mean systolic blood pressure 126.5 mmHg. Most continuous variables were right-skewed; BMI (skewness +1.27), dietary sugar (+1.80), and fasting glucose (+3.73) were the most asymmetric. Full descriptive tables are in `tables/descriptive_continuous.csv`. The obese class accounted for 42% of adults and 47.7% met the 130/80 hypertension threshold.

*Interpretation.* The pronounced right skew of metabolic variables is itself a finding: it reflects a subpopulation with markedly elevated adiposity and glucose, and it dictates the downstream preference for robust and rank-based methods. **Assumptions:** none required for description. **References:** WHO BMI classification; Whitlock & Schluter (2020).

### 4.2 Normality and variance assumptions

Every continuous variable rejected normality (all Shapiro&ndash;Wilk *p* < 0.001; `tables/normality_tests.csv`), and variances were heterogeneous across all grouping factors examined (Levene *p* < 0.05; `tables/variance_homogeneity_tests.csv`). These results are unsurprising at this sample size and motivated the use of Welch's *t*-test and nonparametric confirmation throughout.

*Interpretation.* At n &gt; 5,000, formal normality tests are extremely sensitive and almost always significant; we therefore also inspected Q-Q plots (`figures/qqplot_bmi.png`) and skewness, and relied on the central limit theorem for mean-based inference while corroborating with rank tests. **Assumptions tested:** normality, homoscedasticity. **References:** Shapiro & Wilk (1965); Levene (1960).

### 4.3 RQ1 &mdash; Sex differences in BMI

Women had higher mean BMI than men (30.3 vs 29.4 kg/m&sup2;; mean difference &minus;0.91, 95% CI &minus;1.31 to &minus;0.50). Because variances differed (Levene *p* < 0.001), Welch's *t*-test was used: *t* = &minus;4.45, *p* < 0.001, confirmed by Mann&ndash;Whitney U (*p* = 0.019). The standardised effect was, however, **negligible** (Hedges *g* = &minus;0.12). Larger sex differences were seen for HDL cholesterol (women +9.6 mg/dL; *g* = &minus;0.66, medium) and energy intake (men +593 kcal; *g* = +0.63, medium). See `tables/two_group_tests.csv` and Figures `boxplot_bmi.png`, `density_bmi.png`.

*Interpretation.* The statistically significant but practically negligible BMI difference is a textbook demonstration of why effect sizes must accompany *p*-values in large surveys. The substantial sex difference in HDL is biologically expected and clinically meaningful. **Assumptions tested:** normality (failed &rarr; Welch + Mann&ndash;Whitney), variance homogeneity. **References:** Cohen (1988); Hedges (1981).

### 4.4 RQ2 &mdash; Energy intake and BMI

Single-day energy intake was not linearly associated with BMI (Pearson *r* = 0.01, 95% CI &minus;0.02 to 0.04, *p* = 0.55; Spearman *&rho;* = 0.02). In contrast, waist circumference and BMI were very strongly correlated (*r* = 0.90; Figure `scatter_bmi_waist.png`), and energy correlated strongly with protein (*r* = 0.77) and sodium (*r* = 0.79). See `tables/correlation_pairwise.csv`.

*Interpretation.* The null energy&ndash;BMI association is expected and instructive: a single 24-hour recall is a noisy estimate of habitual intake, and cross-sectional reverse causation (dieting among those with high BMI) further attenuates the relationship. This is a measurement-and-design limitation, not evidence that intake is irrelevant. **Assumptions:** linearity and bivariate spread inspected via hexbin (`scatter_bmi_energy.png`). **References:** Whitlock & Schluter (2020).

### 4.5 RQ3 &mdash; Smoking, body composition, and diet

BMI differed across smoking status (one-way ANOVA *F*(2, 5172) = 16.7, *p* < 0.001; &eta;&sup2; = 0.006; Kruskal&ndash;Wallis corroborated). In the adjusted logistic model, current smoking was associated with **lower** obesity odds (OR 0.67, 95% CI 0.56&ndash;0.80). See `tables/anova_oneway.csv` and `tables/logit_obesity.csv`.

*Interpretation.* The inverse smoking&ndash;obesity association is well documented and reflects appetite-suppressant and metabolic effects of nicotine, but it is heavily confounded by socioeconomic and behavioural factors and must not be read causally or as a health benefit of smoking. **Assumptions tested:** ANOVA homogeneity (failed &rarr; Kruskal&ndash;Wallis confirmation). **References:** Cohen (1988).

### 4.6 RQ4 &mdash; Socioeconomic status and obesity

Obesity prevalence was associated with both education (&chi;&sup2;(4) = 71.3, *p* < 0.001; Cram&eacute;r's V = 0.12) and income group (&chi;&sup2;(2) = 13.9, *p* < 0.001; V = 0.06). In the adjusted model, each unit increase in the income-to-poverty ratio reduced obesity odds (OR 0.94, 95% CI 0.91&ndash;0.98). See `tables/categorical_tests.csv` and the forest plot (`figures/forest_plot.png`).

*Interpretation.* A consistent socioeconomic gradient in obesity emerges across unadjusted categorical tests and the adjusted multivariable model, aligning with the established literature on the social patterning of diet-related disease. The effect sizes are small but robust. **Assumptions tested:** expected cell counts &ge; 5 (Fisher's exact used otherwise). **References:** Cram&eacute;r (1946); WHO (2000).

### 4.7 RQ5 &mdash; Age, blood pressure, and hypertension

Systolic blood pressure increased steeply across age groups (ANOVA *F*(3, 4596) = 393.8, *p* < 0.001; &eta;&sup2; = 0.20), and age correlated with systolic BP at *r* = 0.47. The age&ndash;hypertension contingency was the strongest categorical association in the study (&chi;&sup2;(3) = 521.3, *p* < 0.001; Cram&eacute;r's V = 0.34, large). In multiple linear regression, age, BMI, sex, and sodium jointly explained 23.5% of systolic BP variance (adjusted R&sup2; = 0.234); age contributed the dominant standardised coefficient. See `tables/linreg_systolic.csv`, `tables/linreg_model_fit.csv`, Figures `means_plot_sbp_age.png`, `prediction_plot.png`.

*Interpretation.* The age&ndash;blood-pressure relationship is the most substantial effect in the analysis and is physiologically expected (arterial stiffening with age). The regression model is useful for description and adjustment, though its residuals were non-normal and heteroscedastic (see 4.9), so inference relies on the large-sample robustness of OLS and is corroborated by the consistent ANOVA and correlation results. **Assumptions tested:** linearity, normality of residuals, homoscedasticity, multicollinearity. **References:** Whelton et al. (2018).

### 4.8 RQ6 &mdash; Principal component analysis

PCA on eleven standardised anthropometric, dietary, and clinical variables yielded two dominant components explaining 54.3% of variance (PC1 28.6%, PC2 25.7%; `tables/pca_explained_variance.csv`). PC1 loaded positively on BMI, waist, weight, and blood pressure and negatively on HDL &mdash; an **adiposity/cardiometabolic axis**; PC2 loaded on energy, protein, sodium, and fiber &mdash; a **dietary-intake axis** (`tables/pca_loadings.csv`, Figures `pca_scree.png`, `pca_biplot.png`, `pca_loadings.png`). BMI categories separated cleanly along PC1.

*Interpretation.* PCA confirms that the measured variables collapse into two interpretable, largely independent dimensions: how much body fat a person carries and how much they eat. This is descriptive ordination only &mdash; no clustering or supervised learning is involved. **Assumptions:** linear correlation structure; standardisation applied. **References:** Jolliffe (2002).

### 4.9 Regression diagnostics

Across all three regression models, residuals departed from normality (Shapiro *p* < 0.001) and showed heteroscedasticity (Breusch&ndash;Pagan *p* < 0.001), while independence was acceptable (Durbin&ndash;Watson &asymp; 2.0). A modest number of high-influence points was flagged by Cook's distance (e.g. 219 of 4,215 in the systolic-BP model), none individually decisive. Variance inflation factors were all below 3, indicating **no problematic multicollinearity** among the chosen predictors (notably, BMI and waist circumference were never entered together). See `tables/regression_diagnostics.csv`, `tables/linreg_vif.csv`, and Figure `residual_plot.png`.

*Interpretation.* The diagnostic failures (non-normal, heteroscedastic residuals) are typical for skewed biological outcomes in large samples; they are reported honestly rather than hidden. With n &gt; 4,000, coefficient estimates remain consistent, but heteroscedasticity-robust standard errors or a transformed/quantile-regression outcome would be appropriate refinements (see Future Work). **References:** Breusch & Pagan (1979); Cook (1977).

---

## 5. Discussion

This analysis reproduces several well-established public-health patterns &mdash; the social gradient in obesity, the steep age&ndash;blood-pressure relationship, the sex difference in HDL &mdash; using only transparent classical methods. Two themes recur. First, **statistical significance is not practical significance**: at this sample size, even a 0.9 kg/m&sup2; BMI difference between sexes is "highly significant" yet negligible by Cohen's benchmarks, and only effect sizes reveal this. Second, **design and measurement shape conclusions**: the null energy&ndash;BMI association is a predictable artefact of single-day recall and cross-sectional reverse causation rather than evidence of biological irrelevance.

The work is positioned as the supplementary statistical material of a manuscript: every figure is reproducible from a single script, every table is interpreted, and every assumption is checked before the corresponding test is used. For a food-microbiology, food-safety, nutrition, or public-health laboratory, these are precisely the competencies required to turn data into defensible scientific claims.

---

## 6. Limitations

NHANES employs a complex, stratified, multistage probability sample; this analysis is **unweighted** for didactic clarity, so the point estimates here are sample-specific rather than nationally representative. The design is cross-sectional, precluding causal inference. Dietary intake rests on a single 24-hour recall with substantial within-person variability. Smoking and income are self-reported. Several outcomes had non-normal, heteroscedastic regression residuals. These caveats are stated explicitly and motivate the planned extensions.

---

## 7. Conclusion

A disciplined classical-statistics workflow &mdash; assumption checks first, the right test second, effect sizes and confidence intervals always &mdash; produces clear, honest, and clinically coherent conclusions from NHANES. The repository demonstrates statistical rigour, reproducibility, and scientific communication suitable for participation in research on food safety, nutrition, microbiology, and public health.

---

## 8. References

Full bibliography in `references/references.md`. Principal sources: CDC/NCHS NHANES 2017&ndash;2018; WHO (2000); Whelton et al. (2018); Cohen (1988); Hedges (1981); Shapiro & Wilk (1965); Levene (1960); Mann & Whitney (1947); Kruskal & Wallis (1952); Cram&eacute;r (1946); Breusch & Pagan (1979); Cook (1977); Jolliffe (2002); Whitlock & Schluter (2020); Seabold & Perktold (2010).
