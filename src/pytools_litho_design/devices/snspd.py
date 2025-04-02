import gdsfactory as gf
from ..components.superconductors.snspd import spot_snspd


@gf.cell
def spot_snspd_device(
    channel_w: float = 0.3,
    source_w: float = 2,
    electrical_layer: str = "NEG_NBTIN",
    guide_w: float = 0.5,
    anticrowding_factor: float = 0.4,
    guide_layer: str = "WAVEGUIDE",
    pad_size: float = (50, 50),
) -> gf.Component:
    SNSPD = gf.Component()  # The chip parent component
    SNSPD_COMPONENT = spot_snspd(
        channel_w=channel_w,
        # channel_l=0.2,
        source_w=source_w,
        anticrowding_factor=anticrowding_factor,
        nanowire_layer=electrical_layer,
        guide_w=guide_w,
        guide_layer=guide_layer,
    )

    # Add the snspd component to the parent component
    snspd_ref = SNSPD << SNSPD_COMPONENT
    for port in snspd_ref.ports:
        port_name = f"snspd_{port.name}"
        # if port.layer == pdk.layers.NEG_NBTIN:
        #     port.port_type = "electrical"
        SNSPD.add_port(name=port_name, port=port, layer=electrical_layer)

    # Add the elektrical pads
    PAD = gf.components.pad(size=pad_size, layer=electrical_layer)
    metal_xs = gf.cross_section.cross_section(
        width=source_w,
        layer=electrical_layer,
        port_types=["electrical", "electrical"],
    )
    bend_xs = gf.components.bend_euler(cross_section=metal_xs)
    # C = gf.routing.add_pads_top(
    #     component=SNSPD, cross_section=metal_xs, pad=PAD, pad_pitch=100, bend=bend_xs
    # )
    left_pad = SNSPD << PAD
    left_pad.dmove((-pad_size[0], 0))
    right_pad = SNSPD << PAD
    right_pad.dmove((pad_size[0], 0))

    gf.routing.route_single(
        component=SNSPD,
        port1=left_pad.ports["e3"],
        port2=snspd_ref.ports["e1"],
        cross_section=metal_xs,
        bend=bend_xs,
    )  # Route the left pad

    gf.routing.route_single(
        component=SNSPD,
        port1=right_pad.ports["e1"],
        port2=snspd_ref.ports["e2"],
        cross_section=metal_xs,
        bend=bend_xs,
    )  # Route the right pad

    # Extend the waveguide to the edges of the pads
    waveguide_xs = gf.cross_section.strip(
        width=guide_w, layer=guide_layer, port_types=["optical", "optical"]
    )
    # bend_xs = gf.components.bend_euler(cross_section=waveguide_xs)
    # Length should be half the pad size
    straight_path = gf.components.straight(
        length=pad_size[0] / 2,
        cross_section=waveguide_xs,
    )
    top_extension = SNSPD << straight_path
    top_extension.connect(
        top_extension.ports["o1"],
        snspd_ref.ports["o2"],
    )
    bottom_extension = SNSPD << straight_path
    bottom_extension.connect(
        bottom_extension.ports["o1"],
        snspd_ref.ports["o1"],
    )

    # Create the final component
    FINAL_SNSPD = gf.Component()
    snspd_ref = FINAL_SNSPD << SNSPD

    # Add the pads to the final component
    FINAL_SNSPD.add_port(name="e1", port=left_pad.ports["pad"])
    FINAL_SNSPD.add_port(name="e2", port=right_pad.ports["pad"])
    FINAL_SNSPD.add_port(name="o1", port=top_extension.ports["o2"])
    FINAL_SNSPD.add_port(name="o2", port=bottom_extension.ports["o2"])
    return FINAL_SNSPD


if __name__ == "__main__":
    # Create the SNSPD device
    # Some parameters
    channel_w = 0.3
    source_w = 2
    guide_w = 0.5
    anticrowding_factor = 0.4
    pad_size = (50, 50)

    c = spot_snspd_device(
        channel_w=channel_w,
        source_w=source_w,
        guide_w=guide_w,
        anticrowding_factor=anticrowding_factor,
        pad_size=pad_size,
    )

    c.show()
