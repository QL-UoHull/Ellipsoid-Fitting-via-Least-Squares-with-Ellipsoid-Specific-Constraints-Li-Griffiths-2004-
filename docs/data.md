---
layout: default
title: Point Cloud Data
nav_order: 5
---

# Point Cloud Data

All sample datasets are in the `data/` directory.

| File | Shape | True radii | True centre |
|------|-------|-----------|-------------|
| `unit_sphere_noisy.csv` | sphere | (1, 1, 1) | (0, 0, 0) |
| `ellipsoid_3_2_1.csv` | axis-aligned | (3, 2, 1) | (0, 0, 0) |
| `ellipsoid_rotated_offset.csv` | rotated & offset | (4, 2.5, 1.5) | (5, -3, 2) |
| `prolate_spheroid.csv` | prolate (cigar) | (1, 1, 5) | (0, 0, 0) |
| `oblate_spheroid.csv` | oblate (disc) | (4, 4, 1) | (0, 0, 0) |

## Loading data

```python
from ellipsoid_fitting.utils import load_point_cloud

pts = load_point_cloud('data/ellipsoid_3_2_1.csv')
```

## Generating custom datasets

```python
from ellipsoid_fitting.utils import generate_ellipsoid_points
import numpy as np

pts = generate_ellipsoid_points(
    center=[1, 2, 3], radii=[5, 3, 2],
    n_points=1000, noise_std=0.05,
    rng=np.random.default_rng(42),
)
np.savetxt('my_data.csv', pts, fmt='%.6f', header='x y z', comments='# ')
```
