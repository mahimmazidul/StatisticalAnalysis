import numpy as np
from scipy import stats


def cohens_d(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    pooled = np.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    if pooled == 0:
        return 0.0
    return (a.mean() - b.mean()) / pooled


def hedges_g(a, b):
    d = cohens_d(a, b)
    n = len(a) + len(b)
    correction = 1 - (3 / (4 * n - 9))
    return d * correction


def rank_biserial_from_u(u, n1, n2):
    return 1 - (2 * u) / (n1 * n2)


def eta_squared_anova(groups):
    grand = np.concatenate(groups)
    grand_mean = grand.mean()
    ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in groups)
    ss_total = ((grand - grand_mean) ** 2).sum()
    if ss_total == 0:
        return 0.0
    return ss_between / ss_total


def epsilon_squared_kruskal(h, n):
    return h / (n - 1) if n > 1 else 0.0


def cramers_v(table):
    table = np.asarray(table, dtype=float)
    chi2 = stats.chi2_contingency(table, correction=False)[0]
    n = table.sum()
    r, k = table.shape
    phi2 = chi2 / n
    return np.sqrt(phi2 / min(r - 1, k - 1)) if min(r - 1, k - 1) > 0 else 0.0


def mean_ci(x, conf=0.95):
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    m = x.mean()
    se = x.std(ddof=1) / np.sqrt(n)
    t = stats.t.ppf(1 - (1 - conf) / 2, n - 1)
    return m, m - t * se, m + t * se


def interpret_d(d):
    a = abs(d)
    if a < 0.2:
        return "negligible"
    if a < 0.5:
        return "small"
    if a < 0.8:
        return "medium"
    return "large"


def interpret_r(r):
    a = abs(r)
    if a < 0.1:
        return "negligible"
    if a < 0.3:
        return "weak"
    if a < 0.5:
        return "moderate"
    if a < 0.7:
        return "strong"
    return "very strong"


def interpret_cramers_v(v, dof):
    small = {1: 0.10, 2: 0.07, 3: 0.06}.get(dof, 0.05)
    medium = {1: 0.30, 2: 0.21, 3: 0.17}.get(dof, 0.15)
    large = {1: 0.50, 2: 0.35, 3: 0.29}.get(dof, 0.25)
    if v < small:
        return "negligible"
    if v < medium:
        return "small"
    if v < large:
        return "medium"
    return "large"


def stars(p):
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return "ns"
