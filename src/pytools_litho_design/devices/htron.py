"""
Heater cryotron devices `[1] <https://doi.org/10.1038/s41928-019-0300-8>`_, `[2] <https://doi.org/10.1103/PhysRevApplied.14.054011>`_.
Copied an modified from [qnngroup/qnngds](https://github.com/qnngroup/qnngds/blob/master/src/qnngds/devices/htron.py)
"""

import numpy as np

# from phidl import Device
# import phidl.geometry as pg
import gdsfactory as gf

# from qnngds.utilities import PadPlacement, QnnDevice
# from qnngds.geometries import angled_taper
from typing import Tuple, List, Union, Optional
from ..geometries import angled_taper


@gf.cell
def planar_hTron(
    wire_width: Union[int, float] = 0.3,
    gate_width: Union[int, float] = 0.1,
    channel_width: Union[int, float] = 0.2,
    gap: Union[int, float] = 0.02,
    channel_length: Union[int, float] = 0.01,
) -> gf.Component:
    """Create a planar hTron

    This is a crude example of a planar hTron to get the hang of how
    gdsfactory works, it is not recommended to actually use this device
    for any real applications.

    Parameters
    -----------------
    wire_width : int or float
        Width of routing wires in microns
    gate_width : int or float
        Width of superconducting gate in microns
    channel_width : int or float
        Width of superconducting channel in microns
    gap : int or float
        Spacing between gate and channel in microns
    gate_length : int or float
        Length of superconducting gate in microns
    channel_length : int or float
        Length of superconducting channel in microns
    layer: int
        Layer to draw device on

    Returns
    -------------
    HTRON : gf.Component
        A gdsfactory Component containing a single hTron

    """

    W = gf.Component()
    coupler = W << gf.components.coupler_straight_asymmetric(
        length=channel_length,
        gap=gap,
        width_top=channel_width,
        width_bot=gate_width,
        cross_section="strip",
    )
    # Add the channel tapers
    channel_left_taper = W << angled_taper(
        wire_width=wire_width,
        constr_width=channel_width,
        angle=45,
    )
    channel_left_taper.mirror_x()
    channel_left_taper.connect(channel_left_taper.ports[0], coupler.ports[1])
    channel_right_taper = W << angled_taper(
        wire_width=wire_width,
        constr_width=channel_width,
        angle=45,
    )
    channel_right_taper.connect(channel_right_taper.ports[0], coupler.ports[2])

    # Add the gate tapers
    gate_left_taper = W << angled_taper(
        wire_width=gate_width,
        constr_width=gate_width,
        angle=45,
    )
    gate_left_taper.connect(gate_left_taper.ports[0], coupler.ports[0])
    gate_right_taper = W << angled_taper(
        wire_width=gate_width,
        constr_width=gate_width,
        angle=45,
    )
    gate_right_taper.mirror_x()
    gate_right_taper.connect(gate_right_taper.ports[0], coupler.ports[3])

    # Add the ports to the device
    W.add_port(name="c1", port=channel_left_taper.ports[1])
    W.add_port(name="c2", port=channel_right_taper.ports[1])
    W.add_port(name="g1", port=gate_left_taper.ports[1])
    W.add_port(name="g2", port=gate_right_taper.ports[1])

    return W
