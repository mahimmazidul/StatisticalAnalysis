import html
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from src.utils.paths import FIGURES, REPORT

ENTITIES = {
    "&ndash;": "-", "&mdash;": "—", "&minus;": "-", "&plusmn;": "±",
    "&times;": "×", "&ge;": ">=", "&le;": "<=", "&asymp;": "~",
    "&eta;": "eta", "&epsilon;": "epsilon", "&rho;": "rho", "&chi;": "chi",
    "&sup2;": "^2", "&hellip;": "...", "&rarr;": "->", "&amp;": "&",
    "&Cram": "&Cram",
}

TEAL = colors.HexColor("#264653")
GREEN = colors.HexColor("#2a9d8f")
ORANGE = colors.HexColor("#e76f51")


def _clean(text):
    text = text.replace("Cram&eacute;r", "Cramer").replace("&eacute;", "e")
    for k, v in ENTITIES.items():
        text = text.replace(k, v)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+)`", r"<font face='Courier'>\1</font>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    return text


def _styles():
    ss = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("t", parent=ss["Title"], fontSize=22, textColor=TEAL, spaceAfter=6),
        "subtitle": ParagraphStyle("st", parent=ss["Normal"], fontSize=12, textColor=GREEN,
                                    alignment=TA_CENTER, spaceAfter=14, fontName="Helvetica-Oblique"),
        "h1": ParagraphStyle("h1", parent=ss["Heading1"], fontSize=15, textColor=TEAL,
                             spaceBefore=14, spaceAfter=6),
        "h2": ParagraphStyle("h2", parent=ss["Heading2"], fontSize=12.5, textColor=GREEN,
                             spaceBefore=10, spaceAfter=4),
        "h3": ParagraphStyle("h3", parent=ss["Heading3"], fontSize=11, textColor=ORANGE,
                             spaceBefore=8, spaceAfter=3),
        "body": ParagraphStyle("b", parent=ss["Normal"], fontSize=9.7, leading=14,
                               alignment=TA_JUSTIFY, spaceAfter=6),
        "caption": ParagraphStyle("c", parent=ss["Normal"], fontSize=8.5, leading=11,
                                  textColor=colors.HexColor("#555555"), alignment=TA_CENTER,
                                  spaceAfter=10, fontName="Helvetica-Oblique"),
    }
    return styles


FIGURE_FOR_SECTION = {
    "4.1": ("histogram_bmi.png", "Figure 1. Distribution of BMI in U.S. adults."),
    "4.3": ("boxplot_bmi.png", "Figure 3. BMI by sex."),
    "4.4": ("scatter_bmi_waist.png", "Figure 8. Waist circumference versus BMI."),
    "4.6": ("forest_plot.png", "Figure 23. Adjusted odds ratios for obesity."),
    "4.7": ("means_plot_sbp_age.png", "Figure 25. Mean systolic blood pressure by age and sex."),
    "4.8": ("pca_biplot.png", "Figure 20. PCA biplot."),
    "4.9": ("residual_plot.png", "Figure 24. Regression diagnostics."),
}


def _add_figure(story, styles, fig, caption):
    path = FIGURES / fig
    if not path.exists():
        return
    img = Image(str(path))
    max_w = 15.5 * cm
    ratio = img.imageHeight / img.imageWidth
    img.drawWidth = max_w
    img.drawHeight = max_w * ratio
    if img.drawHeight > 9 * cm:
        img.drawHeight = 9 * cm
        img.drawWidth = img.drawHeight / ratio
    story.append(Spacer(1, 4))
    story.append(img)
    story.append(Paragraph(caption, styles["caption"]))


def build():
    md = (REPORT / "report.md").read_text(encoding="utf-8")
    styles = _styles()
    story = []

    lines = md.splitlines()
    in_title = True
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.strip() == "---":
            story.append(Spacer(1, 4))
            story.append(HRFlowable(width="100%", thickness=0.6, color=GREEN))
            continue
        if line.startswith("# "):
            story.append(Paragraph(_clean(line[2:]), styles["title"]))
            in_title = True
            continue
        if line.startswith("### ") and in_title:
            story.append(Paragraph(_clean(line[4:]), styles["subtitle"]))
            in_title = False
            continue
        if line.startswith("## "):
            story.append(Paragraph(_clean(line[3:]), styles["h1"]))
            continue
        if line.startswith("### "):
            text = line[4:]
            story.append(Paragraph(_clean(text), styles["h2"]))
            key = text.split()[0].rstrip(".") if text[:1].isdigit() else None
            if key in FIGURE_FOR_SECTION:
                fig, cap = FIGURE_FOR_SECTION[key]
                _add_figure(story, styles, fig, cap)
            continue
        if line.startswith("#### "):
            story.append(Paragraph(_clean(line[5:]), styles["h3"]))
            continue
        story.append(Paragraph(_clean(line), styles["body"]))

    doc = SimpleDocTemplate(
        str(REPORT / "report.pdf"), pagesize=A4,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="Applied Statistical Analysis in Food Safety, Nutrition and Public Health",
    )
    doc.build(story)
    print(f"Wrote {REPORT / 'report.pdf'}")


def main():
    build()


if __name__ == "__main__":
    main()
