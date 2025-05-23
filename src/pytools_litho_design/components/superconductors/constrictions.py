import gdsfactory as gf
from ..geometries import rectangle, taper_to_ridge


@gf.cell
def variable_length_constriction(
    channel_length: float = 1,
    channel_width: float = 0.1,
    fine_cross_section: str = "nbtin",
    coarse_cross_section: str = "course_nbtin",
) -> gf.Component:
    """Creates a single wire, made of two optimal steps"""
    fine_xs = gf.get_cross_section(fine_cross_section)
    coarse_xs = gf.get_cross_section(coarse_cross_section)
    NANOWIRE = gf.Component()
    WIRE = taper_to_ridge(
        length=3,
        width1=channel_width,
        width2=channel_width,
        slab_length=coarse_xs.width,
        w_slab2=coarse_xs.width,
        w_slab1=channel_width if channel_width > 2 else 2,
        port_type="electrical",
        main_cross_section=fine_cross_section,
        slab_cross_section=coarse_cross_section,
    )
    LINE = rectangle(
        size=(channel_width, channel_length),
        layer=fine_xs.layer,
    )
    source = NANOWIRE << WIRE
    gnd = NANOWIRE << WIRE
    line = NANOWIRE << LINE
    source.connect("e2", line.ports["e2"])
    gnd.connect("e2", line.ports["e4"])

    NANOWIRE.add_port(name="e1", port=source.ports[0])
    NANOWIRE.add_port(name="e2", port=gnd.ports[0])

    final_NANOWIRE = gf.Component()
    final_NANOWIRE << NANOWIRE
    for port in NANOWIRE.get_ports_list():
        final_NANOWIRE.add_port(name=port.name, port=port)
    final_NANOWIRE.rotate(90)
    return final_NANOWIRE


@gf.cell
def _round_hairpin(
    width,
    pitch,
    length,
    cross_section,
    npoints=300,
) -> gf.Component:
    """Creates a single wire, made of two optimal steps"""
    HAIRPIN = gf.Component()
    LINE = gf.components.straight(
        length=length / 2,
        width=width,
        cross_section=cross_section,
    )
    bend180 = HAIRPIN << gf.components.bend_circular(
        width=width,
        cross_section=cross_section,
        radius=pitch / 2,
        angle=180,
        allow_min_radius_violation=True,
        npoints=npoints,
    )
    line1 = HAIRPIN << LINE
    line2 = HAIRPIN << LINE
    line1.connect("e2", bend180.ports["e2"])
    line2.connect("e1", bend180.ports["e1"])
    HAIRPIN.add_port(name="e1", port=line1.ports["e1"])
    HAIRPIN.add_port(name="e2", port=line2.ports["e2"])
    HAIRPIN.draw_ports()
    HAIRPIN.show()
    return HAIRPIN


@gf.cell
def variable_length_hairpin_constriction(
    channel_length: float = 1,
    channel_width: float = 0.1,
    hairpin_pitch=0.3,
    add_choke: bool = False,
    choke_offset=2,
    choke_pitch=0.5,
    choke_cross_section="xs_nw300",
    fine_cross_section: str = "metal1",
    coarse_cross_section: str = "metal1",
    corner_type: str = "default",
) -> gf.Component:
    """Creates a single wire, made of two optimal steps"""
    fine_xs = gf.get_cross_section(fine_cross_section)
    coarse_xs = gf.get_cross_section(coarse_cross_section)
    choke_xs = gf.get_cross_section(choke_cross_section)
    NANOWIRE = gf.Component()
    WIRE = taper_to_ridge(
        length=3,
        width1=channel_width,
        width2=channel_width,
        slab_length=coarse_xs.width,
        w_slab2=coarse_xs.width,
        w_slab1=channel_width if channel_width > 2 else 2,
        port_type="electrical",
        main_cross_section=fine_cross_section,
        slab_cross_section=coarse_cross_section,
    )
    LINE = gf.Component()
    match corner_type:
        case "default":
            hairpin = LINE << gf.components.optimal_hairpin(
                width=channel_width,
                pitch=hairpin_pitch,
                length=channel_length / 2,
                layer=gf.get_cross_section(fine_cross_section).layer,
            )
        case "round":
            hairpin = LINE << _round_hairpin(
                width=channel_width,
                pitch=hairpin_pitch,
                length=channel_length,
                cross_section=fine_cross_section,
            )
        case _:
            raise ValueError(f"Unknown corner type: {corner_type}")

    deg90_bend1 = LINE << gf.components.bend_circular(
        cross_section=fine_cross_section,
        angle=90,
        width=channel_width,
        npoints=300,
    )
    deg90_bend2 = LINE << gf.components.bend_circular(
        cross_section=fine_cross_section,
        angle=90,
        width=channel_width,
        npoints=300,
    )
    deg90_bend1.mirror_y()
    deg90_bend1.connect("e2", hairpin.ports["e2"], allow_width_mismatch=True)
    deg90_bend2.connect("e2", hairpin.ports["e1"], allow_width_mismatch=True)

    # if add_choke:
    #     # Add the choke inductor
    #     choke_offset = LINE << gf.components.straight(
    #         cross_section=fine_xs, length=choke_offset
    #     )
    #     choke_offset.connect("e2", deg90_bend1.ports["e1"])
    #     deg90_bend3 = LINE << gf.components.bend_circular(
    #         cross_section=fine_xs,
    #         angle=90,
    #         width=channel_width,
    #         npoints=300,
    #     )
    #     deg90_bend3.mirror_y()
    #     deg90_bend3.connect("e2", choke_offset.ports["e1"])
    #     taper_bend3_to_choke = LINE << gf.components.tapers.taper_cross_section(
    #         length=choke_pitch,
    #         cross_section1=fine_xs,
    #         cross_section2=choke_xs,
    #     )
    #     taper_bend3_to_choke.connect("e1", deg90_bend3.ports["e1"])
    #     choke = LINE << gf.components.snspd(
    #         wire_width=choke_xs.width,
    #         wire_pitch=choke_pitch,
    #         layer=choke_xs.layer,
    #         terminals_same_side=True,
    #     )
    #     choke.connect("e1", taper_bend3_to_choke.ports["e2"])

    #     deg90_bend4 = LINE << gf.components.bend_circular(
    #         cross_section=fine_xs,
    #         angle=90,
    #         width=channel_width,
    #         npoints=300,
    #     )
    #     choke_to_bend4_taper = LINE << gf.components.tapers.taper_cross_section(
    #         length=choke_pitch,
    #         cross_section1=choke_xs,
    #         cross_section2=fine_xs,
    #     )
    #     choke_to_bend4_taper.connect("e1", choke.ports["e2"])
    #     deg90_bend4.connect("e1", choke_to_bend4_taper.ports["e2"])
    #     LINE.add_port(
    #         name="e1",
    #         port=deg90_bend2.ports["e1"],
    #     )
    #     LINE.add_port(
    #         name="e2",
    #         port=deg90_bend4.ports["e2"],
    #     )
    # else:
    LINE.add_port(
        name="e1",
        port=deg90_bend1.ports["e1"],
    )
    LINE.add_port(
        name="e2",
        port=deg90_bend2.ports["e1"],
    )

    source = NANOWIRE << WIRE
    gnd = NANOWIRE << WIRE
    line = NANOWIRE << LINE
    source.connect("e2", line.ports["e1"], allow_width_mismatch=True)
    gnd.connect("e2", line.ports["e2"], allow_width_mismatch=True)

    # NANOWIRE.flatten()
    NANOWIRE.add_port(name="e1", port=source.ports[0])
    NANOWIRE.add_port(name="e2", port=gnd.ports[0])
    return NANOWIRE


@gf.cell
def variable_length_meander_constriction(
    channel_width: float = 0.1,
    channel_pitch=0.5,
    size=(1, 1),
    fine_cross_section: str = "metal1",
    coarse_cross_section: str = "metal1",
) -> gf.Component:
    """Creates a single wire, made of two optimal steps"""
    fine_xs = gf.get_cross_section(fine_cross_section)
    coarse_xs = gf.get_cross_section(coarse_cross_section)
    NANOWIRE = gf.Component()
    WIRE = taper_to_ridge(
        length=3,
        width1=channel_width,
        width2=channel_width,
        slab_length=coarse_xs.width,
        w_slab2=coarse_xs.width,
        w_slab1=channel_width if channel_width > 2 else 2,
        port_type="electrical",
        main_cross_section=fine_cross_section,
        slab_cross_section=coarse_cross_section,
    )
    LINE = gf.Component()
    meander = LINE << gf.components.superconductors.snspd(
        wire_width=channel_width,
        wire_pitch=channel_pitch,
        layer=fine_xs.layer,
        size=size,
        terminals_same_side=True,
    )

    entrance_bend = LINE << gf.components.bend_circular(
        cross_section=fine_cross_section,
        angle=90,
        width=channel_width,
        radius=channel_pitch / 2,
        npoints=300,
        allow_min_radius_violation=True,
    )
    entrance_bend.mirror_y()
    entrance_bend.connect("e1", meander.ports["e1"], allow_width_mismatch=True)
    exit_bend = LINE << gf.components.bend_circular(
        cross_section=fine_cross_section,
        angle=90,
        width=channel_width,
        radius=channel_pitch / 2,
        npoints=300,
        allow_min_radius_violation=True,
    )
    exit_bend.connect("e1", meander.ports["e2"], allow_width_mismatch=True)
    LINE.add_port(
        name="e1",
        port=entrance_bend.ports["e2"],
    )
    LINE.add_port(
        name="e2",
        port=exit_bend.ports["e2"],
    )

    # Connect the tapers
    NANOWIRE << LINE
    taper1 = NANOWIRE << WIRE
    taper2 = NANOWIRE << WIRE
    taper1.connect("e2", LINE.ports["e1"], allow_width_mismatch=True)
    taper2.connect("e2", LINE.ports["e2"], allow_width_mismatch=True)
    NANOWIRE.add_port(name="e1", port=taper1.ports[0])
    NANOWIRE.add_port(name="e2", port=taper2.ports[0])
    return NANOWIRE


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


# if __name__ == "__main__":
#     # Example usage
#     # c = spot_wire()
#     # c.show()
#     c = variable_length_constriction()
#     c.show()
