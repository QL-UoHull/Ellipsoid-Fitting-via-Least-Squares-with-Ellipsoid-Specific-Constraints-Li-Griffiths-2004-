# Point Cloud Data

This directory contains synthetic 3D point cloud datasets for testing the
ellipsoid fitting algorithm.

## Files

| File | Description | True radii | True centre |
|------|-------------|-----------|-------------|
| `unit_sphere_noisy.csv` | Unit sphere with σ = 0.02 noise | (1, 1, 1) | (0, 0, 0) |
| `ellipsoid_3_2_1.csv` | Axis-aligned ellipsoid with σ = 0.05 | (3, 2, 1) | (0, 0, 0) |
| `ellipsoid_rotated_offset.csv` | Rotated (30°/15°) and offset ellipsoid | (4, 2.5, 1.5) | (5, -3, 2) |
| `prolate_spheroid.csv` | Prolate (cigar-shaped) spheroid | (1, 1, 5) | (0, 0, 0) |
| `oblate_spheroid.csv` | Oblate (disc-shaped) spheroid | (4, 4, 1) | (0, 0, 0) |

## Format

Each file is a space-separated CSV with a single comment header line:

```
# x y z
x1 y1 z1
x2 y2 z2
...
```

## Generating Your Own Data

```python
from ellipsoid_fitting.utils import generate_ellipsoid_points
import numpy as np

pts = generate_ellipsoid_points(
    center=[1, 2, 3],
    radii=[5, 3, 2],
    n_points=1000,
    noise_std=0.05,
    rng=np.random.default_rng(42),
)
np.savetxt("my_ellipsoid.csv", pts, fmt="%.6f", header="x y z", comments="# ")
```
