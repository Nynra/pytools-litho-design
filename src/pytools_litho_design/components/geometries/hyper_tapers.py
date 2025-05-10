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


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Create and show the hyperbolic taper
    c = hyper_taper()
    c.plot()
    plt.show()
