import numpy as np
import pandas as pd

from src.utils.io import load_analytic, save_table

PCA_VARS = [
    "BMI", "WaistCircumference", "Weight", "SystolicBP", "DiastolicBP",
    "EnergyKcal", "ProteinG", "SodiumMg", "FiberG", "HDL", "Age",
]


def standardize(X):
    mu = X.mean(axis=0)
    sd = X.std(axis=0, ddof=1)
    return (X - mu) / sd


def run_pca(df, columns):
    sub = df[columns].dropna()
    Z = standardize(sub.values)
    cov = np.cov(Z, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]
    scores = Z @ eigvecs
    explained = eigvals / eigvals.sum()
    return {
        "columns": columns,
        "eigenvalues": eigvals,
        "explained": explained,
        "cum_explained": np.cumsum(explained),
        "loadings": eigvecs,
        "scores": scores,
        "index": sub.index,
        "n": len(sub),
    }


def main():
    df = load_analytic()
    cols = [c for c in PCA_VARS if c in df.columns]
    res = run_pca(df, cols)

    var_table = pd.DataFrame(
        {
            "Component": [f"PC{i+1}" for i in range(len(res["eigenvalues"]))],
            "Eigenvalue": res["eigenvalues"].round(4),
            "Explained_Variance_pct": (res["explained"] * 100).round(2),
            "Cumulative_pct": (res["cum_explained"] * 100).round(2),
        }
    )
    save_table(var_table, "pca_explained_variance", index=False)

    n_keep = min(4, res["loadings"].shape[1])
    loadings = pd.DataFrame(
        res["loadings"][:, :n_keep],
        index=cols,
        columns=[f"PC{i+1}" for i in range(n_keep)],
    ).round(3)
    loadings.index.name = "Variable"
    save_table(loadings.reset_index(), "pca_loadings", index=False)

    print(f"PCA on {len(cols)} standardized variables, N = {res['n']}.")
    print(var_table.head(6).to_string(index=False))


if __name__ == "__main__":
    main()
