---
layout: default
title: API Reference
nav_order: 3
---

# API Reference

## `fit_ellipsoid(points)`

Fit an ellipsoid to a 3D point cloud.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `points` | `ndarray (N, 3)` | 3D point cloud. N ≥ 9 required. |

**Returns** `EllipsoidParameters`

**Raises**
- `ValueError` – if fewer than 9 points are given, or the data cannot be fitted by an ellipsoid.

---

## `EllipsoidParameters`

Named tuple returned by `fit_ellipsoid`.

| Field | Type | Description |
|-------|------|-------------|
| `center` | `ndarray (3,)` | Ellipsoid centre (x₀, y₀, z₀) |
| `radii` | `ndarray (3,)` | Semi-axis lengths, descending order |
| `rotation` | `ndarray (3, 3)` | Rotation matrix (principal axes as columns) |
| `algebraic` | `ndarray (10,)` | Raw algebraic coefficient vector |

---

## `algebraic_to_geometric(v)`

Convert a 10-element algebraic coefficient vector to geometric parameters.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `v` | `array_like (10,)` | Coefficients `[a, b, c, f, g, h, p, q, r, d]` |

**Returns** `EllipsoidParameters`

---

## `generate_ellipsoid_points(...)`

Generate random 3D points on an ellipsoid surface.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `center` | `array_like (3,)` | required | Centre |
| `radii` | `array_like (3,)` | required | Semi-axes |
| `rotation` | `ndarray (3,3)` | identity | Orientation |
| `n_points` | `int` | 500 | Number of points |
| `noise_std` | `float` | 0.0 | Gaussian noise σ |
| `rng` | `np.random.Generator` | None | RNG for reproducibility |

**Returns** `ndarray (n_points, 3)`

---

## `plot_fit(points, params, ...)`

3D visualisation of the point cloud and fitted ellipsoid.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `points` | `ndarray (N, 3)` | required | Input points |
| `params` | `EllipsoidParameters` | required | Fit result |
| `n_surface` | `int` | 40 | Surface mesh resolution |
| `show` | `bool` | True | Call `plt.show()` |

**Returns** `matplotlib.axes.Axes3D`

---

## `load_point_cloud(filepath)`

Load a point cloud from a CSV or space-delimited text file.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `filepath` | `str` | Path to file (columns x, y, z; `#` comments ignored) |

**Returns** `ndarray (N, 3)`
