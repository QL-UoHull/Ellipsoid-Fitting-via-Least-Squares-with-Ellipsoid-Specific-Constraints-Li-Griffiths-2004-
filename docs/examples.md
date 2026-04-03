---
layout: default
title: Examples
nav_order: 4
---

# Examples

All example scripts are in the `examples/` directory.

## Basic fit

```python
# examples/basic_fit.py
from ellipsoid_fitting import fit_ellipsoid
from ellipsoid_fitting.utils import generate_ellipsoid_points
import numpy as np

rng = np.random.default_rng(42)
pts = generate_ellipsoid_points([2, -1, 3], [5, 3, 1.5],
                                 n_points=800, noise_std=0.05, rng=rng)
params = fit_ellipsoid(pts)
print(params)
```

Run from the repo root:
```bash
python examples/basic_fit.py
```

## Fit from file

```bash
python examples/fit_from_file.py data/ellipsoid_3_2_1.csv
```

## Interactive notebook

Open `notebooks/ellipsoid_fitting_demo.ipynb` in Jupyter or Colab.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/QL-UoHull/Ellipsoid-Fitting-via-Least-Squares-with-Ellipsoid-Specific-Constraints-Li-Griffiths-2004-/blob/main/notebooks/ellipsoid_fitting_demo.ipynb)
