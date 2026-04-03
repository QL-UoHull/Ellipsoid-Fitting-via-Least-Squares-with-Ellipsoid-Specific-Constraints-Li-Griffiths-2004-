---
layout: default
title: Home
nav_order: 1
---

# Ellipsoid Fitting via Least Squares
## Li & Griffiths (2004) – Python Implementation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/QL-UoHull/Ellipsoid-Fitting-via-Least-Squares-with-Ellipsoid-Specific-Constraints-Li-Griffiths-2004-/blob/main/notebooks/ellipsoid_fitting_demo.ipynb)

---

## Overview

This repository provides a clean Python implementation of the **constrained least-squares ellipsoid fitting** method described in:

> Q. Li and J. G. Griffiths, *"Least Squares Ellipsoid Specific Fitting"*, Geometric Modeling and Processing, 2004. DOI: [10.1109/GMAP.2004.1290055](https://doi.org/10.1109/GMAP.2004.1290055)

Given a set of 3D points lying approximately on an ellipsoidal surface, the algorithm recovers the **centre**, **semi-axis lengths**, and **orientation** of the best-fit ellipsoid while guaranteeing that the result is always a geometrically valid ellipsoid.

---

## Algorithm

Any quadric surface satisfies:

$$F(\mathbf{x}) = ax^2 + by^2 + cz^2 + 2fyz + 2gxz + 2hxy + 2px + 2qy + 2rz + d = 0$$

The key insight of Li & Griffiths is an **ellipsoid-specific constraint**:

$$\kappa = 4ac - g^2 + 4bc - f^2 + 4ab - h^2 > 0$$

This transforms fitting into a **constrained generalised eigenvalue problem** `S v = λ C v`, whose unique positive eigenvalue yields the ellipsoid coefficients.

---

## Quick Start

```python
from ellipsoid_fitting import fit_ellipsoid
from ellipsoid_fitting.utils import generate_ellipsoid_points
import numpy as np

# Generate noisy test points
pts = generate_ellipsoid_points(
    center=[0, 0, 0], radii=[3, 2, 1],
    n_points=500, noise_std=0.05,
    rng=np.random.default_rng(42),
)

# Fit
params = fit_ellipsoid(pts)
print(params.center)  # ≈ [0, 0, 0]
print(params.radii)   # ≈ [3, 2, 1]
```

---

## Pages

- [Installation](installation.md)
- [API Reference](api.md)
- [Examples](examples.md)
- [Point Cloud Data](data.md)
