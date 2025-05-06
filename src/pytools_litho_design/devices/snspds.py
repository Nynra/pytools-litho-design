import gdsfactory as gf
from ..components.superconductors.snspds import spot_snspd, straight_snspd

from ..components.transitions.tapers import taper_to_ridge
from typing import Union


@gf.cell
def spot_snspd_device(
    channel_w: float = 0.3,
    wire_cross_section: Union[gf.CrossSection, str] = "nbtin",
    superconductor_cross_section: Union[gf.CrossSection, str] = "nbtin",
    anticrowding_factor: float = 0.4,
    waveguide_cross_section: Union[gf.CrossSection, str] = "strip",
    waveguide_extension: float = 0,
    add_markers: bool = False,
    marker_distance: float = 100,
    marker_size: float = (50, 50),
    marker_component: str = "ebl_marker",
    add_wire_transition: bool = True,
    add_pads: bool = False,
    pad_component: str = "pad",
    taper_pads: bool = False,
    pad_distance: float = 100,
    pad_size: float = (50, 50),
) -> gf.Component:
    return straight_snspd_device(
        channel_w=channel_w,
        channel_l=0,
        wire_cross_section=wire_cross_section,
        superconductor_cross_section=superconductor_cross_section,
        anticrowding_factor=anticrowding_factor,
        waveguide_cross_section=waveguide_cross_section,
        waveguide_extension=waveguide_extension,
        add_markers=add_markers,
        marker_distance=marker_distance,
        marker_size=marker_size,
        marker_component=marker_component,
        add_wire_transition=add_wire_transition,
        add_pads=add_pads,
        pad_component=pad_component,
        taper_pads=taper_pads,
        pad_distance=pad_distance,
        pad_size=pad_size,
    )
    # if isinstance(wire_cross_section, str):
    #     wire_cross_section = gf.get_cross_section(wire_cross_section)
    # if isinstance(superconductor_cross_section, str):
    #     superconductor_cross_section = gf.get_cross_section(
    #         superconductor_cross_section
    #     )
    # if isinstance(waveguide_cross_section, str):
    #     waveguide_cross_section = gf.get_cross_section(waveguide_cross_section)

    # # Create the SNSPD component
    # SNSPD = gf.Component()  # The chip parent component
    # SNSPD_COMPONENT = spot_snspd(
    #     channel_w=channel_w,
    #     wire_cross_section=wire_cross_section,
    #     anticrowding_factor=anticrowding_factor,
    #     waveguide_cross_section=waveguide_cross_section,
    #     waveguide_extension=waveguide_extension,
    # )

    # # Add the snspd component to the parent component
    # snspd_ref = SNSPD << SNSPD_COMPONENT

    # # Add the elektrical pads
    # if add_pads:
    #     if isinstance(pad_component, str):
    #         pad_component = gf.get_component(pad_component)
    #     PAD = gf.components.pad(size=pad_size, layer=wire_cross_section.layer)
    #     left_pad = SNSPD << PAD
    #     left_pad.dmove((pad_size[0] + pad_distance, 0))
    #     right_pad = SNSPD << PAD
    #     right_pad.dmove((-pad_size[0] - pad_distance, 0))

    #     gf.routing.route_bundle(
    #         SNSPD,
    #         [left_pad.ports["e1"], right_pad.ports["e3"]],
    #         [snspd_ref.ports["e1"], snspd_ref.ports["e2"]],
    #         cross_section=wire_cross_section,
    #         auto_taper=taper_pads,
    #     )  # Route the left pad

    # # Extend the waveguide to the edges of the pads
    # # Length should be half the pad size
    # straight_path = gf.components.straight(
    #     length=pad_size[0] / 2 + waveguide_extension,
    #     cross_section=waveguide_cross_section,
    # )

    # top_extension = SNSPD << straight_path
    # top_extension.connect(
    #     top_extension.ports["o1"],
    #     snspd_ref.ports["o2"],
    # )
    # bottom_extension = SNSPD << straight_path
    # bottom_extension.connect(
    #     bottom_extension.ports["o1"],
    #     snspd_ref.ports["o1"],
    # )

    # # Create the final component
    # FINAL_SNSPD = gf.Component()
    # snspd_ref = FINAL_SNSPD << SNSPD

    # # Add the pads to the final component
    # if add_pads:
    #     FINAL_SNSPD.add_port(name="e1", port=left_pad.ports["e1"])
    #     FINAL_SNSPD.add_port(name="e2", port=right_pad.ports["e1"])
    # FINAL_SNSPD.add_port(name="o1", port=top_extension.ports["o2"])
    # FINAL_SNSPD.add_port(name="o2", port=bottom_extension.ports["o2"])
    # return FINAL_SNSPD


@gf.cell
def straight_snspd_device(
    channel_w: float = 0.3,
    channel_l: float = 1,
    add_channel_protection: bool = True,
    wire_cross_section: gf.CrossSection | str = "au",
    superconductor_cross_section: gf.CrossSection | str = "nbtin",
    anticrowding_factor: float = 0.4,
    waveguide_cross_section: gf.CrossSection | str = "waveguide",
    waveguide_extension: float = 0,
    add_markers: bool = False,
    marker_distance: float = 100,
    marker_size: float = (50, 50),
    marker_component: str = "ebl_marker",
    add_wire_transition: bool = True,
    add_pads: bool = False,
    pad_component: str = "pad",
    taper_pads: bool = False,
    pad_distance: float = 100,
    pad_size: float = (50, 50),
) -> gf.Component:
    if isinstance(wire_cross_section, str):
        wire_cross_section = gf.get_cross_section(wire_cross_section)
    if isinstance(superconductor_cross_section, str):
        superconductor_cross_section = gf.get_cross_section(
            superconductor_cross_section
        )
    if isinstance(waveguide_cross_section, str):
        waveguide_cross_section = gf.get_cross_section(waveguide_cross_section)

    # Create the SNSPD component
    SNSPD = gf.Component()  # The chip parent component
    if channel_l == 0:
        SNSPD_COMPONENT = spot_snspd(
            channel_w=channel_w,
            wire_cross_section=superconductor_cross_section,
            anticrowding_factor=anticrowding_factor,
            waveguide_cross_section=waveguide_cross_section,
            waveguide_extension=waveguide_extension,
            add_channel_protection=add_channel_protection,
        )
    else:
        SNSPD_COMPONENT = straight_snspd(
            channel_w=channel_w,
            channel_l=channel_l,
            wire_cross_section=superconductor_cross_section,
            anticrowding_factor=anticrowding_factor,
            waveguide_cross_section=waveguide_cross_section,
            waveguide_extension=waveguide_extension,
            add_channel_protection=add_channel_protection,
        )

    # Add the snspd component to the parent component
    snspd_ref = SNSPD << SNSPD_COMPONENT

    if add_wire_transition:
        TRANSITION = taper_to_ridge(
            width1=wire_cross_section.width,
            width2=wire_cross_section.width,
            layer_wg=superconductor_cross_section.layer,
            layer_slab=wire_cross_section.layer,
            w_slab1=wire_cross_section.width,
            w_slab2=superconductor_cross_section.width,
            cross_section=wire_cross_section,
            use_slab_port=False,
            port_type="electrical",
        ).copy()

        # TRANSITION.draw_ports()
        ts1 = SNSPD << TRANSITION
        ts2 = SNSPD << TRANSITION
        print(ts1.ports)
        ts1.connect(ts1.ports["e1"], snspd_ref.ports["e1"])
        ts2.connect(ts2.ports["e1"], snspd_ref.ports["e2"])

    # Add the elektrical pads
    if add_pads:
        if isinstance(pad_component, str):
            pad_component = gf.get_component(pad_component)
        PAD = gf.components.pad(size=pad_size, layer=wire_cross_section.layer)
        left_pad = SNSPD << PAD
        left_pad.dmove((pad_size[0] + pad_distance, 0))
        right_pad = SNSPD << PAD
        right_pad.dmove((-pad_size[0] - pad_distance, 0))

        gf.routing.route_bundle(
            SNSPD,
            [left_pad.ports["e1"], right_pad.ports["e3"]],
            [snspd_ref.ports["e1"], snspd_ref.ports["e2"]],
            cross_section=wire_cross_section,
            auto_taper=taper_pads,
        )  # Route the left pad

    # Extend the waveguide to the edges of the pads
    # Length should be half the pad size
    straight_path = gf.components.straight(
        length=pad_size[0] / 2 + waveguide_extension,
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
    if not add_pads and not add_wire_transition:
        SNSPD.add_port(name="e1", port=snspd_ref.ports["e1"])
        SNSPD.add_port(name="e2", port=snspd_ref.ports["e2"])
    if add_wire_transition:
        SNSPD.add_port(name="e1", port=ts2.ports["e2"], layer=wire_cross_section.layer)
        SNSPD.add_port(name="e2", port=ts1.ports["e2"], layer=wire_cross_section.layer)
    SNSPD.add_port(name="o1", port=top_extension.ports["o2"])
    SNSPD.add_port(name="o2", port=bottom_extension.ports["o2"])
    return SNSPD


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
