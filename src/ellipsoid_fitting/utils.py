"""
utils.py
--------
Helper functions for converting between the algebraic and geometric
representations of an ellipsoid, and for generating synthetic test data.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np


class EllipsoidParameters(NamedTuple):
    """Geometric parameters of a fitted ellipsoid.

    Attributes
    ----------
    center : ndarray, shape (3,)
        Centre of the ellipsoid (x₀, y₀, z₀).
    radii : ndarray, shape (3,)
        Semi-axis lengths (a, b, c) in descending order.
    rotation : ndarray, shape (3, 3)
        Rotation matrix whose columns are the unit eigenvectors of the
        ellipsoid's shape matrix (principal axes).
    algebraic : ndarray, shape (10,)
        Raw algebraic coefficient vector
        [a, b, c, f, g, h, p, q, r, d].
    """

    center: np.ndarray
    radii: np.ndarray
    rotation: np.ndarray
    algebraic: np.ndarray

    def __repr__(self) -> str:
        c = np.round(self.center, 4)
        r = np.round(self.radii, 4)
        return (
            f"EllipsoidParameters(\n"
            f"  center  = {c},\n"
            f"  radii   = {r},\n"
            f"  rotation=\n{np.round(self.rotation, 4)}\n)"
        )


def algebraic_to_geometric(v: np.ndarray) -> EllipsoidParameters:
    """Convert a 10-element algebraic coefficient vector to geometric form.

    The algebraic form of a general quadric is::

        F(x,y,z) = ax² + by² + cz²
                   + 2fyz + 2gxz + 2hxy
                   + 2px  + 2qy  + 2rz  + d = 0

    with coefficient vector v = [a, b, c, f, g, h, p, q, r, d].

    Parameters
    ----------
    v : array_like, shape (10,)
        Algebraic coefficient vector.

    Returns
    -------
    EllipsoidParameters

    Raises
    ------
    ValueError
        If the algebraic form does not describe a real ellipsoid.
    """
    v = np.asarray(v, dtype=float)
    a, b, c, f, g, h, p, q, r, d = v

    # Build the 4×4 general quadric matrix (homogeneous form)
    M = np.array([
        [a, h, g, p],
        [h, b, f, q],
        [g, f, c, r],
        [p, q, r, d],
    ])

    # 3×3 sub-matrix of quadratic terms
    M33 = M[:3, :3]

    # Centre: solve M33 · centre = -[p, q, r]
    center = np.linalg.solve(M33, -np.array([p, q, r]))

    # Value of the quadric at the centre
    val_at_centre = M[3, 3] + p * center[0] + q * center[1] + r * center[2]

    # Semi-axes come from eigenvalues of M33 / (-val_at_centre)
    if abs(val_at_centre) < 1e-15:
        raise ValueError("Degenerate ellipsoid: value at centre is zero.")

    eigenvalues, eigenvectors = np.linalg.eigh(M33)

    # For a real ellipsoid every eigenvalue of M33 must have the same sign
    # as -val_at_centre.
    scale = -val_at_centre
    scaled_eigs = eigenvalues / scale
    if np.any(scaled_eigs <= 0):
        raise ValueError(
            "Algebraic coefficients do not describe a real ellipsoid "
            "(some semi-axes would be imaginary)."
        )

    radii = 1.0 / np.sqrt(scaled_eigs)

    # Sort radii descending for a canonical representation
    order = np.argsort(radii)[::-1]
    radii = radii[order]
    rotation = eigenvectors[:, order]

    return EllipsoidParameters(
        center=center,
        radii=radii,
        rotation=rotation,
        algebraic=v,
    )


def generate_ellipsoid_points(
    center: np.ndarray,
    radii: np.ndarray,
    rotation: np.ndarray | None = None,
    n_points: int = 500,
    noise_std: float = 0.0,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Generate random 3D points on the surface of an ellipsoid.

    Parameters
    ----------
    center : array_like, shape (3,)
        Centre of the ellipsoid.
    radii : array_like, shape (3,)
        Semi-axis lengths (a, b, c).
    rotation : array_like, shape (3, 3), optional
        Rotation matrix for axis orientation.  Defaults to identity.
    n_points : int
        Number of surface points to generate.
    noise_std : float
        Standard deviation of Gaussian noise added to each coordinate.
    rng : numpy.random.Generator, optional
        Random number generator for reproducibility.

    Returns
    -------
    ndarray, shape (n_points, 3)
        Noisy surface points.

    Examples
    --------
    >>> pts = generate_ellipsoid_points([0, 0, 0], [3, 2, 1], n_points=1000,
    ...                                 noise_std=0.05, rng=np.random.default_rng(42))
    """
    if rng is None:
        rng = np.random.default_rng()

    center = np.asarray(center, dtype=float)
    radii = np.asarray(radii, dtype=float)
    if rotation is None:
        rotation = np.eye(3)
    rotation = np.asarray(rotation, dtype=float)

    # Uniform sampling on a sphere then scale
    phi = rng.uniform(0.0, 2 * np.pi, n_points)
    cos_theta = rng.uniform(-1.0, 1.0, n_points)
    sin_theta = np.sqrt(1.0 - cos_theta ** 2)

    x = radii[0] * sin_theta * np.cos(phi)
    y = radii[1] * sin_theta * np.sin(phi)
    z = radii[2] * cos_theta

    pts = np.column_stack([x, y, z]) @ rotation.T + center

    if noise_std > 0.0:
        pts += rng.normal(0.0, noise_std, pts.shape)

    return pts


def load_point_cloud(filepath: str) -> np.ndarray:
    """Load a point cloud from a CSV or space-delimited text file.

    The file must contain at least 3 columns (x, y, z).  Comment lines
    starting with ``#`` are ignored.

    Parameters
    ----------
    filepath : str or path-like
        Path to the file.

    Returns
    -------
    ndarray, shape (N, 3)
    """
    return np.loadtxt(filepath, comments="#", usecols=(0, 1, 2))
