import gdsfactory as gf
from ..geometries import rectangle, taper_to_ridge


@gf.cell
def variable_length_constriction(
    channel_length: float = 1,
    channel_width: float = 0.1,
    fine_cross_section: str = "nbtin",
    coarse_cross_section: str = "course_nbtin",
    taper_left: bool = True,
    taper_right: bool = True,
) -> gf.Component:
    """Creates a single wire, made of two optimal steps"""
    fine_xs = gf.get_cross_section(fine_cross_section)
    coarse_xs = gf.get_cross_section(coarse_cross_section)
    NANOWIRE = gf.Component()
    if taper_left or taper_right:
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

    # Add the tapers (or not)
    line = NANOWIRE << LINE
    if taper_left:
        source = NANOWIRE << WIRE
        source.connect("e2", line.ports["e2"])
        NANOWIRE.add_port(name="e1", port=source.ports[0])
    else:
        NANOWIRE.add_port(name="e1", port=LINE.ports["e1"])
    if taper_right:
        gnd = NANOWIRE << WIRE
        gnd.connect("e2", line.ports["e4"])
        NANOWIRE.add_port(name="e2", port=gnd.ports[0])
    else:
        NANOWIRE.add_port(name="e2", port=LINE.ports["e2"])

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
    return HAIRPIN


@gf.cell
def variable_length_hairpin_constriction(
    channel_length: float = 1,
    channel_width: float = 0.1,
    channel_pitch=0.3,
    fine_cross_section: str = "metal1",
    coarse_cross_section: str = "metal1",
    corner_type: str = "default",
    taper_left: bool = True,
    taper_right: bool = True,
) -> gf.Component:
    """Creates a single wire, made of two optimal steps"""
    fine_xs = gf.get_cross_section(fine_cross_section)
    coarse_xs = gf.get_cross_section(coarse_cross_section)
    NANOWIRE = gf.Component()

    if taper_left or taper_right:
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
                pitch=channel_pitch,
                length=channel_length / 2,
                layer=gf.get_cross_section(fine_cross_section).layer,
            )
        case "round":
            hairpin = LINE << _round_hairpin(
                width=channel_width,
                pitch=channel_pitch,
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

    line = NANOWIRE << LINE
    if taper_left:
        source = NANOWIRE << WIRE
        source.connect("e2", line.ports["e1"], allow_width_mismatch=True)
        NANOWIRE.add_port(name="e1", port=source.ports[0])
    else:
        NANOWIRE.add_port(name="e1", port=LINE.ports["e1"])

    if taper_right:
        gnd = NANOWIRE << WIRE
        gnd.connect("e2", line.ports["e2"], allow_width_mismatch=True)
        NANOWIRE.add_port(name="e2", port=gnd.ports[0])
    else:
        NANOWIRE.add_port(name="e2", port=LINE.ports["e2"])

    return NANOWIRE


@gf.cell
def variable_length_meander_constriction(
    channel_width: float = 0.1,
    channel_pitch=0.5,
    size=(1, 1),
    fine_cross_section: str = "metal1",
    coarse_cross_section: str = "metal1",
    add_tapers: bool = True,
    taper_left: bool = True,
    taper_right: bool = True,
) -> gf.Component:
    """Creates a single wire, made of two optimal steps"""
    fine_xs = gf.get_cross_section(fine_cross_section)
    coarse_xs = gf.get_cross_section(coarse_cross_section)
    NANOWIRE = gf.Component()

    if taper_left or taper_right:
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
        radius=fine_xs.radius_min,
        npoints=300,
    )
    entrance_bend.mirror_y()
    entrance_bend.connect("e1", meander.ports["e1"])
    exit_bend = LINE << gf.components.bend_circular(
        cross_section=fine_cross_section,
        angle=90,
        width=channel_width,
        radius=fine_xs.radius_min,
        npoints=300,
    )
    exit_bend.connect("e1", meander.ports["e2"])
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
    if taper_left:
        taper1 = NANOWIRE << WIRE
        taper1.connect("e1", LINE.ports["e1"])
        NANOWIRE.add_port(name="e1", port=taper1.ports["e2"])
    else:
        NANOWIRE.add_port(name="e1", port=LINE.ports["e1"])

    if taper_right:
        taper2 = NANOWIRE << WIRE
        taper2.connect("e2", LINE.ports["e2"])
        NANOWIRE.add_port(name="e2", port=taper2.ports["e2"])
    else:
        NANOWIRE.add_port(name="e2", port=LINE.ports["e2"])

    return NANOWIRE
