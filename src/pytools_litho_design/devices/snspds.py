import gdsfactory as gf
from ..components.superconductors.snspds import spot_snspd, straight_snspd
from ..components.rings import two_ring_muxer

from ..components.geometries.tapers import taper_to_ridge
from typing import Union, Tuple, List


@gf.cell
def spot_snspd_device(
    channel_w: float = 0.3,
    metal_cross_section: Union[gf.CrossSection, str] = "nbtin",
    add_channel_protection: bool = True,
    anticrowding_factor: float = 0.4,
    waveguide_cross_section: str | gf.CrossSection | None = "asic",
    waveguide_extension: float = 0,
    clearance_size: Tuple[int, int] | None = None,
    cladding_layer: str = "NEG_SIO2_BOT",
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
        clearance_size=clearance_size,
        cladding_layer=cladding_layer,
        add_wire_transition=add_wire_transition,
        pad=pad,
        taper_pads=taper_pads,
        pad_distance=pad_distance,
    )


@gf.cell
def straight_snspd_device(
    channel_width: float = 0.3,
    channel_length: float = 1,
    add_channel_protection: bool = True,
    fine_metal_cross_section: gf.CrossSection | str = "nbtin",
    coarse_metal_cross_section: gf.CrossSection | str = "nbtin",
    waveguide_cross_section: gf.CrossSection | str = "asic",
    waveguide_extension: float = 0,
    clearance_size: Tuple[int, int] | None = None,
    cladding_layer: str = "NEG_SIO2_BOT",
    pad: str | gf.Component | None = None,
    pad_distance: Tuple[float, float] = (100, 100),
) -> gf.Component:
    # Create the SNSPD component
    SNSPD = gf.Component()

    # Add the snspd component to the parent component
    snspd_ref = SNSPD << straight_snspd(
        channel_width=channel_width,
        channel_length=channel_length,
        fine_wire_cross_section=fine_metal_cross_section,
        coarse_wire_cross_section=coarse_metal_cross_section,
        waveguide_cross_section=waveguide_cross_section,
        waveguide_extension=waveguide_extension,
        add_channel_protection=add_channel_protection,
    )

    # Add the elektrical pads
    if pad is not None:
        pad1 = SNSPD << pad
        pad2 = SNSPD << pad
        pad1.move((-pad_distance[0], pad_distance[1]))
        pad2.move((pad_distance[0], pad_distance[1]))

        gf.routing.route_bundle(
            SNSPD,
            [pad1.ports["e4"]],
            [snspd_ref.ports["e1"]],
            cross_section="coarse_nbtin",
            router="optical",
        )
        gf.routing.route_bundle(
            SNSPD,
            [pad2.ports["e4"]],
            [snspd_ref.ports["e2"]],
            cross_section="coarse_nbtin",
            router="optical",
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

    if clearance_size is not None:
        cladding = SNSPD << gf.components.rectangle(
            size=clearance_size,
            layer=cladding_layer,
        )
        cladding.center = snspd_ref.center

    # Add the pads to the final component
    if pad is not None:  # and not add_wire_transition:
        SNSPD.add_port(name="e1", port=snspd_ref.ports["e1"])
        SNSPD.add_port(name="e2", port=snspd_ref.ports["e2"])
    else:
        pass

    SNSPD.add_port(name="o1", port=top_extension.ports["o2"])
    SNSPD.add_port(name="o2", port=bottom_extension.ports["o2"])
    SNSPD.center = (0, 0)
    return SNSPD


# def muxed_spot_snspd_device(
#     component: gf.Component,
#     radius_list: list = [20, 40],
#     cross_section="sio2",
#     component_pitch: int = 500,
# ) -> gf.Component:
#     if isinstance(cross_section, str):
#         cross_section = gf.get_cross_section(cross_section)

#     assert (
#         radius_list[0] < radius_list[1]
#     ), "The first radius must be less than the second radius."
#     C = gf.Component()
#     DEMUXER = two_ring_muxer(radius_list=radius_list, cross_section=cross_section)
#     demuxer = C << DEMUXER
#     demuxer.center = (0, 0)
#     c1 = C << component
#     c1.rotate(-90)
#     c1.move((-500, -component_pitch / 2))
#     # c1.connect(port="o1", other=demuxer.ports["o2"])
#     c2 = C << component
#     c2.rotate(-90)
#     c2.move((-500, component_pitch / 2))
#     # c2.connect(port="o1", other=demuxer.ports["o3"])

#     gf.routing.route_bundle(
#         C,
#         [c2.ports["o1"], c1.ports["o1"]],
#         [demuxer.ports["o2"], demuxer.ports["o3"]],
#         cross_section=cross_section,
#         radius=100,
#         on_collision="error",
#     )

#     # Add the optical ports
#     C.add_port("o1", port=demuxer.ports["o1"])
#     C.add_port("o2", port=c1.ports["o2"])
#     C.add_port("o3", port=c2.ports["o2"])

#     # Add the electrical ports
#     C.add_port("e1", port=c1.ports["e1"])
#     C.add_port("e2", port=c1.ports["e2"])
#     C.add_port("e3", port=c2.ports["e1"])
#     C.add_port("e4", port=c2.ports["e2"])

#     return C


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
