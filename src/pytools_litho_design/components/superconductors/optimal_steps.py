from __future__ import annotations

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec
from typing import Union


@gf.cell
def optimal_step(
    end_width: float = 22,
    cross_section: str = "strip",
    num_pts: int = 100,
    width_tol: float = 1e-3,
    anticrowding_factor: float = 1.2,
    symmetric: bool = False,
    port_type: str = "electrical",
) -> Component:
    """Returns an optimally-rounded step geometry.

    .. note::

        This function is a copy of the original in gdsfactory but with electrical
        ports instead of optical ports. The original function is located in
        gdsfactory.components.superconductors.optimal_step


    based on phidl.geometry
    Optimal structure from https://doi.org/10.1103/PhysRevB.84.174510
    Clem, J., & Berggren, K. (2011). Geometry-dependent critical currents in
    superconducting nanocircuits. Physical Review B, 84(17), 1-27.
    """
    if isinstance(cross_section, str):
        cross_section = gf.get_cross_section(cross_section)
    start_width = cross_section.width

    def step_points(eta: float, W: complex, a: complex) -> tuple[float, float]:
        """Returns step points.

        Returns points from a unit semicircle in the w (= u + iv) plane to
        the optimal curve in the zeta (= x + iy) plane which transitions
        a wire from a width of 'W' to a width of 'a'
        eta takes value 0 to pi
        """
        gamma = (a**2 + W**2) / (a**2 - W**2)
        w = np.exp(1j * eta)
        zeta = (
            4
            * 1j
            / np.pi
            * (
                W * np.arctan(np.sqrt((w - gamma) / (gamma + 1)))
                + a * np.arctan(np.sqrt((gamma - 1) / (w - gamma)))
            )
        )
        return np.real(zeta), np.imag(zeta)

    def invert_step_point(
        x_desired: float = -10,
        y_desired: float | None = None,
        W: float = 1,
        a: float = 2,
    ) -> tuple[float, float]:
        """Finds the eta associated with x_desired or y_desired along the optimal curve."""

        def fh(eta: float) -> float:
            guessed_x, guessed_y = step_points(eta, W=W + 0j, a=a + 0j)
            if y_desired is None:
                return (guessed_x - x_desired) ** 2  # Error relative to x_desired
            return (guessed_y - y_desired) ** 2  # Error relative to y_desired

        from scipy.optimize import fminbound

        # Minimize error to find optimal eta
        found_eta = fminbound(fh, 0, np.pi)
        return step_points(found_eta, W=W + 0j, a=a + 0j)

    if start_width > end_width:
        reverse = True
        start_width, end_width = end_width, start_width
    else:
        reverse = False

    D = Component()
    xpts: list[float] = []
    ypts: list[float] = []
    if start_width == end_width:  # Just return a square
        if symmetric:
            ypts = [
                -start_width / 2,
                start_width / 2,
                start_width / 2,
                -start_width / 2,
            ]
            xpts = [0, 0, start_width, start_width]
        if not symmetric:
            ypts = [0, start_width, start_width, 0]
            xpts = [0, 0, start_width, start_width]
        D.info["num_squares"] = 1
    else:
        xmin, _ = invert_step_point(
            y_desired=start_width * (1 + width_tol), W=start_width, a=end_width
        )
        xmax, _ = invert_step_point(
            y_desired=end_width * (1 - width_tol), W=start_width, a=end_width
        )

        xpts = list(np.linspace(xmin, xmax, num_pts))
        for x in xpts:
            x, y = invert_step_point(x_desired=x, W=start_width, a=end_width)
            ypts.append(y)

        ypts[-1] = end_width
        ypts[0] = start_width
        y_num_sq = np.array(ypts)
        x_num_sq = np.array(xpts)

        if not symmetric:
            xpts.append(xpts[-1])
            ypts.append(0)
            xpts.append(xpts[0])
            ypts.append(0)
        else:
            xpts += list(xpts[::-1])
            ypts += [-y for y in ypts[::-1]]
            xpts = [x / 2 for x in xpts]
            ypts = [y / 2 for y in ypts]

        # anticrowding_factor stretches the wire out; a stretched wire is a
        # gentler transition, so there's less chance of current crowding if
        # the fabrication isn't perfect but as a result, the wire isn't as
        # short as it could be
        xpts = [x * anticrowding_factor for x in xpts]

        if reverse:
            xpts = [-x for x in xpts]
            start_width, end_width = end_width, start_width

        D.info["num_squares"] = float(
            np.round(
                np.sum(np.diff(x_num_sq) / ((y_num_sq[:-1] + y_num_sq[1:]) / 2)), 3
            )
        )

    D.add_polygon(list(zip(xpts, ypts)), layer=cross_section.layer)
    if not symmetric:
        if port_type == "electrical":
            D.add_port(
                name="e1",
                center=(max(xpts), end_width / 2),
                width=end_width,
                orientation=0,
                port_type="electrical",
                cross_section=cross_section,
            )
            D.add_port(
                name="e2",
                center=(min(xpts), cross_section.width / 2),
                # width=cross_section.width,
                orientation=180,
                port_type="electrical",
                cross_section=cross_section,
            )
        if port_type == "optical":
            D.add_port(
                name="o1",
                center=(max(xpts), end_width / 2),
                width=end_width,
                orientation=0,
                cross_section=cross_section,
            )
            D.add_port(
                name="o2",
                center=(min(xpts), cross_section.width / 2),
                # width=cross_section.width,
                orientation=180,
                cross_section=cross_section,
            )
    else:
        if port_type == "electrical":
            D.add_port(
                name="e1",
                center=(max(xpts), 0),
                width=end_width,
                orientation=0,
                port_type="electrical",
                cross_section=cross_section,
            )
            D.add_port(
                name="e2",
                center=(min(xpts), 0),
                orientation=180,
                port_type="electrical",
                cross_section=cross_section,
            )
        else:
            D.add_port(
                name="o1",
                center=(min(xpts), 0),
                orientation=180,
                cross_section=cross_section,
            )
            D.add_port(
                name="o2",
                center=(max(xpts), 0),
                orientation=0,
                cross_section=cross_section,
            )

    return D


if __name__ == "__main__":
    c = optimal_step(symmetric=True)
    c.show()
