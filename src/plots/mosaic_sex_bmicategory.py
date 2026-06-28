import matplotlib.pyplot as plt
from statsmodels.graphics.mosaicplot import mosaic

from src.utils.io import load_analytic
from src.utils.style import scaled, PALETTE, apply_style, save_figure

BMI_ORDER = ["Underweight", "Normal", "Overweight", "Obese"]


def build():
    apply_style()
    df = load_analytic().dropna(subset=["Sex", "BMICategory"]).copy()
    df["BMICategory"] = df["BMICategory"].astype(str)
    colors = dict(zip(BMI_ORDER, PALETTE[:4]))

    def props(key):
        return {"color": colors.get(key[1], "#999999"), "edgecolor": "white"}

    fig, ax = plt.subplots(figsize=scaled(8, 5))
    mosaic(df, ["Sex", "BMICategory"], ax=ax, properties=props, gap=0.015, labelizer=lambda k: "")
    ax.set_title("Mosaic Plot: Sex by BMI Category")
    return save_figure(fig, "mosaic_sex_bmicategory", "Mosaic of sex by BMI category")


if __name__ == "__main__":
    build()
