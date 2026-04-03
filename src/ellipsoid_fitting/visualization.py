"""
visualization.py
----------------
3D plotting helpers for inspecting ellipsoid fits.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 – registers 3D projection

from ellipsoid_fitting.utils import EllipsoidParameters


def plot_fit(
    points: np.ndarray,
    params: EllipsoidParameters,
    n_surface: int = 40,
    point_color: str = "steelblue",
    surface_color: str = "tomato",
    surface_alpha: float = 0.25,
    title: str = "Ellipsoid Fit",
    ax: "plt.Axes | None" = None,
    show: bool = True,
) -> plt.Axes:
    """Plot 3D point cloud and the fitted ellipsoid surface.

    Parameters
    ----------
    points : ndarray, shape (N, 3)
        Input point cloud.
    params : EllipsoidParameters
        Result from :func:`~ellipsoid_fitting.fit_ellipsoid`.
    n_surface : int
        Grid resolution for the ellipsoid surface mesh.
    point_color : str
        Matplotlib colour string for the scatter points.
    surface_color : str
        Matplotlib colour string for the ellipsoid surface.
    surface_alpha : float
        Transparency of the ellipsoid surface (0–1).
    title : str
        Plot title.
    ax : matplotlib Axes3D, optional
        Axes to draw into.  A new figure is created if not provided.
    show : bool
        If ``True``, call ``plt.show()`` at the end.

    Returns
    -------
    matplotlib Axes3D
    """
    if ax is None:
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection="3d")

    # Scatter plot of input points
    ax.scatter(
        points[:, 0], points[:, 1], points[:, 2],
        s=4, c=point_color, alpha=0.6, label="Input points",
    )

    # Build the ellipsoid surface mesh
    u = np.linspace(0, 2 * np.pi, n_surface)
    v = np.linspace(0, np.pi, n_surface)

    x = params.radii[0] * np.outer(np.cos(u), np.sin(v))
    y = params.radii[1] * np.outer(np.sin(u), np.sin(v))
    z = params.radii[2] * np.outer(np.ones_like(u), np.cos(v))

    # Rotate and translate
    shape = x.shape
    pts_flat = np.column_stack([x.ravel(), y.ravel(), z.ravel()])
    rotated = pts_flat @ params.rotation.T + params.center

    xs = rotated[:, 0].reshape(shape)
    ys = rotated[:, 1].reshape(shape)
    zs = rotated[:, 2].reshape(shape)

    ax.plot_surface(xs, ys, zs, color=surface_color, alpha=surface_alpha,
                    label="Fitted ellipsoid")

    # Mark the centre
    cx, cy, cz = params.center
    ax.scatter([cx], [cy], [cz], s=60, c="black", marker="+",
               zorder=5, label="Centre")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(title)
    ax.legend(loc="upper left", fontsize=8)

    if show:
        plt.tight_layout()
        plt.show()

    return ax
