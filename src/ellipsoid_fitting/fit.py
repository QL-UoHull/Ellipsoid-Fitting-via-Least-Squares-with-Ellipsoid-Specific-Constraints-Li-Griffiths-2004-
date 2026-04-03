"""
fit.py
------
Core implementation of the Li–Griffiths least-squares ellipsoid-specific
fitting algorithm.

Reference
---------
Q. Li and J. G. Griffiths, "Least Squares Ellipsoid Specific Fitting,"
Proceedings of the Geometric Modeling and Processing, Beijing, China, 2004,
pp. 335-340, doi: 10.1109/GMAP.2004.1290055.

Algorithm summary
-----------------
Any quadric surface can be written as the algebraic form:

    F(x) = a·x² + b·y² + c·z² + 2f·yz + 2g·xz + 2h·xy
            + 2p·x + 2q·y + 2r·z + d = 0

where the coefficient vector is v = [a, b, c, f, g, h, p, q, r, d]ᵀ.

An ellipsoid-specific constraint derived by Li & Griffiths ensures the
fitted surface is always a real ellipsoid:

    κ = 4·a·c - g² + 4·b·c - f² + 4·a·b - h² > 0  (simplified form)

The algorithm solves a generalised eigenvalue problem S·v = λ·C·v where S is
the scatter matrix built from the data and C encodes the ellipsoid constraint.
"""

import numpy as np
from ellipsoid_fitting.utils import EllipsoidParameters, algebraic_to_geometric


def _build_design_row(x: float, y: float, z: float) -> np.ndarray:
    """Return the 10-element design-matrix row for point (x, y, z)."""
    return np.array([
        x * x, y * y, z * z,
        2 * y * z, 2 * x * z, 2 * x * y,
        2 * x, 2 * y, 2 * z,
        1.0,
    ])


def _build_constraint_matrix() -> np.ndarray:
    """
    Return the 10×10 constraint matrix C that encodes the ellipsoid-specific
    condition derived in Li & Griffiths (2004), Eq. (15).

    The constraint is κ = 4ac - g² + 4bc - f² + 4ab - h² > 0,
    written in quadratic form vᵀ C v > 0.
    """
    C = np.zeros((10, 10))
    # Indices: a=0, b=1, c=2, f=3, g=4, h=5, p=6, q=7, r=8, d=9
    C[0, 1] = C[1, 0] = 2.0   # 4ab term → 2 * e_0 e_1 coeff = 2
    C[0, 2] = C[2, 0] = 2.0   # 4ac
    C[1, 2] = C[2, 1] = 2.0   # 4bc
    C[3, 3] = -1.0             # -f²
    C[4, 4] = -1.0             # -g²
    C[5, 5] = -1.0             # -h²
    return C


def fit_ellipsoid(points: np.ndarray) -> EllipsoidParameters:
    """
    Fit an ellipsoid to a set of 3D points using the Li–Griffiths
    constrained least-squares method.

    Parameters
    ----------
    points : array_like, shape (N, 3)
        3D point cloud with N ≥ 9 points.  Columns are x, y, z.

    Returns
    -------
    EllipsoidParameters
        Named tuple containing the geometric parameters of the fitted
        ellipsoid: center, radii (semi-axes), and rotation matrix.

    Raises
    ------
    ValueError
        If fewer than 9 points are supplied or if no valid ellipsoid
        eigenvector is found (data cannot be fit by an ellipsoid).

    Examples
    --------
    >>> import numpy as np
    >>> from ellipsoid_fitting import fit_ellipsoid
    >>> rng = np.random.default_rng(0)
    >>> # Generate noisy points on a unit sphere
    >>> theta = rng.uniform(0, np.pi, 200)
    >>> phi   = rng.uniform(0, 2 * np.pi, 200)
    >>> pts = np.column_stack([np.sin(theta) * np.cos(phi),
    ...                        np.sin(theta) * np.sin(phi),
    ...                        np.cos(theta)])
    >>> params = fit_ellipsoid(pts + rng.normal(0, 0.02, pts.shape))
    >>> print(params.center)
    """
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points must be an (N, 3) array.")
    n = points.shape[0]
    if n < 9:
        raise ValueError(f"At least 9 points are required; got {n}.")

    # Build the N×10 design matrix D
    D = np.array([_build_design_row(x, y, z) for x, y, z in points])

    # Scatter matrix S = DᵀD
    S = D.T @ D

    # Constraint matrix C
    C = _build_constraint_matrix()

    # Solve the generalised eigenvalue problem S·v = λ·C·v
    # Only the upper-left 6×6 block of C is non-zero, so we use the
    # partitioned formulation from Li & Griffiths.
    S11 = S[:6, :6]
    S12 = S[:6, 6:]
    S21 = S[6:, :6]
    S22 = S[6:, 6:]
    C11 = C[:6, :6]

    # Eliminate the unconstrained part (Eq. 14 in Li & Griffiths)
    S22_inv = np.linalg.inv(S22)
    M = np.linalg.inv(C11) @ (S11 - S12 @ S22_inv @ S21)

    eigenvalues, eigenvectors = np.linalg.eig(M)

    # The valid solution is the eigenvector corresponding to the unique
    # positive eigenvalue (Li & Griffiths, Theorem 1)
    # We only consider real eigenvalues.
    eigenvalues = eigenvalues.real
    eigenvectors = eigenvectors.real

    positive_mask = eigenvalues > 0
    if not positive_mask.any():
        raise ValueError(
            "No positive eigenvalue found. The input data cannot be "
            "fitted by an ellipsoid. Try adding more points or ensuring "
            "the data approximates an ellipsoidal surface."
        )

    best_idx = np.argmax(eigenvalues * positive_mask - 1e18 * ~positive_mask)
    u1 = eigenvectors[:, best_idx]

    # Recover the full 10-vector
    u2 = -S22_inv @ S21 @ u1
    v = np.concatenate([u1, u2])

    return algebraic_to_geometric(v)
