# Ellipsoid Fitting (Li–Griffiths 2004) — Constrained Least‑Squares for 3D Point Clouds

**Keywords:** ellipsoid fitting, constrained least squares, quadric fitting, 3D point cloud, geometric modeling, generalized eigenvalue problem, scatter matrix, Python, NumPy, SciPy

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A research-oriented **Python implementation** of the **Li–Griffiths (2004)** algorithm for **least‑squares ellipsoid fitting with ellipsoid‑specific constraints**.

Unlike unconstrained algebraic quadric fitting (which may yield hyperboloids/paraboloids), this method enforces conditions that produce a **valid ellipsoid** when fitting noisy **3D point‑cloud data**.

> **Primary reference (peer‑reviewed):**
> Li, Q. and Griffiths, J. G. (2004). *Least squares ellipsoid specific fitting.*
> *Proceedings of the Geometric Modeling and Processing, 2004* (IEEE), pp. 335–340.
> DOI: 10.1109/GMAP.2004.1290055

---

## What this repository provides

- Constrained **least‑squares ellipsoid fitting** for 3D Cartesian point sets
- Conversion from algebraic quadric coefficients to geometric parameters: **centre**, **semi‑axis lengths**, and **orientation**
- Reproducible **datasets**, runnable **examples**, and a **Jupyter notebook** demo
- **CITATION.cff** for GitHub’s “Cite this repository” feature

---

## Installation

```bash
# Clone
# (Note: after renaming, the repo will be: ellipsoid-fitting-li)
git clone https://github.com/QL-UoHull/ellipsoid-fitting-li.git
cd ellipsoid-fitting-li

pip install -r requirements.txt
# Optional: editable install
pip install -e .
```

**Dependencies:** NumPy, SciPy, Matplotlib.

---

## Quick start

```python
import numpy as np
from ellipsoid_fitting import fit_ellipsoid, generate_ellipsoid_points

pts = generate_ellipsoid_points(
    centre=(1.0, 2.0, 3.0),
    radii=(5.0, 3.0, 2.0),
    n_points=300,
    noise_std=0.05,
)

result = fit_ellipsoid(pts[:, 0], pts[:, 1], pts[:, 2])

print("Centre:", result["centre"])
print("Radii :", result["radii"])
print("Axes  :", result["axes"])  
```

---

## Citation

If you use this code in academic work, please cite the original method:

```bibtex
@inproceedings{li2004ellipsoid,
  title     = {Least squares ellipsoid specific fitting},
  author    = {Li, Qingde and Griffiths, John G.},
  booktitle = {Proceedings of the Geometric Modeling and Processing, 2004},
  pages     = {335--340},
  year      = {2004},
  publisher = {IEEE},
  doi       = {10.1109/GMAP.2004.1290055}
}
```

---

## License

MIT License — see [LICENSE](LICENSE).