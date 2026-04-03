"""Tests for ellipsoid_fitting.fit and ellipsoid_fitting.utils."""

import sys
import os

import numpy as np
import pytest

# Allow importing from src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ellipsoid_fitting.fit import fit_ellipsoid
from ellipsoid_fitting.utils import (
    EllipsoidParameters,
    algebraic_to_geometric,
    generate_ellipsoid_points,
)


RNG = np.random.default_rng(0)


def _make_points(center, radii, rotation=None, n=600, noise=0.02):
    return generate_ellipsoid_points(
        center, radii, rotation=rotation, n_points=n, noise_std=noise, rng=RNG
    )


class TestFitEllipsoid:
    def test_unit_sphere(self):
        pts = _make_points([0, 0, 0], [1, 1, 1], noise=0.01)
        p = fit_ellipsoid(pts)
        np.testing.assert_allclose(p.center, [0, 0, 0], atol=0.05)
        np.testing.assert_allclose(sorted(p.radii, reverse=True),
                                   [1, 1, 1], atol=0.05)

    def test_axis_aligned_ellipsoid(self):
        pts = _make_points([0, 0, 0], [3, 2, 1], noise=0.03)
        p = fit_ellipsoid(pts)
        np.testing.assert_allclose(p.center, [0, 0, 0], atol=0.1)
        np.testing.assert_allclose(sorted(p.radii, reverse=True),
                                   [3, 2, 1], atol=0.1)

    def test_offset_center(self):
        pts = _make_points([5, -3, 2], [4, 2.5, 1.5], noise=0.05)
        p = fit_ellipsoid(pts)
        np.testing.assert_allclose(p.center, [5, -3, 2], atol=0.15)

    def test_prolate_spheroid(self):
        pts = _make_points([0, 0, 0], [1, 1, 5], noise=0.03)
        p = fit_ellipsoid(pts)
        np.testing.assert_allclose(np.max(p.radii), 5, atol=0.15)

    def test_oblate_spheroid(self):
        pts = _make_points([0, 0, 0], [4, 4, 1], noise=0.03)
        p = fit_ellipsoid(pts)
        np.testing.assert_allclose(np.max(p.radii), 4, atol=0.15)

    def test_rotated_ellipsoid(self):
        angle = np.deg2rad(30)
        R = np.array([[np.cos(angle), -np.sin(angle), 0],
                      [np.sin(angle),  np.cos(angle), 0],
                      [0, 0, 1]])
        pts = _make_points([0, 0, 0], [3, 2, 1], rotation=R, noise=0.03)
        p = fit_ellipsoid(pts)
        np.testing.assert_allclose(sorted(p.radii, reverse=True),
                                   [3, 2, 1], atol=0.15)

    def test_returns_ellipsoid_parameters(self):
        pts = _make_points([0, 0, 0], [2, 1.5, 1])
        result = fit_ellipsoid(pts)
        assert isinstance(result, EllipsoidParameters)
        assert result.center.shape == (3,)
        assert result.radii.shape == (3,)
        assert result.rotation.shape == (3, 3)
        assert result.algebraic.shape == (10,)

    def test_radii_positive(self):
        pts = _make_points([1, 2, 3], [3, 2, 1])
        p = fit_ellipsoid(pts)
        assert np.all(p.radii > 0)

    def test_rotation_orthonormal(self):
        pts = _make_points([0, 0, 0], [3, 2, 1])
        p = fit_ellipsoid(pts)
        np.testing.assert_allclose(p.rotation @ p.rotation.T, np.eye(3),
                                   atol=1e-10)

    def test_too_few_points(self):
        with pytest.raises(ValueError, match="9 points"):
            fit_ellipsoid(np.random.rand(5, 3))

    def test_wrong_shape(self):
        with pytest.raises(ValueError):
            fit_ellipsoid(np.random.rand(20, 2))


class TestAlgebraicToGeometric:
    def test_round_trip_unit_sphere(self):
        # Unit sphere: x²+y²+z²-1=0 → v=[1,1,1,0,0,0,0,0,0,-1]
        v = np.array([1.0, 1.0, 1.0, 0, 0, 0, 0, 0, 0, -1.0])
        p = algebraic_to_geometric(v)
        np.testing.assert_allclose(p.center, [0, 0, 0], atol=1e-10)
        np.testing.assert_allclose(p.radii, [1, 1, 1], atol=1e-10)

    def test_scaled_sphere(self):
        # 4x²+4y²+4z²-4=0 → same sphere
        v = np.array([4.0, 4.0, 4.0, 0, 0, 0, 0, 0, 0, -4.0])
        p = algebraic_to_geometric(v)
        np.testing.assert_allclose(p.radii, [1, 1, 1], atol=1e-10)


class TestGenerateEllipsoidPoints:
    def test_shape(self):
        pts = generate_ellipsoid_points([0, 0, 0], [1, 1, 1], n_points=300)
        assert pts.shape == (300, 3)

    def test_approximate_surface_distance(self):
        radii = np.array([3.0, 2.0, 1.0])
        pts = generate_ellipsoid_points([0, 0, 0], radii, n_points=500,
                                        noise_std=0.0,
                                        rng=np.random.default_rng(1))
        # Points should satisfy ellipsoid equation ≈ 1
        surface_val = (pts[:, 0] / radii[0])**2 + \
                      (pts[:, 1] / radii[1])**2 + \
                      (pts[:, 2] / radii[2])**2
        np.testing.assert_allclose(surface_val, 1.0, atol=1e-10)
