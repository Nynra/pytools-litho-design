import gdsfactory as gf
import numpy as np
from gdsfactory.typings import Layer

from .constrictions import variable_length_constriction
from gdsfactory.components.waveguides import straight as straight_waveguide
from typing import Union


@gf.cell
def straight_snspd(
    channel_width: float = 0.5,
    channel_length: float = 10,
    add_channel_protection: bool = True,
    fine_wire_cross_section: str = "nbtin",
    coarse_wire_cross_section: str = "course_nbtin",
    waveguide_cross_section: str = "strip",
    waveguide_extension: float = 0,
) -> gf.Component:
    waveguide_xs = gf.get_cross_section(waveguide_cross_section)

    # Add the nanowire
    C = gf.Component()
    nanowire = C << variable_length_constriction(
        channel_width=channel_width,
        channel_length=channel_length,
        fine_cross_section=fine_wire_cross_section,
        coarse_cross_section=coarse_wire_cross_section,
    )

    # Add the waveguide to the middle of the nanowire
    length = 10 + 2 * waveguide_extension
    waveguide = C << straight_waveguide(
        cross_section=waveguide_cross_section, length=length
    )
    waveguide.rotate(90)
    waveguide.center = (
        nanowire.xmin + nanowire.xsize / 2,
        nanowire.ymin + nanowire.ysize / 2,
    )
    if add_channel_protection:
        PROTECTION_LAYER = gf.components.rectangle(
            size=(nanowire.xsize * 0.3, channel_width * 3 + 1),
            layer=waveguide_xs.layer,
        ).copy()
        rinner = 2000
        router = rinner
        ROUNDED_PROTECTION_LAYER = gf.Component()
        for p in PROTECTION_LAYER.get_polygons(layers=[waveguide_xs.layer])[
            gf.get_layer(waveguide_xs.layer)
        ]:
            p_round = p.round_corners(rinner, router, 200)
            ROUNDED_PROTECTION_LAYER.add_polygon(p_round, layer=waveguide_xs.layer)

        protection_rect = C << ROUNDED_PROTECTION_LAYER

        # Position the center over the center of the wire
        protection_rect.center = nanowire.center

    # Add the ports
    C.add_port(
        name="o2",
        port=waveguide.ports["o2"],
        cross_section=waveguide_cross_section,
    )
    C.add_port(
        name="o1",
        port=waveguide.ports["o1"],
        cross_section=waveguide_cross_section,
    )

    C.add_port(name="e1", port=nanowire.ports["e1"])
    C.add_port(name="e2", port=nanowire.ports["e2"])
    C.center = (0, 0)
    C.flatten()

    return C


# @gf.cell
# def spot_snspd(
#     channel_w: float = 0.5,
#     fine_wire_cross_section: Union[gf.CrossSection, str] = "metal1",
#     course_wire_cross_section: Union[gf.CrossSection, str] = "course_nbtin",
#     anticrowding_factor: float = 1.2,
#     waveguide_cross_section: Union[gf.CrossSection, str] = "strip",
#     waveguide_extension: float = 0,
#     add_output_grating: bool = False,
#     output_grating: str | gf.Component = "grating_coupler_traditional",
#     add_channel_protection: bool = True,
# ) -> gf.Component:
#     return straight_snspd(
#         channel_w=channel_w,
#         channel_l=0,
#         fine_wire_cross_section=fine_wire_cross_section,
#         course_wire_cross_section=course_wire_cross_section,
#         anticrowding_factor=anticrowding_factor,
#         waveguide_cross_section=waveguide_cross_section,
#         waveguide_extension=waveguide_extension,
#         add_output_grating=add_output_grating,
#         output_grating=output_grating,
#         add_channel_protection=add_channel_protection,
#     )


# def hairpin_snspd(
#     length_hairpin=40,
#     width_hairpin=0.05,
#     pitch_hairpin=0.3,
#     rotation_hairpin=90,  # 0, 90, or 180
#     num_of_boxes_meander=23,  # Always use odd number
#     width_meander=0.5,
#     length_meander_box=10,
#     bending_radius_meander=0.75,
#     insulator_width_meander=1.5,
#     wire_width_regular=5,
#     Markers=True,
# ):
#     Meander = create_rectangle_meander(
#         num_of_boxes=num_of_boxes_meander,
#         width=width_meander,
#         length=length_meander_box,
#         bending_radius=bending_radius_meander,
#         insulator_width=insulator_width_meander,
#         wire_width=wire_width_regular,
#     )
#     Meander.move(destination=(50, -50))
#     hairpin_custom = hairpin_with_tapers(
#         hairpin_length=length_hairpin,
#         hairpin_width=width_hairpin,
#         hairpin_pitch=pitch_hairpin,
#         wire_width=wire_width_regular,
#         rotation=rotation_hairpin,
#     )
#     Pads = create_connection_pads(bonding_pad=True)

#     R_Pad_to_HP = pr.route_smooth(
#         port1=Pads.ports["Left"],
#         port2=hairpin_custom.ports["input"],
#         radius=5,
#         width=None,
#         path_type="manhattan",
#         manual_path=None,
#         smooth_options={"corner_fun": pp.euler, "use_eff": True},
#         layer=2,
#     )

#     R_HP_to_Meander = pr.route_smooth(
#         port1=Meander.ports["input"],
#         port2=hairpin_custom.ports["output"],
#         radius=5,
#         width=None,
#         path_type="manhattan",
#         manual_path=None,
#         smooth_options={"corner_fun": pp.euler, "use_eff": True},
#         layer=2,
#     )

#     R_Meander_to_Pad = pr.route_smooth(
#         port1=Meander.ports["output"],
#         port2=Pads.ports["Right"],
#         radius=5,
#         width=None,
#         path_type="manhattan",
#         manual_path=None,
#         smooth_options={"corner_fun": pp.euler, "use_eff": True},
#         layer=2,
#     )
#     C = dl.Device()
#     C.add_ref(
#         [Pads, Meander, hairpin_custom, R_Pad_to_HP, R_HP_to_Meander, R_Meander_to_Pad]
#     )

#     return C


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # c = spot_snspd()
    # c = rectangle_meander()
    # c.plot()
    # plt.show()
