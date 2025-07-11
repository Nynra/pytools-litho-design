import gdsfactory as gf
from ..geometries import add_protection_mask, rectangle, taper_to_ridge
from gdsfactory.typings import CrossSectionSpec


@gf.cell
def variable_length_constriction(
    channel_length: float = 1,
    channel_width: float = 0.1,
    fine_cross_section: str = "nbtin",
    coarse_cross_section: str = "course_nbtin",
    protection_mask_cross_section: CrossSectionSpec | None = None,
    taper_left: bool = True,
    taper_right: bool = True,
) -> gf.Component:
    """Creates a single wire, made of two optimal steps"""
    if isinstance(fine_cross_section, str):
        fine_xs = gf.get_cross_section(fine_cross_section)
    else:
        fine_xs = fine_cross_section
    if isinstance(coarse_cross_section, str):
        coarse_xs = gf.get_cross_section(coarse_cross_section)
    else:
        coarse_xs = coarse_cross_section
    if protection_mask_cross_section is not None:
        if isinstance(protection_mask_cross_section, str):
            protection_mask_cross_section = gf.get_cross_section(
                protection_mask_cross_section
            )
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

    if protection_mask_cross_section is not None:
        if isinstance(protection_mask_cross_section, str):
            protection_mask_cross_section = gf.get_cross_section(
                protection_mask_cross_section
            )
        final_NANOWIRE = add_protection_mask(
            component=final_NANOWIRE,
            protection_layer=protection_mask_cross_section.layer,
            component_layers=[
                fine_xs.layer,
                coarse_xs.layer,
            ],
            offset=protection_mask_cross_section.width,
            corner_radius=protection_mask_cross_section.radius,
        )
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
        radius=pitch,
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
    channel_pitch=0.3,
    fine_cross_section: CrossSectionSpec = "metal1",
    coarse_cross_section: CrossSectionSpec = "metal1",
    waveguide_cross_section: CrossSectionSpec | None = None,
    channel_corner_type: str = "default",
    protection_mask_cross_section: CrossSectionSpec | None = None,
    taper_left: bool = True,
    taper_right: bool = True,
) -> gf.Component:
    """Creates a single wire, made of two optimal steps"""
    if isinstance(fine_cross_section, str):
        fine_xs = gf.get_cross_section(fine_cross_section)
    else:
        fine_xs = fine_cross_section
    if isinstance(coarse_cross_section, str):
        coarse_xs = gf.get_cross_section(coarse_cross_section)
    else:
        coarse_xs = coarse_cross_section
    if protection_mask_cross_section is not None:
        if isinstance(protection_mask_cross_section, str):
            protection_mask_cross_section = gf.get_cross_section(
                protection_mask_cross_section
            )
    if waveguide_cross_section is not None:
        waveguide_cross_section = gf.get_cross_section(waveguide_cross_section)
        if waveguide_cross_section.width < 2 * fine_xs.width + channel_pitch:
            raise ValueError(
                f"The waveguide width is smaller than the hairpin width. "
                f"Please increase the waveguide width: {waveguide_cross_section.width} < {2 * fine_xs.width + channel_pitch}."
            )
    NANOWIRE = gf.Component()

    if taper_left or taper_right:
        WIRE = taper_to_ridge(
            length=3,
            width1=fine_xs.width,
            width2=fine_xs.width,
            slab_length=coarse_xs.width,
            w_slab2=coarse_xs.width,
            w_slab1=fine_xs.width if fine_xs.width > 2 else 2,
            port_type="electrical",
            main_cross_section=fine_cross_section,
            slab_cross_section=coarse_cross_section,
        )
    LINE = gf.Component()
    match channel_corner_type:
        case "default":
            hairpin = LINE << gf.components.optimal_hairpin(
                width=fine_xs.width,
                pitch=channel_pitch,
                length=channel_length / 2,
                layer=gf.get_cross_section(fine_cross_section).layer,
            )
        case "round":
            hairpin = LINE << _round_hairpin(
                width=fine_xs.width,
                pitch=channel_pitch,
                length=channel_length,
                cross_section=fine_xs,
            )
        case _:
            raise ValueError(f"Unknown corner type: {channel_corner_type}")
    deg90_bend1 = LINE << gf.components.bend_circular(
        cross_section=fine_xs,
        angle=90,
        width=fine_xs.width,
        npoints=300,
    )
    deg90_bend2 = LINE << gf.components.bend_circular(
        cross_section=fine_xs,
        angle=90,
        width=fine_xs.width,
        npoints=300,
    )
    deg90_bend1.mirror_y()
    deg90_bend1.connect("e2", hairpin.ports["e2"])
    deg90_bend2.connect("e2", hairpin.ports["e1"])
    # hairpin.flatten()

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
        source.connect("e2", line.ports["e1"])
        NANOWIRE.add_port(name="e1", port=source.ports["e1"])
    else:
        NANOWIRE.add_port(name="e1", port=LINE.ports["e1"])

    if taper_right:
        gnd = NANOWIRE << WIRE
        gnd.connect("e2", line.ports["e2"])
        NANOWIRE.add_port(name="e2", port=gnd.ports["e1"])
    else:
        NANOWIRE.add_port(name="e2", port=LINE.ports["e2"])

    if waveguide_cross_section is not None:
        # Add a waveguide over the hairpin
        waveguide = NANOWIRE << gf.components.straight(
            length=channel_length,
            cross_section=waveguide_cross_section,
        )
        waveguide.mirror_x()
        waveguide.center = hairpin.center
        NANOWIRE.add_ports(waveguide.ports)

    # NANOWIRE.flatten()

    if protection_mask_cross_section is not None:
        NANOWIRE = add_protection_mask(
            component=NANOWIRE,
            protection_layer=protection_mask_cross_section.layer,
            component_layers=[
                fine_xs.layer,
                coarse_xs.layer,
            ],
            offset=protection_mask_cross_section.width,
            corner_radius=protection_mask_cross_section.radius,
        )

    return NANOWIRE


@gf.cell
def variable_length_meander_constriction(
    channel_pitch=0.5,
    size=(1, 1),
    fine_cross_section: str = "metal1",
    coarse_cross_section: str = "metal1",
    protection_mask_cross_section: CrossSectionSpec | None = None,
    taper_left: bool = True,
    taper_right: bool = True,
) -> gf.Component:
    """Creates a single wire, made of two optimal steps"""
    if isinstance(fine_cross_section, str):
        fine_xs = gf.get_cross_section(fine_cross_section)
    else:
        fine_xs = fine_cross_section
    if isinstance(coarse_cross_section, str):
        coarse_xs = gf.get_cross_section(coarse_cross_section)
    else:
        coarse_xs = coarse_cross_section
    if protection_mask_cross_section is not None:
        if isinstance(protection_mask_cross_section, str):
            protection_mask_cross_section = gf.get_cross_section(
                protection_mask_cross_section
            )
    NANOWIRE = gf.Component()

    if taper_left or taper_right:
        WIRE = taper_to_ridge(
            length=3,
            width1=fine_xs.width,
            width2=fine_xs.width,
            slab_length=coarse_xs.width,
            w_slab2=coarse_xs.width,
            w_slab1=fine_xs.width if fine_xs.width > 2 else 2,
            port_type="electrical",
            main_cross_section=fine_xs,
            slab_cross_section=coarse_xs,
        )
    LINE = gf.Component()
    meander = LINE << gf.components.superconductors.snspd(
        wire_width=fine_xs.width,
        wire_pitch=channel_pitch,
        layer=fine_xs.layer,
        size=size,
        terminals_same_side=True,
    )

    entrance_bend = LINE << gf.components.bend_circular(
        cross_section=fine_xs,
        angle=90,
        width=fine_xs.width,
        radius=channel_pitch,
        npoints=300,
        allow_min_radius_violation=True,
    )
    entrance_bend.mirror_y()
    entrance_bend.connect("e1", meander.ports["e1"])
    exit_bend = LINE << gf.components.bend_circular(
        cross_section=fine_xs,
        angle=90,
        width=fine_xs.width,
        radius=channel_pitch,
        npoints=300,
        allow_min_radius_violation=True,
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
        NANOWIRE.add_port(name="e2", port=taper2.ports["e1"])
    else:
        NANOWIRE.add_port(name="e2", port=LINE.ports["e2"])

    if protection_mask_cross_section is not None:
        NANOWIRE = add_protection_mask(
            component=NANOWIRE,
            protection_layer=protection_mask_cross_section.layer,
            component_layers=[
                fine_xs.layer,
                coarse_xs.layer,
            ],
            offset=protection_mask_cross_section.width,
            corner_radius=protection_mask_cross_section.radius,
        )

    return NANOWIRE
