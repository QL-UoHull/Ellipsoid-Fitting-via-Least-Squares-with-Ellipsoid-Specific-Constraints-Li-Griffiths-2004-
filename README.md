# Ellipsoid Fitting via Least Squares with Ellipsoid-Specific Constraints

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-15%20passed-brightgreen)](#running-the-tests)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/QL-UoHull/Ellipsoid-Fitting-via-Least-Squares-with-Ellipsoid-Specific-Constraints-Li-Griffiths-2004-/blob/main/notebooks/ellipsoid_fitting_demo.ipynb)
[![DOI](https://img.shields.io/badge/paper-10.1109%2FGMAP.2004.1290055-blue)](https://doi.org/10.1109/GMAP.2004.1290055)

---

A Python implementation of the **Li–Griffiths constrained least-squares ellipsoid fitting** algorithm.

> Q. Li and J. G. Griffiths, *"Least Squares Ellipsoid Specific Fitting"*,
> Proceedings of the Geometric Modeling and Processing, Beijing, China, 2004,
> pp. 335–340. DOI: [10.1109/GMAP.2004.1290055](https://doi.org/10.1109/GMAP.2004.1290055)

Given a set of 3D surface points, this package fits a **geometrically valid ellipsoid** – centre, semi-axis lengths, and orientation – using an algebraic constrained eigenvalue approach that guarantees the result is always a real ellipsoid.

---

## Table of Contents

- [Features](#features)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Algorithm Overview](#algorithm-overview)
- [Point Cloud Data](#point-cloud-data)
- [Reproducibility Resources](#reproducibility-resources)
- [Running the Tests](#running-the-tests)
- [Documentation](#documentation)
- [Citation](#citation)
- [License](#license)

---

## Features

- ✅ Ellipsoid-specific constraint (always yields a valid ellipsoid, not a hyperboloid or paraboloid)
- ✅ Recovers centre, semi-axis lengths, and rotation matrix
- ✅ Handles noise, arbitrary orientation, and off-centre ellipsoids
- ✅ Minimal dependencies: NumPy + SciPy only for the core algorithm
- ✅ Sample point cloud datasets included
- ✅ Interactive Jupyter/Colab notebook

---

## Repository Structure

```
.
├── src/
│   └── ellipsoid_fitting/
│       ├── __init__.py        # Public API
│       ├── fit.py             # Core Li–Griffiths algorithm
│       ├── utils.py           # Data generation, algebraic↔geometric conversion
│       └── visualization.py   # 3D matplotlib plotting helpers
├── tests/
│   └── test_ellipsoid_fitting.py   # 15 unit tests (pytest)
├── data/
│   ├── unit_sphere_noisy.csv
│   ├── ellipsoid_3_2_1.csv
│   ├── ellipsoid_rotated_offset.csv
│   ├── prolate_spheroid.csv
│   └── oblate_spheroid.csv
├── examples/
│   ├── basic_fit.py           # Minimal usage example
│   └── fit_from_file.py       # Load and fit from CSV
├── notebooks/
│   └── ellipsoid_fitting_demo.ipynb   # Interactive Colab/Jupyter demo
├── docs/                      # GitHub Pages documentation
├── CITATION.cff               # Machine-readable citation
├── LICENSE                    # MIT
└── pyproject.toml
```

---

## Installation

**Requirements:** Python 3.8+, NumPy ≥ 1.21, SciPy ≥ 1.7, Matplotlib ≥ 3.4

```bash
git clone https://github.com/QL-UoHull/Ellipsoid-Fitting-via-Least-Squares-with-Ellipsoid-Specific-Constraints-Li-Griffiths-2004-.git
cd Ellipsoid-Fitting-via-Least-Squares-with-Ellipsoid-Specific-Constraints-Li-Griffiths-2004-
pip install -e .
```

Or install dependencies manually and add `src/` to your path:

```bash
pip install numpy scipy matplotlib
```

---

## Quick Start

```python
from ellipsoid_fitting import fit_ellipsoid
from ellipsoid_fitting.utils import generate_ellipsoid_points
import numpy as np

# Generate noisy points on an ellipsoidal surface
pts = generate_ellipsoid_points(
    center=[0, 0, 0],
    radii=[3, 2, 1],
    n_points=500,
    noise_std=0.05,
    rng=np.random.default_rng(42),
)

# Fit
params = fit_ellipsoid(pts)

print("Centre :", params.center)   # ≈ [0, 0, 0]
print("Radii  :", params.radii)    # ≈ [3, 2, 1]
print("Rotation:\n", params.rotation)
```

Load from a CSV file:

```python
from ellipsoid_fitting.utils import load_point_cloud

pts = load_point_cloud("data/ellipsoid_rotated_offset.csv")
params = fit_ellipsoid(pts)
print(params)
```

Visualise:

```python
from ellipsoid_fitting.visualization import plot_fit
plot_fit(pts, params)
```

---

## Algorithm Overview

Any quadric surface satisfies the algebraic equation:

$$F(\mathbf{x}) = ax^2 + by^2 + cz^2 + 2fyz + 2gxz + 2hxy + 2px + 2qy + 2rz + d = 0$$

with coefficient vector **v** = [a, b, c, f, g, h, p, q, r, d]ᵀ.

**Li & Griffiths (2004)** derive an ellipsoid-specific algebraic constraint:

$$\kappa = 4ac - g^2 + 4bc - f^2 + 4ab - h^2 > 0$$

and show that fitting under this constraint reduces to solving the generalised eigenvalue problem:

$$S\,\mathbf{v} = \lambda\,C\,\mathbf{v}$$

where **S** = DᵀD is the scatter matrix built from the data and **C** encodes the constraint. The solution is the eigenvector corresponding to the **unique positive eigenvalue**.

---

## Point Cloud Data

Five synthetic datasets are provided in `data/`:

| File | Description | True radii | True centre |
|------|-------------|-----------|-------------|
| `unit_sphere_noisy.csv` | Noisy unit sphere | (1, 1, 1) | (0, 0, 0) |
| `ellipsoid_3_2_1.csv` | Axis-aligned ellipsoid | (3, 2, 1) | (0, 0, 0) |
| `ellipsoid_rotated_offset.csv` | Rotated 30°/15°, offset | (4, 2.5, 1.5) | (5, −3, 2) |
| `prolate_spheroid.csv` | Cigar-shaped spheroid | (1, 1, 5) | (0, 0, 0) |
| `oblate_spheroid.csv` | Disc-shaped spheroid | (4, 4, 1) | (0, 0, 0) |

Each file is space-separated with a `# x y z` header. All datasets include Gaussian noise (σ = 0.02–0.05) for realism.

---

## Reproducibility Resources

| Resource | Link |
|----------|------|
| Jupyter / Colab notebook | [`notebooks/ellipsoid_fitting_demo.ipynb`](notebooks/ellipsoid_fitting_demo.ipynb) |
| Open in Colab | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/QL-UoHull/Ellipsoid-Fitting-via-Least-Squares-with-Ellipsoid-Specific-Constraints-Li-Griffiths-2004-/blob/main/notebooks/ellipsoid_fitting_demo.ipynb) |
| Example scripts | [`examples/`](examples/) |
| Sample data | [`data/`](data/) |

The notebook covers:
- Algorithm walkthrough with equations
- Fitting a unit sphere, axis-aligned ellipsoid, and rotated+offset ellipsoid
- Loading data from file
- 3D visualisation
- Accuracy benchmark vs. noise level

---

## Running the Tests

```bash
PYTHONPATH=src python -m pytest tests/ -v
```

Expected output: **15 tests passed**.

---

## Documentation

Full documentation is available on **GitHub Pages**:  
👉 https://ql-uohull.github.io/Ellipsoid-Fitting-via-Least-Squares-with-Ellipsoid-Specific-Constraints-Li-Griffiths-2004-

Topics covered: Installation, API Reference, Examples, Point Cloud Data.

---

## Citation

If you use this code, please cite both this software and the original paper:

```bibtex
@article{li2004ellipsoid,
  title     = {Least Squares Ellipsoid Specific Fitting},
  author    = {Li, Qingde and Griffiths, John G.},
  booktitle = {Proceedings of the Geometric Modeling and Processing},
  year      = {2004},
  pages     = {335--340},
  doi       = {10.1109/GMAP.2004.1290055}
}
```

A `CITATION.cff` file is included for automatic citation on GitHub.

---

## License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE) for details.

