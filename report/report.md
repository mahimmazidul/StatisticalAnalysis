# Applied Statistical Analysis in Food Safety, Nutrition and Public Health

### A classical biostatistical analysis of the NHANES 2017&ndash;2018 cycle

---

## Abstract

**Background.** Obesity, diet, and blood pressure are central concerns of nutrition science and public health. The National Health and Nutrition Examination Survey (NHANES) is the main survey used to track these factors in the United States.

**Objective.** To describe the spread and drivers of body mass index (BMI), blood pressure, and obesity in U.S. adults using a clear, reproducible set of classical statistical methods.

**Methods.** Eight NHANES 2017&ndash;2018 data files were merged on the participant id and limited to 5,175 adults aged 20 and older with a measured BMI. After screening odd values, encoding, and a missing data check, we computed descriptive statistics, tested the assumptions of normality and equal variance, and then applied two group tests (Student and Welch t, Mann&ndash;Whitney U), analysis of variance with Tukey follow up, Kruskal&ndash;Wallis tests, chi square and Fisher tests, Pearson, Spearman, and partial correlations, multiple linear regression, and multivariable logistic regression with full diagnostics. Principal component analysis summarised the multivariable structure. Every result is reported with an effect size and a 95% confidence interval.

**Results.** BMI was strongly skewed to the right (skewness +1.27; mean 29.9, median 28.6 kg/m&sup2;). Women had slightly higher BMI than men (mean difference &minus;0.91 kg/m&sup2;; Welch t = &minus;4.45, p < 0.001), but the effect was tiny (Hedges g = &minus;0.12). Energy intake from one day of recall showed no link with BMI (r = 0.01, p = 0.55). Systolic blood pressure rose sharply with age (correlation r = 0.47; ANOVA eta squared = 0.20), and the link between age and high blood pressure was the strongest categorical effect seen (Cram&eacute;r's V = 0.34). In the adjusted logistic model, dietary fiber (OR 0.97 per gram, 95% CI 0.96&ndash;0.98) and higher income (OR 0.94, 0.91&ndash;0.98) were both linked to lower odds of obesity. Two components, one for body size and blood pressure and one for food intake, explained 54.3% of the variation.

**Conclusions.** Clear classical statistics, applied openly and with the assumptions checked, give readable and sensible results. Reporting effect sizes alongside p values matters in large surveys, where tiny differences still reach significance.

---

## 1. Introduction

Carrying too much body fat is a leading and changeable risk factor for heart disease, type 2 diabetes, and several cancers, and it interacts with diet, income, and behaviour. Public health work leans on national surveys such as NHANES to watch these factors and to raise questions for lab and clinical follow up. The statistics this needs are squarely classical: researchers compare groups, measure how strong a link is, adjust for other factors, and report uncertainty honestly.

This report applies that classical toolkit to the 2017&ndash;2018 NHANES cycle. The value on display is statistical reasoning: choosing the right test for the data, checking its assumptions, measuring how large each effect is, and reading the results in plain scientific terms rather than as bare numbers.

---

## 2. Research Questions

1. **RQ1.** Does BMI differ between men and women?
2. **RQ2.** Is higher energy intake linked to higher BMI?
3. **RQ3.** Does smoking relate to body weight and diet?
4. **RQ4.** Are income and education linked to obesity?
5. **RQ5.** Does age predict higher blood pressure?
6. **RQ6.** What hidden patterns sit behind the body, diet, and clinical variables?

---

## 3. Methods

### 3.1 Dataset

The data come from NHANES 2017&ndash;2018, run by the CDC. Eight public files (demographics, body measures, day one diet recall, smoking, blood pressure, alcohol, HDL cholesterol, and fasting glucose) were downloaded and merged on the participant id `SEQN`.

### 3.2 Data cleaning

We kept adults aged 20 and older who had a measured BMI, leaving **5,175 people**. Values outside a sensible physical range (for example BMI below 10 or above 90, or systolic blood pressure below 70 or above 240) were set to missing. The survey codes for "refused" and "don't know" were also set to missing. We then built grouped variables: WHO weight classes, age and income bands, a three level smoking variable, and flags for obesity (BMI of 30 or more), high blood pressure (130/80 or more), and current smoking. Each step lives in its own small script under `src/data_cleaning/`, with the reasoning written up in `workflow/WORKFLOW.md`.

### 3.3 Missing data

We measured how much was missing for each variable and drew it three ways: a missing value matrix, a bar chart of real counts, and a heatmap of whether variables go missing together (`figures/missing_matrix.png`, `missing_bar.png`, `missing_heatmap.png`). Fasting glucose was missing for most people by design, since only a subsample fasted, while diet, blood pressure, income, and HDL had moderate gaps. The main analyses use complete cases for each test, which is fair when data are missing at random. Median imputation is offered as a simple alternative, and multiple imputation is listed as future work.

### 3.4 Statistical analysis

We tested normality with the Shapiro&ndash;Wilk, Kolmogorov&ndash;Smirnov, and Anderson&ndash;Darling tests, and equal variance with the Levene and Bartlett tests. The choice of test then followed a clear rule: Welch's t test when variances differed, the Mann&ndash;Whitney U test when normality failed, one way ANOVA with Tukey follow up (or Kruskal&ndash;Wallis) for several groups, and chi square (or Fisher) for categories. Links between two numbers used Pearson and Spearman coefficients with confidence intervals, plus partial correlations that adjust for age. Multiple linear regression handled the numeric outcomes, and multivariable logistic regression handled the yes or no outcomes, reporting adjusted odds ratios. The regression checks covered residual normality, equal spread (Breusch&ndash;Pagan), independence (Durbin&ndash;Watson), influence (Cook's distance and leverage), and overlap between predictors (variance inflation factors). Principal component analysis ran on the standardised correlation matrix. Effect sizes (Hedges g, eta squared, epsilon squared, Cram&eacute;r's V) went with every test. The work used Python with NumPy, pandas, SciPy, statsmodels, Matplotlib, and seaborn.

---

## 4. Results

### 4.1 Descriptive statistics

Among the 5,175 adults, mean BMI was 29.9 kg/m&sup2; (SD 7.4), mean age was 51.2 years, and mean systolic blood pressure was 126.5 mmHg. Most numeric variables leaned to the right; BMI (skewness +1.27), sugar (+1.80), and fasting glucose (+3.73) were the most lopsided. The full tables are in `tables/descriptive_continuous.csv`. The obese group made up 42% of adults, and 47.7% met the 130/80 threshold for high blood pressure.

*What this means.* The strong right skew of the metabolic variables is itself a result: it points to a group of people with much higher body fat and glucose, and it is why we lean on robust and rank based methods further down. **Assumptions:** none needed for description.

### 4.2 Normality and variance

Every numeric variable failed the normality test (all Shapiro&ndash;Wilk p < 0.001; `tables/normality_tests.csv`), and variances differed across every grouping we tried (Levene p < 0.05; `tables/variance_homogeneity_tests.csv`). At this sample size that is no surprise, and it is why we used Welch's t test and confirmed results with rank based tests.

*What this means.* With more than 5,000 people, normality tests are very touchy and almost always come back significant, so we also looked at Q-Q plots (`figures/qqplot_bmi.png`) and skewness, leaned on the central limit theorem for tests of means, and double checked with rank tests. **Assumptions tested:** normality, equal variance.

### 4.3 RQ1, sex differences in BMI

Women had higher mean BMI than men (30.3 vs 29.4 kg/m&sup2;; mean difference &minus;0.91, 95% CI &minus;1.31 to &minus;0.50). Because variances differed (Levene p < 0.001), we used Welch's t test: t = &minus;4.45, p < 0.001, backed up by the Mann&ndash;Whitney U test (p = 0.019). The size of the difference was **tiny** though (Hedges g = &minus;0.12). Larger sex gaps appeared for HDL cholesterol (women +9.6 mg/dL; g = &minus;0.66, medium) and energy intake (men +593 kcal; g = +0.63, medium). See `tables/two_group_tests.csv` and the figures `boxplot_bmi.png` and `density_bmi.png`.

*What this means.* A difference that is significant but tiny is a clear lesson in why effect sizes must sit next to p values in large surveys. The real sex gap in HDL is expected and clinically meaningful. **Assumptions tested:** normality (failed, so Welch and Mann&ndash;Whitney), equal variance.

### 4.4 RQ2, energy intake and BMI

One day of energy intake showed no straight line link with BMI (Pearson r = 0.01, 95% CI &minus;0.02 to 0.04, p = 0.55; Spearman rho = 0.02). By contrast, waist size and BMI were very strongly linked (r = 0.90; figure `scatter_bmi_waist.png`), and energy tracked closely with protein (r = 0.77) and sodium (r = 0.79). See `tables/correlation_pairwise.csv`.

*What this means.* The flat energy and BMI link is both expected and useful to see. A single 24 hour recall is a noisy guess at how someone usually eats, and in a snapshot survey people with high BMI may already be cutting back, which pulls the link toward zero. This is a measurement and design limit, not proof that intake does not matter. **Assumptions:** we checked the shape and spread with a hexbin plot (`scatter_bmi_energy.png`).

### 4.5 RQ3, smoking, body size, and diet

BMI differed across smoking groups (one way ANOVA F(2, 5172) = 16.7, p < 0.001; eta squared = 0.006; Kruskal&ndash;Wallis agreed). In the adjusted logistic model, current smoking went with **lower** odds of obesity (OR 0.67, 95% CI 0.56&ndash;0.80). See `tables/anova_oneway.csv` and `tables/logit_obesity.csv`.

*What this means.* The lower obesity odds among smokers is well known and reflects how nicotine curbs appetite and shifts metabolism, but it is tangled up with income and behaviour and must not be read as a reason to smoke. **Assumptions tested:** ANOVA equal variance (failed, so Kruskal&ndash;Wallis as backup).

### 4.6 RQ4, income, education, and obesity

Obesity was linked to both education (chi square(4) = 71.3, p < 0.001; Cram&eacute;r's V = 0.12) and income group (chi square(2) = 13.9, p < 0.001; V = 0.06). In the adjusted model, each step up in the income to poverty ratio lowered the odds of obesity (OR 0.94, 95% CI 0.91&ndash;0.98). See `tables/categorical_tests.csv` and the forest plot (`figures/forest_plot.png`).

*What this means.* A steady income gradient in obesity shows up across the simple tests and the adjusted model alike, matching a large literature on how diet related disease tracks with social standing. The effects are small but consistent. **Assumptions tested:** expected counts of 5 or more (Fisher used otherwise).

### 4.7 RQ5, age, blood pressure, and high blood pressure

Systolic blood pressure climbed steeply across age groups (ANOVA F(3, 4596) = 393.8, p < 0.001; eta squared = 0.20), and age tracked systolic pressure at r = 0.47. The link between age and high blood pressure was the strongest categorical effect in the study (chi square(3) = 521.3, p < 0.001; Cram&eacute;r's V = 0.34, large). In multiple linear regression, age, BMI, sex, and sodium together explained 23.5% of the variation in systolic pressure (adjusted R squared = 0.234), with age the biggest standardised driver. See `tables/linreg_systolic.csv`, `tables/linreg_model_fit.csv`, and the figures `means_plot_sbp_age.png` and `prediction_plot.png`.

*What this means.* The age and blood pressure link is the largest effect in the analysis and fits the biology, since arteries stiffen with age. The model is useful for description and adjustment, though its residuals were not normal and the spread was uneven (see 4.9), so we lean on the large sample behaviour of the method and on the matching ANOVA and correlation results. **Assumptions tested:** straight line fit, residual normality, equal spread, overlap between predictors.

### 4.8 RQ6, principal component analysis

PCA on eleven standardised body, diet, and clinical variables gave two main components that explained 54.3% of the variation (PC1 28.6%, PC2 25.7%; `tables/pca_explained_variance.csv`). PC1 loaded positively on BMI, waist, weight, and blood pressure and negatively on HDL, a **body size and blood pressure axis**; PC2 loaded on energy, protein, sodium, and fiber, a **food intake axis** (`tables/pca_loadings.csv`, and the figures `pca_scree.png`, `pca_biplot.png`, `pca_loadings.png`). Weight classes separated cleanly along PC1.

*What this means.* PCA shows that the measured variables fold neatly into two readable and largely separate ideas: how much body fat a person carries, and how much they eat. This is plain descriptive ordination. **Assumptions:** linear correlation structure; variables standardised.

### 4.9 Regression checks

Across all three regression models, residuals strayed from normal (Shapiro p < 0.001) and the spread was uneven (Breusch&ndash;Pagan p < 0.001), while independence looked fine (Durbin&ndash;Watson near 2.0). A handful of high influence points showed up on Cook's distance (for example 219 of 4,215 in the blood pressure model), none of them decisive on its own. The variance inflation factors all sat below 3, so there was **no troubling overlap** among the chosen predictors (in particular, BMI and waist were never used together). See `tables/regression_diagnostics.csv`, `tables/linreg_vif.csv`, and the figure `residual_plot.png`.

*What this means.* The failed checks (residuals not normal, spread uneven) are common for skewed health outcomes in large samples, and we report them openly rather than hide them. With more than 4,000 people the coefficients stay steady, but robust standard errors or a transformed outcome would be sensible next steps (see Future Work).

---

## 5. Discussion

This analysis recovers several well known public health patterns, including the income gradient in obesity, the steep rise in blood pressure with age, and the sex gap in HDL, using only clear classical methods. Two threads run through it. First, **significant is not the same as large**: at this sample size even a 0.9 kg/m&sup2; sex gap in BMI is "highly significant" yet tiny by Cohen's yardsticks, and only an effect size reveals that. Second, **design and measurement shape the answer**: the flat energy and BMI link is a predictable result of one day of recall and snapshot reverse causation, not a sign that intake does not matter.

The work is laid out like the statistical supplement of a paper: every figure can be remade from one script, every table is explained, and every assumption is checked before its test is used. For a food microbiology, food safety, nutrition, or public health lab, these are exactly the skills needed to turn data into claims that hold up.

---

## 6. Limitations

NHANES uses a complex, layered sample design. This analysis is **unweighted** to keep it clear, so the numbers here describe this sample rather than the whole country. The design is a snapshot, so it cannot show cause and effect. Diet rests on a single 24 hour recall, which varies a lot from day to day within a person. Smoking and income are self reported. Several regression models had residuals that were not normal and spread unevenly. These points are stated plainly and drive the planned next steps.

---

## 7. Conclusion

A careful classical workflow, with assumptions checked first, the right test second, and effect sizes and confidence intervals always, gives clear, honest, and sensible results from NHANES. The project shows statistical care, reproducibility, and plain communication, the skills needed to take part in research on food safety, nutrition, microbiology, and public health.

---

## 8. References

The full list is in `references/references.md`. Main sources: CDC NHANES 2017&ndash;2018; WHO (2000); Whelton et al. (2018); Cohen (1988); Hedges (1981); Shapiro and Wilk (1965); Levene (1960); Mann and Whitney (1947); Kruskal and Wallis (1952); Cram&eacute;r (1946); Breusch and Pagan (1979); Cook (1977); Jolliffe (2002); Whitlock and Schluter (2020); Seabold and Perktold (2010).
