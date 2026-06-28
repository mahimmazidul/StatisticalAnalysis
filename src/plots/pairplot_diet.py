import matplotlib.pyplot as plt
import seaborn as sns

from src.utils.io import load_analytic
from src.utils.paths import FIGURES
from src.utils.style import SEX_PALETTE, apply_style

VARS = ["BMI", "EnergyKcal", "ProteinG", "FiberG", "SodiumMg"]


def build():
    apply_style()
    df = load_analytic()
    sub = df[VARS + ["Sex"]].dropna().sample(n=min(1500, len(df)), random_state=7)
    g = sns.pairplot(sub, vars=VARS, hue="Sex", palette=SEX_PALETTE,
                     corner=True, plot_kws={"s": 10, "alpha": 0.3}, diag_kind="kde", height=2.3)
    g.figure.suptitle("Pairwise Relationships Among Dietary and Anthropometric Variables",
                      y=1.02, fontweight="bold")
    FIGURES.mkdir(parents=True, exist_ok=True)
    png = FIGURES / "pairplot_diet.png"
    svg = FIGURES / "pairplot_diet.svg"
    g.figure.savefig(png, dpi=300, bbox_inches="tight")
    g.figure.savefig(svg, bbox_inches="tight")
    plt.close(g.figure)
    return png, svg


if __name__ == "__main__":
    build()
