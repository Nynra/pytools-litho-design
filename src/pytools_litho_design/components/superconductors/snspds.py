import gdsfactory as gf
import numpy as np
from gdsfactory.typings import Layer, CrossSectionSpec

from .constrictions import (
    _round_hairpin,
    variable_length_constriction,
    variable_length_hairpin_constriction,
    variable_length_meander_constriction,
)
from ..geometries import taper_to_ridge, add_protection_mask
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
    protection_mask_cross_section: CrossSectionSpec | None = None,
    taper_left: bool = True,
    taper_right: bool = True,
) -> gf.Component:
    waveguide_xs = gf.get_cross_section(waveguide_cross_section)

    # Add the nanowire
    C = gf.Component()
    LINE = variable_length_constriction(
        channel_width=channel_width,
        channel_length=channel_length,
        fine_cross_section=fine_wire_cross_section,
        coarse_cross_section=coarse_wire_cross_section,
        protection_mask_cross_section=protection_mask_cross_section,
        taper_left=taper_left,
        taper_right=taper_right,
    )
    nanowire = C << LINE
    # Add the waveguide to the middle of the nanowire
    length = 10
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
            size=(nanowire.xsize * 0.3, channel_width * 3 + 3),
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


@gf.cell
def hairpin_snspd(
    channel_length: float = 10,
    channel_pitch: float = 0.3,
    fine_wire_cross_section: str = "nbtin",
    coarse_wire_cross_section: str = "course_nbtin",
    waveguide_cross_section: str = "strip",
    protection_mask_cross_section: CrossSectionSpec | None = None,
    corner_type: str = "round",
    taper_left: bool = True,
    taper_right: bool = True,
) -> gf.Component:
    if isinstance(waveguide_cross_section, str):
        waveguide_xs = gf.get_cross_section(waveguide_cross_section)
    else:
        waveguide_xs = waveguide_cross_section
    if isinstance(fine_wire_cross_section, str):
        fine_wire_xs = gf.get_cross_section(fine_wire_cross_section)
    else:
        fine_wire_xs = fine_wire_cross_section
    if isinstance(coarse_wire_cross_section, str):
        coarse_wire_xs = gf.get_cross_section(coarse_wire_cross_section)
    else:
        coarse_wire_xs = coarse_wire_cross_section
    if isinstance(protection_mask_cross_section, str):
        protection_mask_xs = gf.get_cross_section(protection_mask_cross_section)
    else:
        protection_mask_xs = protection_mask_cross_section

    # Add the nanowire
    C = gf.Component()
    LINE = variable_length_hairpin_constriction(
        channel_length=channel_length,
        fine_cross_section=fine_wire_cross_section,
        coarse_cross_section=coarse_wire_cross_section,
        channel_pitch=channel_pitch,
        protection_mask_cross_section=protection_mask_xs,
        channel_corner_type=corner_type,
        taper_left=taper_left,
        taper_right=taper_right,
    )

    # LINE.draw_ports()
    # LINE.show()
    nanowire = C << LINE
    # Add the waveguide to the middle of the nanowire
    waveguide = C << straight_waveguide(
        length=nanowire.xsize / 2,
        width=fine_wire_xs.width + channel_pitch + 1,
        cross_section=waveguide_cross_section,
    )
    # waveguide.rotate(90)
    waveguide.center = nanowire.center
    waveguide.xmax = nanowire.xmax

    if protection_mask_cross_section is not None:
        C = add_protection_mask(
            component=C,
            protection_layer=protection_mask_xs.layer,
            component_layers=[
                fine_wire_xs.layer,
                coarse_wire_xs.layer,
            ],
            offset=protection_mask_xs.width,
            corner_radius=protection_mask_xs.radius,
        )

    # Add the ports
    C.add_port(
        name="o1",
        port=waveguide.ports["o2"],
        cross_section=waveguide_cross_section,
    )
    C.add_port(
        name="o2",
        port=waveguide.ports["o1"],
        cross_section=waveguide_cross_section,
    )

    C.add_port(name="e2", port=nanowire.ports["e1"])
    C.add_port(name="e1", port=nanowire.ports["e2"])
    C.center = (0, 0)
    C.flatten()
    C.rotate(90)

    return C


@gf.cell
def choked_hairpin_snspd(
    channel_length: float = 10,
    channel_pitch: float = 0.3,
    channel_corner_type: str = "round",
    choke_offset: float = 0.5,
    choke_pitch: float = 0.5,
    choke_size: tuple[float, float] = (5, 5),
    protection_mask_cross_section: CrossSectionSpec | None = None,
    fine_wire_cross_section: CrossSectionSpec = "nbtin",
    coarse_wire_cross_section: CrossSectionSpec = "course_nbtin",
    choke_cross_section: CrossSectionSpec = "nbtin",
    waveguide_cross_section: CrossSectionSpec = "strip",
    taper_left: bool = True,
    taper_right: bool = True,
) -> gf.Component:
    if isinstance(waveguide_cross_section, str):
        waveguide_xs = gf.get_cross_section(waveguide_cross_section)
    else:
        waveguide_xs = waveguide_cross_section
    if isinstance(fine_wire_cross_section, str):
        fine_wire_xs = gf.get_cross_section(fine_wire_cross_section)
    else:
        fine_wire_xs = fine_wire_cross_section
    if isinstance(coarse_wire_cross_section, str):
        coarse_wire_xs = gf.get_cross_section(coarse_wire_cross_section)
    else:
        coarse_wire_xs = coarse_wire_cross_section
    if isinstance(choke_cross_section, str):
        choke_xs = gf.get_cross_section(choke_cross_section)
    else:
        choke_xs = choke_cross_section
    if isinstance(protection_mask_cross_section, str):
        protection_mask_cross_section = gf.get_cross_section(
            protection_mask_cross_section
        )

    # Add the nanowire
    C = gf.Component()
    LINE = gf.Component()
    HAIRPIN = variable_length_hairpin_constriction(
        channel_length=channel_length,
        channel_pitch=channel_pitch,
        fine_cross_section=fine_wire_cross_section,
        coarse_cross_section=coarse_wire_cross_section,
        waveguide_cross_section=waveguide_cross_section,
        protection_mask_cross_section=protection_mask_cross_section,
        taper_right=False,
        channel_corner_type=channel_corner_type,
    )
    hairpin = LINE << HAIRPIN
    hairpin.mirror_y()

    choke = LINE << variable_length_meander_constriction(
        channel_pitch=choke_pitch,
        size=choke_size,
        coarse_cross_section=coarse_wire_xs,
        fine_cross_section=choke_xs,
        taper_left=False,
    )
    in_taper = LINE << gf.components.taper_cross_section(
        cross_section1=fine_wire_xs, cross_section2=choke_xs, length=1
    )
    in_taper.connect("e1", hairpin.ports["e2"])
    connector = LINE << gf.components.straight(
        length=choke_offset,
        width=choke_xs.width,
        cross_section=choke_xs,
    )
    connector.connect("e1", in_taper.ports["e2"])
    choke.connect("e1", connector.ports["e2"])

    LINE.add_port(
        name="e1",
        port=hairpin.ports["e1"],
        cross_section=fine_wire_xs,
    )
    LINE.add_port(
        name="e2",
        port=choke.ports["e2"],
        cross_section=choke_xs,
    )
    if waveguide_cross_section is not None:
        LINE.add_port(
            name="o1",
            port=hairpin.ports["o1"],
            cross_section=waveguide_cross_section,
        )
        LINE.add_port(
            name="o2",
            port=hairpin.ports["o2"],
            cross_section=waveguide_cross_section,
        )
        print("Adding waveguide ports")

    C << LINE
    C.add_ports(LINE.ports)
    C.center = (0, 0)
    C.rotate(90)

    if protection_mask_cross_section is not None:
        C = add_protection_mask(
            component=C,
            protection_layer=protection_mask_cross_section.layer,
            component_layers=[
                fine_wire_xs.layer,
                coarse_wire_xs.layer,
                choke_xs.layer,
            ],
            offset=protection_mask_cross_section.width,
            corner_radius=protection_mask_cross_section.radius,
        )
    C.flatten()
    return C


@gf.cell
def meander_snspd(
    channel_width: float = 0.5,
    channel_pitch: float = 0.3,
    size: tuple[float, float] = (5, 5),
    fine_wire_cross_section: CrossSectionSpec = "nbtin",
    coarse_wire_cross_section: CrossSectionSpec = "course_nbtin",
    waveguide_cross_section: CrossSectionSpec = "strip",
    protection_mask_cross_section: CrossSectionSpec | None = None,
) -> gf.Component:
    if isinstance(waveguide_cross_section, str):
        waveguide_xs = gf.get_cross_section(waveguide_cross_section)
    else:
        waveguide_xs = waveguide_cross_section
    if isinstance(fine_wire_cross_section, str):
        fine_wire_cross_section = gf.get_cross_section(fine_wire_cross_section)
    if isinstance(coarse_wire_cross_section, str):
        coarse_wire_cross_section = gf.get_cross_section(coarse_wire_cross_section)
    if isinstance(protection_mask_cross_section, str):
        protection_mask_cross_section = gf.get_cross_section(
            protection_mask_cross_section
        )

    # Add the nanowire
    C = gf.Component()
    LINE = variable_length_meander_constriction(
        channel_width=channel_width,
        channel_pitch=channel_pitch,
        size=size,
        fine_cross_section=fine_wire_cross_section,
        coarse_cross_section=coarse_wire_cross_section,
        protection_mask_cross_section=protection_mask_cross_section,
    )

    # LINE.draw_ports()
    # LINE.show()
    nanowire = C << LINE
    # Add the waveguide to the middle of the nanowire
    waveguide = C << straight_waveguide(
        length=size[0] * 1.5,
        width=channel_width + channel_pitch + 1,
        cross_section=waveguide_cross_section,
    )
    # waveguide.rotate(90)
    waveguide.center = nanowire.center
    # waveguide.xmax = nanowire.xmax

    # Add the ports
    C.add_port(
        name="o1",
        port=waveguide.ports["o2"],
        cross_section=waveguide_cross_section,
    )
    C.add_port(
        name="o2",
        port=waveguide.ports["o1"],
        cross_section=waveguide_cross_section,
    )

    print(nanowire.ports)
    C.draw_ports()
    C.show()
    C.add_port(name="e2", port=nanowire.ports["e1"])
    C.add_port(name="e1", port=nanowire.ports["e2"])
    C.center = (0, 0)
    C.flatten()
    C.rotate(90)

    return C


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # c = spot_snspd()
    # c = rectangle_meander()
    # c.plot()
    # plt.show()
