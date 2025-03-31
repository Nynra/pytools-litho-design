"""Single nanowire constriction."""

# from phidl import Device

# import phidl.geometry as pg
from typing import Tuple, Optional, Union

# from qnngds.utilities import PadPlacement, QnnDevice, WireBond, MultiProbeTip
import gdsfactory as gf


@gf.cell
def spot_wire(
    channel_w: float = 0.1,
    source_w: float = 0.3,
    layer: int = 1,
    num_pts: int = 100,
) -> gf.Component:
    """Creates a single wire, made of two optimal steps from channel_w to
    source_w.

    Args:
        channel_w (int or float): The width of the channel (at the hot-spot location).
        source_w (int or float): The width of the nanowire's "source".
        layer (int): The layer where to put the device.
        num_pts (int): The number of points comprising the optimal_steps geometries.

    Returns:
        Device: A device containing 2 optimal steps joined at their channel_w end.
    """
    NANOWIRE = gf.Component()
    # wire = pg.optimal_step(
    #     channel_w, source_w, symmetric=True, num_pts=num_pts, layer=layer
    # )
    wire = gf.components.optimal_step(
        start_width=channel_w,
        end_width=source_w,
        num_pts=num_pts,
        symmetric=True,
        layer=layer,
    )
    source = NANOWIRE << wire
    gnd = NANOWIRE << wire
    source.connect(source.ports[0], gnd.ports[0])

    NANOWIRE.add_port(name="1", port=source.ports[1])
    NANOWIRE.add_port(name="2", port=gnd.ports[1])

    final_NANOWIRE = gf.Component()
    final_NANOWIRE << NANOWIRE
    for port in NANOWIRE.get_ports_list():
        final_NANOWIRE.add_port(name=port.name, port=port)
    return final_NANOWIRE


def variable_length_wire(
    channel_w: float = 0.1,
    source_w: float = 0.3,
    channel_l: float = 1,
    two_point_probe: bool = False,
    four_point_probe: bool = False,
    layer: int = 1,
    num_pts: int = 100,
) -> gf.Component:
    """Creates a single wire, made of two optimal steps

    Creates a single nanowire, made of two optimal steps from channel_w to
    source_w with a constriction of the chosen length in the middle.

    Parameters
    ----------
    channel_w : float, optional
        The width of the channel (at the hot-spot location), by default 0.1
    source_w : float, optional
        The width of the nanowire's "source", by default 0.3
    constr_length : float, optional
        The length of the interior constriction, by default 1
    two_point_probe : bool, optional
        Whether to create pads for four-point-probe configuration, by default False
    four_point_probe : bool, optional
        Whether to create pads for two-point-probe configuration, by default False
    layer : int, optional
        The layer where to put the device, by default 1
    num_pts : int, optional
        The number of points comprising the optimal_steps geometries, by default 100

    Returns
    -------
    gf.Component
        A device containing 2 optimal steps joined at their channel_w end.
    """
    NANOWIRE = gf.Component()
    # wire = pg.optimal_step(
    #     channel_w, source_w, symmetric=True, num_pts=num_pts, layer=layer
    # )
    wire = gf.components.optimal_step(
        start_width=channel_w,
        end_width=source_w,
        num_pts=num_pts,
        symmetric=True,
        layer=layer,
    )
    # line = pg.rectangle((constr_length, channel_w), layer=layer)
    LINE = gf.Component()
    line = LINE << gf.components.rectangle(size=(channel_l, channel_w), layer=layer)
    line.center = [0, 0]
    LINE.add_port(
        "top",
        center=(-channel_l / 2, 0),
        orientation=180,
        width=channel_w,
        layer=layer,
    )
    LINE.add_port(
        "bottom",
        center=(channel_l / 2, 0),
        orientation=0,
        width=channel_w,
        layer=layer,
    )

    source = NANOWIRE << wire
    constriction = NANOWIRE << LINE
    gnd = NANOWIRE << wire
    source.connect(source.ports[0], constriction.ports["top"])
    gnd.connect(gnd.ports[0], constriction.ports["bottom"])

    NANOWIRE.add_port(name="constriction_top", port=constriction.ports["top"])
    NANOWIRE.add_port(name="constriction_bottom", port=constriction.ports["bottom"])
    NANOWIRE.add_port(name="source", port=source.ports[1])
    NANOWIRE.add_port(name="gnd", port=gnd.ports[1])

    if four_point_probe:
        # Add probes for four-point-probe
        add_probe(
            device=NANOWIRE,
            probe_port="constriction_top",
            probe_name="source_probe1",
            rotation=45,
            probe_width=source_w,
        )
        add_probe(
            device=NANOWIRE,
            probe_port="constriction_top",
            probe_name="source_probe2",
            rotation=-45,
            probe_width=source_w,
        )
        add_probe(
            device=NANOWIRE,
            probe_port="constriction_bottom",
            probe_name="gnd_probe1",
            rotation=45,
            probe_width=source_w,
        )
        add_probe(
            device=NANOWIRE,
            probe_port="constriction_bottom",
            probe_name="gnd_probe2",
            rotation=-45,
            probe_width=source_w,
        )
    elif two_point_probe:
        # Add probes for two-point-probe
        add_probe(
            device=NANOWIRE,
            probe_port="constriction_top",
            probe_name="top_probe",
            rotation=90,
            probe_width=source_w,
        )
        add_probe(
            device=NANOWIRE,
            probe_port="constriction_bottom",
            probe_name="bottom_probe",
            rotation=90,
            probe_width=source_w,
        )

    NANOWIRE.flatten()
    NANOWIRE.name = f"NANOWIRE.VAR(w={channel_w:.2f} l={channel_l:.1f})"
    return NANOWIRE


def add_probe(
    device: gf.Component,
    probe_port: str,
    probe_name: str,
    probe_width: float = 0.1,
    layer: int = 1,
    rotation: float = 0,
    **kwargs,
) -> gf.Component:
    """Add a probe to a device.

    Parameters
    ----------
    device : gf.Component
        The device to add the probe to.
    probe_port : str
        The port to add the probe to.
    probe_name : str
        The name of the probe port.
    probe_width : float, optional
        The width of the probe, by default 0.1
    layer : int, optional
        The layer to draw the probe on, by default 1
    rotation : float, optional
        The rotation of the probe, by default 0

    Returns
    -------
    gf.Component
        The device with the probe added.
    """
    wire = gf.components.optimal_step(
        start_width=device.ports[probe_port].width,
        end_width=probe_width,
        num_pts=100,
        symmetric=True,
        layer=layer,
    )
    probe = device << wire
    probe.connect(probe.ports[0], device.ports[probe_port])
    if rotation:
        probe.rotate(rotation, device.ports[probe_port].center)
    device.add_port(name=probe_name, port=probe.ports[1])
    return device
