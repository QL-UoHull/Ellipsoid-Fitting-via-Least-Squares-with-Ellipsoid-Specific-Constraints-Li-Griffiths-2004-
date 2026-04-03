"""
basic_fit.py
------------
Minimal example: fit an ellipsoid to a synthetic noisy point cloud
and print the recovered geometric parameters.

Run:
    python examples/basic_fit.py
"""

import sys
import os

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ellipsoid_fitting import fit_ellipsoid
from ellipsoid_fitting.utils import generate_ellipsoid_points

# ── Ground-truth parameters ──────────────────────────────────────────────────
TRUE_CENTER = np.array([2.0, -1.0, 3.0])
TRUE_RADII  = np.array([5.0,  3.0, 1.5])

# ── Generate noisy surface points ────────────────────────────────────────────
rng = np.random.default_rng(42)
points = generate_ellipsoid_points(
    center=TRUE_CENTER,
    radii=TRUE_RADII,
    n_points=800,
    noise_std=0.05,
    rng=rng,
)

print(f"Fitting ellipsoid to {len(points)} noisy surface points ...\n")

# ── Fit ───────────────────────────────────────────────────────────────────────
params = fit_ellipsoid(points)

# ── Report ────────────────────────────────────────────────────────────────────
print("Ground-truth centre :", TRUE_CENTER)
print("Fitted centre       :", np.round(params.center, 3))
print()
print("Ground-truth radii  :", sorted(TRUE_RADII, reverse=True))
print("Fitted radii        :", np.round(sorted(params.radii, reverse=True), 3))
print()
print("Rotation matrix (fitted):")
print(np.round(params.rotation, 4))
