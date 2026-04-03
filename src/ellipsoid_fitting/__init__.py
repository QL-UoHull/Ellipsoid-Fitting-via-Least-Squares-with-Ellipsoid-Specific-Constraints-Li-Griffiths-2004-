"""
ellipsoid_fitting
=================
Python implementation of the Li–Griffiths least-squares ellipsoid-specific
fitting algorithm (Li & Griffiths, 2004).

Usage
-----
>>> from ellipsoid_fitting import fit_ellipsoid, EllipsoidParameters
>>> params = fit_ellipsoid(points)
>>> print(params.center, params.radii)
"""

from ellipsoid_fitting.fit import fit_ellipsoid
from ellipsoid_fitting.utils import EllipsoidParameters, algebraic_to_geometric

__all__ = ["fit_ellipsoid", "EllipsoidParameters", "algebraic_to_geometric"]
__version__ = "0.1.0"
