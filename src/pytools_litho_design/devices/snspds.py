import gdsfactory as gf
from ..components.superconductors.snspds import (
    hairpin_snspd,
    straight_snspd,
    meander_snspd,
    choked_hairpin_snspd,
)
from gdsfactory.typings import CrossSectionSpec

# from ..components.rings import two_ring_muxer

from ..components.geometries import add_protection_mask
from typing import Union, Tuple, List


# @gf.cell
# def spot_snspd_device(
#     channel_w: float = 0.3,
#     metal_cross_section: Union[gf.CrossSection, str] = "nbtin",
#     add_channel_protection: bool = True,
#     anticrowding_factor: float = 0.4,
#     waveguide_cross_section: str | gf.CrossSection | None = "asic",
#     waveguide_extension: float = 0,
#     clearance_size: Tuple[int, int] | None = None,
#     cladding_layer: str = "NEG_SIO2_BOT",
#     add_wire_transition: bool = False,
#     pad: str | gf.Component | None = None,
#     taper_pads: bool = True,
#     pad_distance: Tuple[float, float] = (100, 100),
# ) -> gf.Component:
#     return straight_snspd_device(
#         channel_w=channel_w,
#         channel_l=0,
#         add_channel_protection=add_channel_protection,
#         metal_cross_section=metal_cross_section,
#         anticrowding_factor=anticrowding_factor,
#         waveguide_cross_section=waveguide_cross_section,
#         waveguide_extension=waveguide_extension,
#         clearance_size=clearance_size,
#         cladding_layer=cladding_layer,
#         add_wire_transition=add_wire_transition,
#         pad=pad,
#         taper_pads=taper_pads,
#         pad_distance=pad_distance,
#     )


def _add_pads(
    component: gf.Component,
    pad: str | gf.Component,
    pad_distance: Tuple[float, float],
    coarse_metal_cross_section: str | gf.CrossSection,
    waveguide_cross_section: str | gf.CrossSection = "asic",
    protection_mask_cross_section: str | gf.CrossSection | None = None,
) -> gf.Component:
    """Adds pads to the component."""
    if isinstance(coarse_metal_cross_section, str):
        coarse_metal_cross_section = gf.get_cross_section(coarse_metal_cross_section)
    if isinstance(waveguide_cross_section, str):
        waveguide_cross_section = gf.get_cross_section(waveguide_cross_section)
    if (
        isinstance(protection_mask_cross_section, str)
        and protection_mask_cross_section is not None
    ):
        protection_mask_cross_section = gf.get_cross_section(
            protection_mask_cross_section
        )
    if isinstance(pad, str):
        pad = gf.get_component(pad)
    if isinstance(pad, gf.Component):
        pad = pad.copy()

    C = gf.Component()
    snspd_ref = C << component

    # Add the pads and move to the right position
    pad1 = C << pad
    pad2 = C << pad
    pad1.move((-pad_distance[0], pad_distance[1]))
    pad2.move((pad_distance[0], pad_distance[1]))

    # Route the pads to the device
    left_route = gf.routing.route_bundle(
        C,
        [pad1.ports["e4"]],
        [snspd_ref.ports["e1"]],
        cross_section=coarse_metal_cross_section,
        router="optical",
    )
    right_route = gf.routing.route_bundle(
        C,
        [pad2.ports["e4"]],
        [snspd_ref.ports["e2"]],
        cross_section=coarse_metal_cross_section,
        router="optical",
    )

    # Add the protection mask over the signal wire
    if protection_mask_cross_section is not None:
        temp = gf.Component()
        for route in left_route:
            for i in route.instances:
                temp.add(i)
        for route in right_route:
            for i in route.instances:
                temp.add(i)

        temp = add_protection_mask(
            component=temp,
            protection_layer=protection_mask_cross_section.layer,
            component_layers=[
                coarse_metal_cross_section.layer,
                waveguide_cross_section.layer,
            ],
            offset=protection_mask_cross_section.width,
            corner_radius=None,
        )
        C << temp.copy_layers(
            layer_map={
                protection_mask_cross_section.layer: protection_mask_cross_section.layer
            }
        )

    # Add the original ports to the component
    C.add_ports(component.ports)

    return C


@gf.cell
def straight_snspd_device(
    channel_width: float = 0.3,
    channel_length: float = 1,
    fine_metal_cross_section: gf.CrossSection | str = "nbtin",
    coarse_metal_cross_section: gf.CrossSection | str = "nbtin",
    waveguide_cross_section: gf.CrossSection | str = "asic",
    protection_mask_cross_section: gf.CrossSection | str = "asic",
    clearance_size: Tuple[int, int] | None = None,
    cladding_layer: str = "NEG_SIO2_BOT",
    pad: str | gf.Component | None = None,
    pad_distance: Tuple[float, float] = (100, 100),
) -> gf.Component:
    # Create the SNSPD component
    SNSPD = gf.Component()

    # Add the snspd component to the parent component
    SNSPD_GEOMETRY = straight_snspd(
        channel_width=channel_width,
        channel_length=channel_length,
        fine_wire_cross_section=fine_metal_cross_section,
        coarse_wire_cross_section=coarse_metal_cross_section,
        waveguide_cross_section=waveguide_cross_section,
        protection_mask_cross_section=protection_mask_cross_section,
    )

    # Add the elektrical pads
    if pad is not None:
        SNSPD_GEOMETRY = _add_pads(
            component=SNSPD_GEOMETRY,
            pad=pad,
            pad_distance=pad_distance,
            coarse_metal_cross_section=coarse_metal_cross_section,
            waveguide_cross_section=waveguide_cross_section,
            protection_mask_cross_section=protection_mask_cross_section,
        )

    snspd_ref = SNSPD << SNSPD_GEOMETRY

    # Extend the waveguide to the edges of the pads
    # Length should be half the pad size
    straight_path = gf.components.straight(
        length=10,
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
    SNSPD.flatten()
    return SNSPD


@gf.cell
def hairpin_snspd_device(
    channel_length: float = 1,
    channel_pitch: float = 0.3,
    fine_metal_cross_section: gf.CrossSection | str = "nbtin",
    coarse_metal_cross_section: gf.CrossSection | str = "nbtin",
    waveguide_cross_section: gf.CrossSection | str = "asic",
    protection_mask_cross_section: gf.CrossSection | str = "asic",
    clearance_size: Tuple[int, int] | None = None,
    cladding_layer: str = "NEG_SIO2_BOT",
    pad: str | gf.Component | None = None,
    pad_distance: Tuple[float, float] = (100, 100),
    corner_type: str = "round",
) -> gf.Component:
    # Create the SNSPD component
    SNSPD = gf.Component()

    # Add the snspd component to the parent component
    SNSPD_GEOMETRY = hairpin_snspd(
        channel_length=channel_length,
        channel_pitch=channel_pitch,
        fine_wire_cross_section=fine_metal_cross_section,
        coarse_wire_cross_section=coarse_metal_cross_section,
        protection_mask_cross_section=protection_mask_cross_section,
        waveguide_cross_section=waveguide_cross_section,
        corner_type=corner_type,
    )
    # snspd_ref = SNSPD << SNSPD_GEOMETRY

    # Add the electrical pads
    if pad is not None:
        SNSPD_GEOMETRY = _add_pads(
            component=SNSPD_GEOMETRY,
            pad=pad,
            pad_distance=pad_distance,
            coarse_metal_cross_section=coarse_metal_cross_section,
            waveguide_cross_section=waveguide_cross_section,
            protection_mask_cross_section=protection_mask_cross_section,
        )

    snspd_ref = SNSPD << SNSPD_GEOMETRY

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

    SNSPD.add_port(name="o1", port=snspd_ref.ports["o1"])
    SNSPD.add_port(name="o2", port=snspd_ref.ports["o2"])
    SNSPD.center = (0, 0)
    SNSPD.flatten()
    return SNSPD


@gf.cell
def meander_snspd_device(
    channel_width: float = 0.3,
    channel_pitch: float = 1,
    size: Tuple[float, float] = (5, 5),
    add_signal_wire_protection: bool = True,
    fine_metal_cross_section: CrossSectionSpec = "nbtin",
    coarse_metal_cross_section: CrossSectionSpec = "nbtin",
    waveguide_cross_section: CrossSectionSpec = "asic",
    protection_mask_cross_section: CrossSectionSpec | None = None,
    protection_mask_offset: float = 3,
    protection_mask_rounding: float = 0.5,
    waveguide_extension: float = 0,
    pad: str | gf.Component | None = None,
    pad_distance: Tuple[float, float] = (100, 100),
) -> gf.Component:
    # Create the SNSPD component
    SNSPD = gf.Component()

    # Add the snspd component to the parent component
    SNSPD_GEOMETRY = meander_snspd(
        channel_width=channel_width,
        channel_pitch=channel_pitch,
        size=size,
        fine_wire_cross_section=fine_metal_cross_section,
        coarse_wire_cross_section=coarse_metal_cross_section,
        waveguide_cross_section=waveguide_cross_section,
        protection_mask_cross_section=protection_mask_cross_section,
        protection_mask_offset=protection_mask_offset,
        protection_mask_rounding=protection_mask_rounding,
    )

    # Add the electrical pads
    if pad is not None:
        SNSPD_GEOMETRY = _add_pads(
            component=SNSPD_GEOMETRY,
            pad=pad,
            pad_distance=pad_distance,
            coarse_metal_cross_section=coarse_metal_cross_section,
            waveguide_cross_section=waveguide_cross_section,
            protection_mask_cross_section=protection_mask_cross_section,
            protection_mask_offset=protection_mask_offset,
            protection_mask_rounding=protection_mask_rounding,
            add_protection=add_signal_wire_protection,
        )

    snspd_ref = SNSPD << SNSPD_GEOMETRY

    if waveguide_extension > 0:
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
    if pad is not None:  # and not add_wire_transition:
        SNSPD.add_port(name="e1", port=snspd_ref.ports["e1"])
        SNSPD.add_port(name="e2", port=snspd_ref.ports["e2"])
    else:
        pass

    if waveguide_extension > 0:
        SNSPD.add_port(name="o1", port=top_extension.ports["o2"])
        SNSPD.add_port(name="o2", port=bottom_extension.ports["o2"])
    else:
        SNSPD.add_port(name="o1", port=snspd_ref.ports["o1"])
        SNSPD.add_port(name="o2", port=snspd_ref.ports["o2"])
    SNSPD.center = (0, 0)
    SNSPD.flatten()
    return SNSPD


@gf.cell
def choked_hairpin_snspd_device(
    # Channel parameters
    channel_length: float = 1,
    channel_pitch: float = 0.2,
    channel_corner_type: str = "round",
    choke_offset: float = 4,
    choke_size: Tuple[float, float] = (10, 10),
    choke_pitch: float = 0.3,
    # Protection parameters
    protection_mask_cross_section: CrossSectionSpec | None = None,
    # Cross-section parameters
    fine_metal_cross_section: gf.CrossSection | str = "nbtin",
    choke_cross_section: gf.CrossSection | str = "nbtin",
    coarse_metal_cross_section: gf.CrossSection | str = "nbtin",
    waveguide_cross_section: gf.CrossSection | str = "asic",
    # Pad parameters
    pad: str | gf.Component | None = None,
    pad_distance: Tuple[float, float] = (100, 100),
) -> gf.Component:
    # Create the SNSPD component
    SNSPD = gf.Component()

    # Add the snspd component to the parent component
    SNSPD_GEOMETRY = choked_hairpin_snspd(
        channel_length=channel_length,
        channel_pitch=channel_pitch,
        channel_corner_type=channel_corner_type,
        fine_wire_cross_section=fine_metal_cross_section,
        coarse_wire_cross_section=coarse_metal_cross_section,
        choke_cross_section=choke_cross_section,
        choke_offset=choke_offset,
        choke_size=choke_size,
        choke_pitch=choke_pitch,
        waveguide_cross_section=waveguide_cross_section,
        protection_mask_cross_section=protection_mask_cross_section,
    )

    # Add the electrical pads
    if pad is not None:
        SNSPD_GEOMETRY = _add_pads(
            component=SNSPD_GEOMETRY,
            pad=pad,
            pad_distance=pad_distance,
            coarse_metal_cross_section=coarse_metal_cross_section,
            waveguide_cross_section=waveguide_cross_section,
            protection_mask_cross_section=protection_mask_cross_section,
        )

    snspd_ref = SNSPD << SNSPD_GEOMETRY

    # Add the pads to the final component
    if pad is not None:  # and not add_wire_transition:
        SNSPD.add_port(name="e1", port=snspd_ref.ports["e1"])
        SNSPD.add_port(name="e2", port=snspd_ref.ports["e2"])
    else:
        pass

    SNSPD.add_port(name="o1", port=snspd_ref.ports["o1"])
    SNSPD.add_port(name="o2", port=snspd_ref.ports["o2"])
    SNSPD.center = (0, 0)
    SNSPD.flatten()
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

    c = straight_snspd_device(
        channel_w=channel_w,
        source_w=source_w,
        guide_w=guide_w,
        anticrowding_factor=anticrowding_factor,
        pad_size=pad_size,
    )

    c.show()
