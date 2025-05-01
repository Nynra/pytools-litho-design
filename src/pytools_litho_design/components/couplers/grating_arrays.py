import gdsfactory as gf


@gf.cell
def grating_coupler_array(
    grating_coupler="grating_coupler_elliptical",
    pitch=127,
    n=5,
    cross_section="strip",
    with_loopback=True,
    with_loss_test=True,
):
    """Create a grating coupler array for glued fibers."""
    if isinstance(grating_coupler, str):
        grating_coupler = gf.get_component(grating_coupler)
    if isinstance(cross_section, str):
        cross_section = gf.get_cross_section(cross_section)

    min_gratings = 1
    min_gratings += 2 if with_loopback else 0
    min_gratings += 2 if with_loss_test else 0
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
        with_loopback=with_loopback,
    )
    CHIP = gf.Component()
    grating_array = CHIP << GRATING_ARRAY

    if with_loss_test:
        # Add the alignment and loss structure
        # Create a short piece of waveguide to use as a checkpoint during routing
        CHECKPOINT = gf.components.straight(
            cross_section=cross_section,
        )

        # Position the checkpoints below the grating array
        loss_checkpoint1 = CHIP << CHECKPOINT
        loss_checkpoint1.center = (
            grating_array.xmin,
            grating_array.ymin - cross_section.radius_min,
        )
        loss_checkpoint2 = CHIP << CHECKPOINT
        loss_checkpoint2.center = (
            grating_array.xmax,
            grating_array.ymin - cross_section.radius_min,
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
        )
        gf.routing.route_single(
            CHIP,
            loss_checkpoint1.ports["o2"],
            loss_checkpoint2.ports["o1"],
            cross_section=cross_section,
        )

        for cnt, port in enumerate(grating_array.ports):
            # Skip first and last ports as we use these for a loss route
            if cnt == 0:
                continue
            if cnt == n - 1:
                continue

            # Add the other ports
            CHIP.add_port(name=f"o{cnt}", port=port)

    else:
        # Add all ports
        for port in grating_array.ports:
            CHIP.add_port(name=port.name, port=port)

    return CHIP


# if __name__ == "__main__":
#     get_pdk("demo", set_active=True)

#     c = glued_grating_array(
#         grating_coupler="grating_coupler_elliptical",
#         with_loopback=True,
#         with_loss_test=True,
#     )
#     c.show()
