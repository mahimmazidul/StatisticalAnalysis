import importlib
import sys

from src.utils.paths import CLEAN_FILE, ensure_dirs

ANALYSES = [
    "descriptive_statistics",
    "crosstabs",
    "normality_tests",
    "variance_tests",
    "group_tests_two",
    "anova",
    "categorical_tests",
    "correlation",
    "linear_regression",
    "logistic_regression",
    "regression_diagnostics",
    "pca",
]

PLOTS = [
    "histogram_bmi",
    "density_bmi",
    "boxplot_bmi",
    "violin_bmi",
    "ecdf_bmi",
    "qqplot_bmi",
    "ridgeline_bmi_age",
    "scatter_bmi_waist",
    "scatter_bmi_energy",
    "strip_rug_hdl",
    "bar_bmicategory",
    "stacked_bar_smoking_bmi",
    "grouped_bar_obesity",
    "mosaic_sex_bmicategory",
    "correlation_heatmap",
    "correlation_clustered",
    "pairplot_diet",
    "pca_scree",
    "pca_loadings",
    "pca_biplot",
    "coefficient_plot_linear",
    "forest_plot",
    "residual_plot",
    "prediction_plot",
    "means_plot_sbp_age",
    "missingness",
]


def ensure_data():
    if CLEAN_FILE.exists():
        return
    from src import download_data, make_offline_data, preprocess

    ok, fail = download_data.download()
    if fail:
        make_offline_data.main()
    preprocess.main()


def main():
    ensure_dirs()
    ensure_data()
    for mod in ANALYSES:
        m = importlib.import_module(f"src.analysis.{mod}")
        m.main()
        print(f"[analysis] {mod} complete")
    for mod in PLOTS:
        m = importlib.import_module(f"src.plots.{mod}")
        m.build()
        print(f"[figure] {mod} complete")
    from src import build_report

    build_report.main()
    print("All analyses, figures and the report were generated.")


if __name__ == "__main__":
    sys.exit(main())
