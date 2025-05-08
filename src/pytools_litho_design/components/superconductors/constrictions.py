"""Single nanowire constriction."""

# from phidl import Device

# import phidl.geometry as pg
from typing import Tuple, Optional, Union

# from qnngds.utilities import PadPlacement, QnnDevice, WireBond, MultiProbeTip
import gdsfactory as gf
from .optimal_steps import optimal_step
from ..geometries import rectangle


@gf.cell
def spot_constriction(
    channel_w: float = 0.1,
    cross_section: Union[str, gf.CrossSection] = "nbtin",
    anticrowding_factor: float = 1.2,
    num_pts: int = 500,
) -> gf.Component:
    """Creates a single wire, made of two optimal steps from channel_w to
    source_w.

    Parameters
    ----------
    channel_w : float, optional
        The width of the channel (at the hot-spot location), by default 0.1
    cross_section : Union[str, gf.CrossSection], optional
        The cross-section of the wire, by default "nbtin"
    anticrowding_factor : float, optional
        The factor by which to increase the length of the constriction, by default 1.2
    num_pts : int, optional
        The number of points comprising the optimal_steps geometries, by default 100

    Returns
    -------
    gf.Component
        A device containing 2 optimal steps joined at their channel_w end.
    """
    if isinstance(cross_section, str):
        cross_section = gf.get_cross_section(cross_section)
    NANOWIRE = gf.Component()
    # wire = pg.optimal_step(
    #     channel_w, source_w, symmetric=True, num_pts=num_pts, layer=layer
    # )
    WIRE = optimal_step(
        end_width=channel_w,
        num_pts=num_pts,
        symmetric=True,
        anticrowding_factor=anticrowding_factor,
        cross_section=cross_section,
        port_type="electrical",
    )
    source = NANOWIRE << WIRE
    gnd = NANOWIRE << WIRE
    source.connect(source.ports[0], gnd.ports[0])

    NANOWIRE.add_port(name="e1", port=source.ports[1])
    NANOWIRE.add_port(name="e2", port=gnd.ports[1])

    final_NANOWIRE = gf.Component()
    final_NANOWIRE << NANOWIRE
    for port in NANOWIRE.get_ports_list():
        final_NANOWIRE.add_port(name=port.name, port=port)
    return final_NANOWIRE


@gf.cell
def variable_length_constriction(
    channel_w: float = 0.1,
    channel_l: float = 1,
    cross_section: Union[str, gf.CrossSection] = "nbtin",
    anticrowding_factor: float = 1.2,
    num_pts: int = 500,
) -> gf.Component:
    """Creates a single wire, made of two optimal steps"""
    if isinstance(cross_section, str):
        cross_section = gf.get_cross_section(cross_section)
    NANOWIRE = gf.Component()
    # wire = pg.optimal_step(
    #     channel_w, source_w, symmetric=True, num_pts=num_pts, layer=layer
    # )
    WIRE = optimal_step(
        end_width=channel_w,
        num_pts=num_pts,
        symmetric=True,
        anticrowding_factor=anticrowding_factor,
        cross_section=cross_section,
        port_type="electrical",
    )
    gf.components.rectangle
    LINE = rectangle(
        size=(channel_w, channel_l),
        layer=cross_section.layer,
    )
    source = NANOWIRE << WIRE
    gnd = NANOWIRE << WIRE
    line = NANOWIRE << LINE

    source.connect("e1", line.ports["e2"])
    gnd.connect("e1", line.ports["e4"])

    NANOWIRE.add_port(name="e1", port=source.ports[1])
    NANOWIRE.add_port(name="e2", port=gnd.ports[1])

    final_NANOWIRE = gf.Component()
    final_NANOWIRE << NANOWIRE
    for port in NANOWIRE.get_ports_list():
        final_NANOWIRE.add_port(name=port.name, port=port)
    final_NANOWIRE.rotate(90)
    return final_NANOWIRE


# @gf.cell
# def rectangle_meander_constriction(
#     num_of_boxes=23,
#     # width=0.5,
#     length=20,
#     cross_section="nbtin",
#     # bending_radius=0.5,
#     # insulator_width=0.75,
#     # wire_width=5,
#     # write_on_layer=2,
# ):
#     if isinstance(cross_section, str):
#         cross_section = gf.get_cross_section(cross_section)

#     MEANDER = gf.Component()

#     # Initialize a list to store the devices that will become the "ports" of the meander
#     boxes = []
#     BOX = gf.components.compass(
#         size=[length, cross_section.width], layer=cross_section.layer
#     )
#     for i in range(num_of_boxes):  # We need 25 boxes to create 24 turns
#         # Create and place the box
#         box = MEANDER << BOX
#         box.move(
#             [
#                 0,
#                 i
#                 * (
#                     cross_section.width
#                     + (cross_section.bbox_offsets if cross_section.bbox_offsets else 0)
#                 ),
#             ]
#         )

#         # Add the boxes to the list
#         boxes.append(box)

#     # Now create the connecting paths
#     for i in range(0, len(boxes) - 1, 2):  # Skip every second box
#         # I1 = pr.route_smooth(
#         #     port1=boxes[i].ports["E"],
#         #     port2=boxes[i + 1].ports["E"],
#         #     radius=bending_radius,
#         #     width=width,
#         #     path_type="manhattan",
#         #     manual_path=None,
#         #     smooth_options={"corner_fun": pp.euler, "use_eff": True},
#         #     layer=write_on_layer,
#         # )
#         gf.routing.route_single(
#             component=MEANDER,
#             port1=boxes[i].ports["e2"],
#             port2=boxes[i + 1].ports["e2"],
#             cross_section=cross_section,
#             bend=gf.components.bend_euler(cross_section=cross_section),
#         )

#         # I2 = pr.route_smooth(
#         #     port1=boxes[i + 1].ports["W"],
#         #     port2=boxes[i + 2].ports["W"],
#         #     radius=bending_radius,
#         #     width=width,
#         #     path_type="manhattan",
#         #     manual_path=None,
#         #     smooth_options={"corner_fun": pp.euler, "use_eff": True},
#         #     layer=write_on_layer,
#         # )
#         gf.routing.route_single(
#             component=MEANDER,
#             port1=boxes[i + 1].ports["e4"],
#             port2=boxes[i + 2].ports["e4"],
#             cross_section=cross_section,
#             bend=gf.components.bend_euler(cross_section=cross_section),
#         )

#         # meander.add_ref([I1, I2])

#     MEANDER.add_port(
#         name="e1",
#         center=[
#             length / 2,
#             (
#                 (num_of_boxes - 1) * cross_section.width
#                 + (num_of_boxes - 1)
#                 * (cross_section.bbox_offsets if cross_section.bbox_offsets else 0)
#             ),
#         ],
#         cross_section=cross_section,
#         orientation=0,
#     )
#     MEANDER.add_port(
#         name="e2", center=[length / -2, 0], cross_section=cross_section, orientation=180
#     )
#     MEANDER.rotate(-90, center=(0, 0))

#     # Create the input taper
#     # taper_device_in = Device("taper_in")
#     # taper_geometry_in = pg.taper(
#     #     width1=wire_width, width2=width, length=2 * wire_width, layer=write_on_layer
#     # )
#     # taper_in_ref = taper_device_in.add_ref(taper_geometry_in)
#     # taper_device_in.add_port(
#     #     name="input", midpoint=[0, 0], width=wire_width, orientation=180
#     # )
#     # taper_device_in.add_port(
#     #     name="output", midpoint=[2 * wire_width, 0], width=width, orientation=0
#     # )

#     # Create the output taper
#     # taper_device_out = Device("taper_out")
#     # taper_geometry_out = pg.taper(
#     #     width1=wire_width, width2=width, length=2 * wire_width, layer=write_on_layer
#     # )
#     # taper_out_ref = taper_device_out.add_ref(taper_geometry_out)
#     # taper_device_out.add_port(
#     #     name="input", midpoint=[0, 0], width=wire_width, orientation=180
#     # )
#     # taper_device_out.add_port(
#     #     name="output", midpoint=[2 * wire_width, 0], width=width, orientation=0
#     # )

#     # Connect the input taper to the meander
#     # taper_in_ref = meander << taper_device_in
#     # taper_in_ref.connect(port="output", destination=meander.ports["IN2"])

#     # # Connect the output taper to the meander
#     # taper_out_ref = meander << taper_device_out
#     # taper_out_ref.connect(port="output", destination=meander.ports["IN1"])

#     # Add ports to the main device meander
#     # meander.add_port(name="input", port=taper_in_ref.ports["input"])
#     # meander.add_port(name="output", port=taper_out_ref.ports["input"])

#     return MEANDER


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
