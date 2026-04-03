"""
fit_from_file.py
----------------
Load a point cloud from a CSV file (one of the files in data/) and fit
an ellipsoid to it.

Run:
    python examples/fit_from_file.py data/ellipsoid_3_2_1.csv
"""

import sys
import os

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ellipsoid_fitting import fit_ellipsoid
from ellipsoid_fitting.utils import load_point_cloud

if len(sys.argv) < 2:
    default = os.path.join(
        os.path.dirname(__file__), "..", "data", "ellipsoid_3_2_1.csv"
    )
    filepath = default
    print(f"No file supplied – using default: {os.path.basename(default)}\n")
else:
    filepath = sys.argv[1]

points = load_point_cloud(filepath)
print(f"Loaded {len(points)} points from '{filepath}'\n")

params = fit_ellipsoid(points)
print(params)
