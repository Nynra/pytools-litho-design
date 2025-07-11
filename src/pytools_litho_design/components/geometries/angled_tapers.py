"""Geometries contains useful shapes/tools that are not available in phidl's
geometry library."""

import numpy as np
from typing import Tuple, List, Union, Optional
import gdsfactory as gf


@gf.cell
def hyper_taper(length=10, wide_section=50, narrow_section=5, layer=1) -> gf.Component:
    """Hyperbolic taper (solid). Designed by colang.

    See the original code at [qnngds](https://github.com/qnngroup/qnngds/tree/master?tab=readme-ov-file).
    The code was modified to use gdsfactory.

    Parameters
    ----------
    length: int or float
        Length of taper.
    wide_section: int or float
        Wide width dimension.
    narrow_section: int or float
        Narrow width dimension.
    layer: int
        Layer for device to be created on.

    Returns
    -------
    Component
        The hyper taper.
    """

    taper_length = length
    wide = wide_section
    zero = 0
    narrow = narrow_section
    x_list = np.arange(0, taper_length + 0.1, 0.1)
    x_list2 = np.arange(taper_length, -0.1, -0.1)
    pts = []

    a = np.arccosh(wide / narrow) / taper_length

    for x in x_list:
        pts.append((x, np.cosh(a * x) * narrow / 2))
    for y in x_list2:
        pts.append((y, -np.cosh(a * y) * narrow / 2))
        HT = gf.Component()
        _ = HT.add_polygon(pts, layer=layer)
        HT.add_port(name="1", center=[0, 0], width=narrow, orientation=180, layer=layer)
        HT.add_port(
            name="2", center=[taper_length, 0], width=wide, orientation=0, layer=layer
        )
        HT.flatten()
    return HT


@gf.cell
def angled_taper(
    wire_width: Union[int, float] = 0.6,
    constr_width: Union[int, float] = 0.1,
    angle: Union[int, float] = 60,
    radius: Union[int, float] = 3,
    p=0.4,
) -> gf.Component:
    """Create an angled taper with euler curves

    See the original code at [qnngds](https://github.com/qnngroup/qnngds/tree/master?tab=readme-ov-file)
    The code was modified to use gdsfactory.

    Parameters
    ----------
    wire_width: int or float
        Width of wide end of taper
    constr_width: int or float
        Width of narrow end of taper
    angle: int or float
        Angle between taper ends in degrees
    radius: int or float
        Radius of curvature for the taper
    p: int or float
        The percentage of the curve that is a straight line

    Returns
    -------
    Components
        A gdsfactory Component containing a single taper
    """
    # Define the sections of the crossing (beginning and end)
    constr_sect = gf.get_cross_section("strip", width=constr_width)
    wire_sect = gf.get_cross_section("strip", width=wire_width)

    # Create the transition obj and the routing function (euler in this case)
    trans = gf.path.transition(constr_sect, wire_sect)
    euler_path = gf.path.euler(angle=angle, radius=radius, p=p)

    # Extrude the transition along the routing function to create the component
    taper = gf.path.extrude_transition(euler_path, trans)
    return taper


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Create and show the angled taper
    c = angled_taper()
    c.plot()
    plt.show()
