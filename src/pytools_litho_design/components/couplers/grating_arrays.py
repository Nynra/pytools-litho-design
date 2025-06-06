import gdsfactory as gf
from functools import partial
from gdsfactory.typings import ComponentSpec, CrossSectionSpec


@gf.cell
def grating_coupler_array(
    grating_coupler: ComponentSpec = "grating_coupler_elliptical",
    pitch: float = 127,
    n: int = 5,
    cross_section: CrossSectionSpec = "strip",
    with_loopback: bool = True,
    with_loss_structure: bool = False,
) -> gf.Component:
    """Create a grating coupler array for glued fibers.

    Parameters:
        grating_coupler: ComponentSpec
            Grating coupler component or name.
        pitch: float
            Pitch between grating couplers.
        n: int
            Number of grating couplers in the array.
        cross_section: CrossSectionSpec
            Cross-section for the waveguides.
        with_loopback: bool
            Whether to include a loopback structure.
        with_loss_structure: bool
            Whether to include a loss structure. This loop in combination with the
            loopback structure can be used to measure the loss of the grating coupler.

    Returns:
        gf.Component of the grating coupler array.
    """
    if isinstance(grating_coupler, str):
        grating_coupler = gf.get_component(grating_coupler)
    if isinstance(cross_section, str):
        cross_section = gf.get_cross_section(cross_section)

    min_gratings = 1
    min_gratings += 2 if with_loopback else 0
    min_gratings += 2 if with_loss_structure else 0
    if n < min_gratings:
        raise ValueError(
            f"n must be at least {min_gratings} for this configuration, got {n}"
        )

    # Create a fiber array
    GRATING_ARRAY = gf.components.grating_coupler_array(
        grating_coupler=grating_coupler,
        pitch=pitch,
        n=n,
        rotation=-90,
        cross_section=cross_section,
        with_loopback=False,
    )
    CHIP = gf.Component()
    grating_array = CHIP << GRATING_ARRAY

    # Add the alignment and loss structure
    # Create a short piece of waveguide to use as a checkpoint during routing
    CHECKPOINT = gf.components.straight(
        cross_section=cross_section,
    )
    radius = cross_section.radius_min

    if with_loopback:
        loopback_checkpoint1 = CHIP << CHECKPOINT
        loopback_checkpoint1.center = (
            grating_array.xmin,
            grating_array.ymin - 1.5 * cross_section.radius,
        )

        loopback_checkpoint2 = CHIP << CHECKPOINT
        loopback_checkpoint2.center = (
            grating_array.xmax,
            grating_array.ymin - 1.5 * cross_section.radius,
        )

        gf.routing.route_bundle(
            CHIP,
            [
                grating_array.ports["o0"],
            ],
            [
                loopback_checkpoint1.ports["o1"],
            ],
            cross_section=cross_section,
            # start_straight_length=cross_section.radius_min,
            end_straight_length=cross_section.radius,
            bend=gf.get_component(
                "bend_euler", cross_section=cross_section, radius=radius
            ),
        )
        gf.routing.route_bundle(
            CHIP,
            [
                grating_array.ports[f"o{n-1}"],
            ],
            [
                loopback_checkpoint2.ports["o2"],
            ],
            cross_section=cross_section,
            end_straight_length=cross_section.radius,
            bend=gf.get_component(
                "bend_euler", cross_section=cross_section, radius=radius
            ),
        )
        gf.routing.route_single(
            CHIP,
            loopback_checkpoint1.ports["o2"],
            loopback_checkpoint2.ports["o1"],
            cross_section=cross_section,
            bend=gf.get_component(
                "bend_euler", cross_section=cross_section, radius=radius
            ),
        )
    if with_loss_structure and not with_loopback:
        raise ValueError("Loss structure cannot be enabled without loopback.")

    if with_loss_structure:
        # Position the checkpoints below the grating array
        loss_checkpoint1 = CHIP << CHECKPOINT
        loss_checkpoint1.center = (
            grating_array.xmin - cross_section.radius,
            grating_array.ymin - 2.5 * cross_section.radius,
        )
        loss_checkpoint2 = CHIP << CHECKPOINT
        loss_checkpoint2.center = (
            grating_array.xmax + cross_section.radius,
            grating_array.ymin - 2.5 * cross_section.radius,
        )

        gf.routing.route_bundle(
            CHIP,
            [
                grating_array.ports["o1"],
                grating_array.ports[f"o{n-2}"],
            ],
            [
                loss_checkpoint1.ports["o1"],
                loss_checkpoint2.ports["o2"],
            ],
            cross_section=cross_section,
            start_straight_length=cross_section.radius,
            end_straight_length=cross_section.radius,
            bend=gf.get_component(
                "bend_euler", cross_section=cross_section, radius=radius
            ),
        )
        gf.routing.route_single(
            CHIP,
            loss_checkpoint1.ports["o2"],
            loss_checkpoint2.ports["o1"],
            cross_section=cross_section,
            bend=gf.get_component(
                "bend_euler", cross_section=cross_section, radius=radius
            ),
        )

    if with_loopback and with_loss_structure:
        skip_ports = ["o0", "o1", f"o{n-1}", f"o{n-2}"]
    elif with_loopback:
        skip_ports = ["o0", f"o{n-1}"]
    else:
        skip_ports = []

    iter = 1
    for cnt, port in enumerate(grating_array.ports):
        # Skip first and last ports as we use these for a loss route
        if port.name in skip_ports:
            continue

        # Add the other ports
        CHIP.add_port(name=f"o{iter}", port=port)
        iter += 1

    return CHIP


@gf.cell
def grating_coupler_cluster(
    coupler: ComponentSpec = "grating_coupler_traditional",
    row_offset: int = 150,
    column_offset: int = 600,
    cross_section: CrossSectionSpec = "strip",
) -> gf.Component:
    """Create a cluster of grating couplers.

    Parameters:
        coupler: ComponentSpec
            Grating coupler component or name.
        row_offset: int
            Vertical offset between rows of grating couplers.
        column_offset: int
            Horizontal offset between columns of grating couplers.
        cross_section: CrossSectionSpec
            Cross-section for the waveguides.

    Returns:
        gf.Component of the grating coupler cluster.
    """
    if isinstance(cross_section, str):
        cross_section = gf.get_cross_section(cross_section)
    if isinstance(coupler, str):
        coupler = gf.get_component(coupler)

    # Create the chip and create the layout
    CHIP = gf.Component()
    grating1 = CHIP << coupler
    grating2 = CHIP << coupler
    grating3 = CHIP << coupler
    grating4 = CHIP << coupler
    grating5 = CHIP << coupler
    grating6 = CHIP << coupler
    grating7 = CHIP << coupler
    grating8 = CHIP << coupler

    # Position the gratings
    grating2.rotate(180)
    grating2.center = (grating1.x - column_offset, grating1.y)
    grating3.rotate(180)
    grating3.center = (grating1.x, grating1.y - row_offset)
    grating4.center = (grating2.x, grating2.y - row_offset)
    grating5.center = (grating3.x, grating3.y - row_offset)
    grating6.rotate(180)
    grating6.center = (grating4.x, grating4.y - row_offset)
    grating7.rotate(180)
    grating7.center = (grating5.x, grating5.y - row_offset)
    grating8.center = (grating6.x, grating6.y - row_offset)

    # Create 4 ports at the top and 4 at the bottom
    OUTPUT_GUIDE = gf.components.waveguides.straight(
        length=10,
        cross_section=cross_section,
    )
    output1 = CHIP << OUTPUT_GUIDE
    output2 = CHIP << OUTPUT_GUIDE
    output3 = CHIP << OUTPUT_GUIDE
    output4 = CHIP << OUTPUT_GUIDE
    output5 = CHIP << OUTPUT_GUIDE
    output6 = CHIP << OUTPUT_GUIDE
    output7 = CHIP << OUTPUT_GUIDE
    output8 = CHIP << OUTPUT_GUIDE

    # 1, 4, 5, 8 at the bottom
    guide_spacing = column_offset / 6
    output_offset = row_offset
    output5.rotate(-90)
    output5.center = (grating7.x - 1.5 * guide_spacing, grating7.y - output_offset)
    output1.rotate(-90)
    output1.center = (grating7.x - 2.5 * guide_spacing, grating7.y - output_offset)
    output8.rotate(-90)
    output8.center = (grating8.x - 1.5 * guide_spacing, grating8.y - output_offset)
    output4.rotate(-90)
    output4.center = (grating8.x - 2.5 * guide_spacing, grating8.y - output_offset)

    # 2, 3, 6, 7 at the top
    output6.rotate(90)
    output6.center = (grating1.x - 3.5 * guide_spacing, grating1.y + output_offset)
    output2.rotate(90)
    output2.center = (grating1.x - 4.5 * guide_spacing, grating1.y + output_offset)
    output3.rotate(90)
    output3.center = (grating1.x + 1.5 * guide_spacing, grating2.y + output_offset)
    output7.rotate(90)
    output7.center = (grating1.x + 2.5 * guide_spacing, grating2.y + output_offset)

    # Route the waveguides
    gf.routing.route_bundle(
        CHIP,
        [
            grating1.ports["o1"],
            grating5.ports["o1"],
        ],
        [
            output1.ports["o1"],
            output5.ports["o1"],
        ],
        cross_section=cross_section,
    )
    gf.routing.route_bundle(
        CHIP,
        [
            grating3.ports["o1"],
            grating7.ports["o1"],
        ],
        [
            output3.ports["o1"],
            output7.ports["o1"],
        ],
        cross_section=cross_section,
    )
    gf.routing.route_bundle(
        CHIP,
        [
            grating2.ports["o1"],
            grating6.ports["o1"],
            #         grating7.ports["o1"],
            #         grating8.ports["o1"],
        ],
        [
            output2.ports["o1"],
            output6.ports["o1"],
            #         output7.ports["o1"],
            #         output8.ports["o1"],
        ],
        cross_section=cross_section,
    )
    gf.routing.route_bundle(
        CHIP,
        [
            grating4.ports["o1"],
            grating8.ports["o1"],
        ],
        [
            output4.ports["o1"],
            output8.ports["o1"],
        ],
        cross_section=cross_section,
    )

    FINAL_CHIP = gf.Component()
    FINAL_CHIP << CHIP
    FINAL_CHIP.add_port("o1", port=output1.ports["o2"], cross_section="strip")
    FINAL_CHIP.add_port("o2", port=output2.ports["o2"], cross_section="strip")
    FINAL_CHIP.add_port("o3", port=output3.ports["o2"], cross_section="strip")
    FINAL_CHIP.add_port("o4", port=output4.ports["o2"], cross_section="strip")
    FINAL_CHIP.add_port("o5", port=output5.ports["o2"], cross_section="strip")
    FINAL_CHIP.add_port("o6", port=output6.ports["o2"], cross_section="strip")
    FINAL_CHIP.add_port("o7", port=output7.ports["o2"], cross_section="strip")
    FINAL_CHIP.add_port("o8", port=output8.ports["o2"], cross_section="strip")
    FINAL_CHIP.flatten()
    return FINAL_CHIP


@gf.cell
def grating_coupler_opposing(
    grating: str | gf.Component = "grating_coupler_traditional",
    n: int = 4,
    distance: int = 150,
    pitch: int = 200,
    cross_section: str | gf.Component = "asic",
) -> gf.Component:
    assert n % 2 == 0, "n must be even"
    n_side = int(n / 2)
    GRATING_ARRAY = grating_coupler_array(
        grating_coupler=grating,
        n=n_side,
        cross_section=cross_section,
        with_loopback=False,
        pitch=pitch,
    )
    C = gf.Component()
    array1 = C << GRATING_ARRAY
    array2 = C << GRATING_ARRAY
    array2.rotate(180)
    array1.ymin = array2.ymax + distance

    # CHIP.flatten()
    for port in array1.ports:
        C.add_port(f"0_{port.name}", port=port)

    for port in array2.ports:
        C.add_port(f"1_{port.name}", port=port)
    return C


if __name__ == "__main__":
    c = grating_coupler_opposing()
    c.draw_ports()
    c.show()

#     get_pdk("demo", set_active=True)

#     c = glued_grating_array(
#         grating_coupler="grating_coupler_elliptical",
#         with_loopback=True,
#         with_loss_test=True,
#     )
#     c.show()
