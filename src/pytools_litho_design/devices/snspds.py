import gdsfactory as gf
from ..components.superconductors.snspds import spot_snspd, straight_snspd
from ..components.rings import two_ring_muxer

from ..components.transitions.tapers import taper_to_ridge
from typing import Union, Tuple


@gf.cell
def spot_snspd_device(
    channel_w: float = 0.3,
    metal_cross_section: Union[gf.CrossSection, str] = "nbtin",
    add_channel_protection: bool = True,
    anticrowding_factor: float = 0.4,
    waveguide_cross_section: str | gf.CrossSection | None = "asic",
    waveguide_extension: float = 0,
    add_wire_transition: bool = False,
    pad: str | gf.Component | None = None,
    taper_pads: bool = True,
    pad_distance: Tuple[float, float] = (100, 100),
) -> gf.Component:
    return straight_snspd_device(
        channel_w=channel_w,
        channel_l=0,
        add_channel_protection=add_channel_protection,
        metal_cross_section=metal_cross_section,
        anticrowding_factor=anticrowding_factor,
        waveguide_cross_section=waveguide_cross_section,
        waveguide_extension=waveguide_extension,
        add_wire_transition=add_wire_transition,
        pad=pad,
        taper_pads=taper_pads,
        pad_distance=pad_distance,
    )


@gf.cell
def straight_snspd_device(
    channel_w: float = 0.3,
    channel_l: float = 1,
    add_channel_protection: bool = True,
    metal_cross_section: gf.CrossSection | str = "nbtin",
    anticrowding_factor: float = 0.4,
    waveguide_cross_section: gf.CrossSection | str = "asic",
    waveguide_extension: float = 0,
    add_wire_transition: bool = False,
    transition_cross_section: gf.CrossSection | str = "au",
    pad: str | gf.Component | None = None,
    taper_pads: bool = True,
    pad_distance: Tuple[float, float] = (100, 100),
) -> gf.Component:
    if isinstance(metal_cross_section, str):
        metal_cross_section = gf.get_cross_section(metal_cross_section)
    if isinstance(waveguide_cross_section, str):
        waveguide_cross_section = gf.get_cross_section(waveguide_cross_section)

    # Create the SNSPD component
    SNSPD = gf.Component()  # The chip parent component
    if channel_l == 0:
        SNSPD_COMPONENT = spot_snspd(
            channel_w=channel_w,
            wire_cross_section=metal_cross_section,
            anticrowding_factor=anticrowding_factor,
            waveguide_cross_section=waveguide_cross_section,
            waveguide_extension=waveguide_extension,
            add_channel_protection=add_channel_protection,
        )
    else:
        SNSPD_COMPONENT = straight_snspd(
            channel_w=channel_w,
            channel_l=channel_l,
            wire_cross_section=metal_cross_section,
            anticrowding_factor=anticrowding_factor,
            waveguide_cross_section=waveguide_cross_section,
            waveguide_extension=waveguide_extension,
            add_channel_protection=add_channel_protection,
        )

    # Add the snspd component to the parent component
    snspd_ref = SNSPD << SNSPD_COMPONENT

    if add_wire_transition:
        TRANSITION = taper_to_ridge(
            length=10,
            width1=metal_cross_section.width,
            width2=metal_cross_section.width,
            layer_wg=metal_cross_section.layer,
            layer_slab=transition_cross_section.layer,
            w_slab1=transition_cross_section.width,
            w_slab2=metal_cross_section.width,
            cross_section=transition_cross_section,
            use_slab_port=True,
            port_type="electrical",
        ).copy()
        ts1 = SNSPD << TRANSITION
        ts2 = SNSPD << TRANSITION
        ts1.connect(ts1.ports["e1"], snspd_ref.ports["e1"])
        ts2.connect(ts2.ports["e1"], snspd_ref.ports["e2"])

    # Add the elektrical pads
    if pad is not None:
        if isinstance(pad, str):
            pad = gf.get_component(pad)
        if add_wire_transition:
            assert (
                pad.layer == transition_cross_section.layer
            ), "Pad layer must match transition cross section layer."
        left_pad = SNSPD << pad
        left_pad.dmove((pad.xsize + pad_distance[0], pad.ysize + pad_distance[1]))
        right_pad = SNSPD << pad
        right_pad.dmove((-pad.xsize - pad_distance[0], pad.ysize + pad_distance[1]))

        gf.routing.route_single(
            SNSPD,
            left_pad.ports["e4"],
            snspd_ref.ports["e2"],
            cross_section=metal_cross_section,
            auto_taper=taper_pads,
            radius=(
                metal_cross_section.radius
                if metal_cross_section.radius is not None
                else metal_cross_section.radius_min
            ),
        )  # Route the left pad
        gf.routing.route_single(
            SNSPD,
            right_pad.ports["e4"],
            snspd_ref.ports["e1"],
            cross_section=metal_cross_section,
            auto_taper=taper_pads,
            radius=(
                metal_cross_section.radius
                if metal_cross_section.radius is not None
                else metal_cross_section.radius_min
            ),
        )

    # Extend the waveguide to the edges of the pads
    # Length should be half the pad size
    straight_path = gf.components.straight(
        length=waveguide_extension,
        cross_section=waveguide_cross_section,
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

    # Add the pads to the final component
    if pad is not None and not add_wire_transition:
        SNSPD.add_port(name="e1", port=snspd_ref.ports["e1"])
        SNSPD.add_port(name="e2", port=snspd_ref.ports["e2"])
    if add_wire_transition:
        SNSPD.add_port(
            name="e1", port=ts2.ports["e2"], layer=transition_cross_section.layer
        )
        SNSPD.add_port(
            name="e2", port=ts1.ports["e2"], layer=transition_cross_section.layer
        )
    else:
        SNSPD.add_port(name="e1", port=snspd_ref.ports["e1"])
        SNSPD.add_port(name="e2", port=snspd_ref.ports["e2"])

    SNSPD.add_port(name="o1", port=top_extension.ports["o2"])
    SNSPD.add_port(name="o2", port=bottom_extension.ports["o2"])
    SNSPD.center = (0, 0)
    return SNSPD


def muxed_spot_snspd_device(
    component: gf.Component,
    radius_list: list = [20, 40],
    cross_section="sio2",
    component_pitch: int = 500,
) -> gf.Component:
    if isinstance(cross_section, str):
        cross_section = gf.get_cross_section(cross_section)

    assert (
        radius_list[0] < radius_list[1]
    ), "The first radius must be less than the second radius."
    C = gf.Component()
    DEMUXER = two_ring_muxer(radius_list=radius_list, cross_section=cross_section)
    demuxer = C << DEMUXER
    demuxer.center = (0, 0)
    c1 = C << component
    c1.rotate(-90)
    c1.move((-500, -component_pitch / 2))
    # c1.connect(port="o1", other=demuxer.ports["o2"])
    c2 = C << component
    c2.rotate(-90)
    c2.move((-500, component_pitch / 2))
    # c2.connect(port="o1", other=demuxer.ports["o3"])

    gf.routing.route_bundle(
        C,
        [c2.ports["o1"], c1.ports["o1"]],
        [demuxer.ports["o2"], demuxer.ports["o3"]],
        cross_section=cross_section,
        radius=100,
        on_collision="error",
    )

    # Add the optical ports
    C.add_port("o1", port=demuxer.ports["o1"])
    C.add_port("o2", port=c1.ports["o2"])
    C.add_port("o3", port=c2.ports["o2"])

    # Add the electrical ports
    C.add_port("e1", port=c1.ports["e1"])
    C.add_port("e2", port=c1.ports["e2"])
    C.add_port("e3", port=c2.ports["e1"])
    C.add_port("e4", port=c2.ports["e2"])

    return C


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
