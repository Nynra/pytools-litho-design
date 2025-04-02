"""Single nanowire constriction."""

# from phidl import Device

# import phidl.geometry as pg
from typing import Tuple, Optional, Union

# from qnngds.utilities import PadPlacement, QnnDevice, WireBond, MultiProbeTip
import gdsfactory as gf
from .optimal_step import optimal_step


@gf.cell
def spot_constriction(
    channel_w: float = 0.1,
    source_w: float = 0.3,
    anticrowding_factor: float = 1.2,
    two_point_probe: bool = False,
    four_point_probe: bool = False,
    layer: int = "NEG_NBTIN",
    num_pts: int = 100,
) -> gf.Component:
    """Creates a single wire, made of two optimal steps from channel_w to
    source_w.

    Parameters
    ----------
    channel_w : float, optional
        The width of the channel (at the hot-spot location), by default 0.1
    source_w : float, optional
        The width of the nanowire's "source", by default 0.3
    anticrowding_factor : float, optional
        The factor by which to increase the length of the constriction, by default 1.2
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
    WIRE = optimal_step(
        start_width=channel_w,
        end_width=source_w,
        num_pts=num_pts,
        symmetric=True,
        layer=layer,
        anticrowding_factor=anticrowding_factor,
    )
    source = NANOWIRE << WIRE
    gnd = NANOWIRE << WIRE
    source.connect(source.ports[0], gnd.ports[0])

    NANOWIRE.add_port(name="e1", port=source.ports[1])
    NANOWIRE.add_port(name="e2", port=gnd.ports[1])

    if four_point_probe:
        # Add probes for four-point-probe
        add_probe(
            device=NANOWIRE,
            probe_port="e1",
            probe_name="e3",
            rotation=45,
            probe_width=source_w,
        )
        add_probe(
            device=NANOWIRE,
            probe_port="e1",
            probe_name="e3",
            rotation=-45,
            probe_width=source_w,
        )
        add_probe(
            device=NANOWIRE,
            probe_port="e2",
            probe_name="e4",
            rotation=45,
            probe_width=source_w,
        )
        add_probe(
            device=NANOWIRE,
            probe_port="e2",
            probe_name="e5",
            rotation=-45,
            probe_width=source_w,
        )
    elif two_point_probe:
        # Add probes for two-point-probe
        add_probe(
            device=NANOWIRE,
            probe_port="e1",
            probe_name="e3",
            rotation=90,
            probe_width=source_w,
        )
        add_probe(
            device=NANOWIRE,
            probe_port="e2",
            probe_name="e4",
            rotation=90,
            probe_width=source_w,
        )

    # # Make sure the e ports are electrical
    # for port in NANOWIRE.ports:
    #     if port.name in ["e1", "e2"]:
    #         port.port_type = "electrical"

    final_NANOWIRE = gf.Component()
    final_NANOWIRE << NANOWIRE
    for port in NANOWIRE.get_ports_list():
        final_NANOWIRE.add_port(name=port.name, port=port)
    return final_NANOWIRE


@gf.cell
def variable_length_constriction(
    channel_w: float = 0.1,
    source_w: float = 0.3,
    channel_l: float = 1,
    anticrowding_factor: float = 1.2,
    two_point_probe: bool = False,
    four_point_probe: bool = False,
    layer: int = "NEG_NBTIN",
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
    channel_l : float, optional
        The length of the interior constriction, by default 1
    anticrowding_factor : float, optional
        The factor by which to increase the length of the constriction, by default 1.2
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
    WIRE = optimal_step(
        start_width=channel_w,
        end_width=source_w,
        num_pts=num_pts,
        symmetric=True,
        layer=layer,
        anticrowding_factor=anticrowding_factor,
    )
    # for port in WIRE.ports:
    #     # A hack but cant find a way to initate with elektrical ports....
    #     port.port_type = "electrical"

    # line = pg.rectangle((constr_length, channel_w), layer=layer)
    LINE = gf.Component()
    line = LINE << gf.components.rectangle(size=(channel_l, channel_w), layer=layer)
    line.center = [0, 0]
    LINE.add_port(
        "e1",
        center=(-channel_l / 2, 0),
        orientation=180,
        width=channel_w,
        layer=layer,
        port_type="electrical",
    )
    LINE.add_port(
        "e2",
        center=(channel_l / 2, 0),
        orientation=0,
        width=channel_w,
        layer=layer,
        port_type="electrical",
    )

    source = NANOWIRE << WIRE
    constriction = NANOWIRE << LINE
    gnd = NANOWIRE << WIRE
    source.connect(source.ports[0], constriction.ports["e1"])
    gnd.connect(gnd.ports[0], constriction.ports["e2"])

    NANOWIRE.add_port(name="ec1", port=constriction.ports["e1"])
    NANOWIRE.add_port(name="ec2", port=constriction.ports["e1"])
    NANOWIRE.add_port(name="e1", port=source.ports[1])
    NANOWIRE.add_port(name="e2", port=gnd.ports[1])

    if four_point_probe:
        # Add probes for four-point-probe
        add_probe(
            device=NANOWIRE,
            probe_port="ec1",
            probe_name="e3",
            rotation=45,
            probe_width=source_w,
        )
        add_probe(
            device=NANOWIRE,
            probe_port="ec1",
            probe_name="e3",
            rotation=-45,
            probe_width=source_w,
        )
        add_probe(
            device=NANOWIRE,
            probe_port="ec2",
            probe_name="e4",
            rotation=45,
            probe_width=source_w,
        )
        add_probe(
            device=NANOWIRE,
            probe_port="ec2",
            probe_name="e5",
            rotation=-45,
            probe_width=source_w,
        )
    elif two_point_probe:
        # Add probes for two-point-probe
        add_probe(
            device=NANOWIRE,
            probe_port="ec1",
            probe_name="e3",
            rotation=90,
            probe_width=source_w,
        )
        add_probe(
            device=NANOWIRE,
            probe_port="ec2",
            probe_name="e4",
            rotation=90,
            probe_width=source_w,
        )

    NANOWIRE.flatten()
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


# if __name__ == "__main__":
#     # Example usage
#     # c = spot_wire()
#     # c.show()
#     c = variable_length_constriction()
#     c.show()
