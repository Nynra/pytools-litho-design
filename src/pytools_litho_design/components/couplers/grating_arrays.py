import gdsfactory as gf
from functools import partial
from ..bends import bend_euler


@gf.cell
def grating_coupler_array(
    grating_coupler="grating_coupler_elliptical",
    pitch=127,
    n=5,
    cross_section="strip",
    with_loopback=True,
    with_loss_structure: bool = False,
):
    """Create a grating coupler array for glued fibers."""
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
            grating_array.ymin - 1.5 * cross_section.radius_min,
        )

        loopback_checkpoint2 = CHIP << CHECKPOINT
        loopback_checkpoint2.center = (
            grating_array.xmax,
            grating_array.ymin - 1.5 * cross_section.radius_min,
        )

        gf.routing.route_bundle(
            CHIP,
            [
                grating_array.ports["o0"],
                grating_array.ports[f"o{n-1}"],
            ],
            [
                loopback_checkpoint1.ports["o1"],
                loopback_checkpoint2.ports["o2"],
            ],
            cross_section=cross_section,
            # start_straight_length=cross_section.radius_min,
            end_straight_length=cross_section.radius_min,
            bend=gf.components.bend_euler(cross_section=cross_section, radius=radius),
        )
        gf.routing.route_single(
            CHIP,
            loopback_checkpoint1.ports["o2"],
            loopback_checkpoint2.ports["o1"],
            cross_section=cross_section,
            bend=gf.components.bend_euler(cross_section=cross_section, radius=radius),
        )
    if with_loss_structure and not with_loopback:
        raise ValueError("Loss structure cannot be enabled without loopback.")

    if with_loss_structure:
        # Position the checkpoints below the grating array
        loss_checkpoint1 = CHIP << CHECKPOINT
        loss_checkpoint1.center = (
            grating_array.xmin - cross_section.radius_min,
            grating_array.ymin - 2.5 * cross_section.radius_min,
        )
        loss_checkpoint2 = CHIP << CHECKPOINT
        loss_checkpoint2.center = (
            grating_array.xmax + cross_section.radius_min,
            grating_array.ymin - 2.5 * cross_section.radius_min,
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
            start_straight_length=cross_section.radius_min,
            end_straight_length=cross_section.radius_min,
            bend=gf.components.bend_euler(cross_section=cross_section, radius=radius),
        )
        gf.routing.route_single(
            CHIP,
            loss_checkpoint1.ports["o2"],
            loss_checkpoint2.ports["o1"],
            cross_section=cross_section,
            bend=gf.components.bend_euler(cross_section=cross_section, radius=radius),
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


# if __name__ == "__main__":
#     get_pdk("demo", set_active=True)

#     c = glued_grating_array(
#         grating_coupler="grating_coupler_elliptical",
#         with_loopback=True,
#         with_loss_test=True,
#     )
#     c.show()
