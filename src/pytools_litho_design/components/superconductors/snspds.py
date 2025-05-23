import gdsfactory as gf
import numpy as np
from gdsfactory.typings import Layer

from .constrictions import (
    _round_hairpin,
    variable_length_constriction,
    variable_length_hairpin_constriction,
    variable_length_meander_constriction,
)
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
    LINE = variable_length_constriction(
        channel_width=channel_width,
        channel_length=channel_length,
        fine_cross_section=fine_wire_cross_section,
        coarse_cross_section=coarse_wire_cross_section,
    )
    nanowire = C << LINE
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
    channel_width: float = 0.5,
    channel_length: float = 10,
    add_channel_protection: bool = True,
    fine_wire_cross_section: str = "nbtin",
    coarse_wire_cross_section: str = "course_nbtin",
    hairpin_pitch: float = 0.3,
    choke_cross_section: str = "nbtin",
    waveguide_cross_section: str = "strip",
    waveguide_extension: float = 0,
    corner_type: str = "round",
) -> gf.Component:
    waveguide_xs = gf.get_cross_section(waveguide_cross_section)

    # Add the nanowire
    C = gf.Component()
    LINE = variable_length_hairpin_constriction(
        channel_width=channel_width,
        channel_length=channel_length,
        fine_cross_section=fine_wire_cross_section,
        coarse_cross_section=coarse_wire_cross_section,
        choke_cross_section=choke_cross_section,
        hairpin_pitch=hairpin_pitch,
        corner_type=corner_type,
    )

    # LINE.draw_ports()
    # LINE.show()
    nanowire = C << LINE
    # Add the waveguide to the middle of the nanowire
    waveguide = C << straight_waveguide(
        length=nanowire.xsize / 2,
        width=channel_width + hairpin_pitch + 1,
        cross_section=waveguide_cross_section,
    )
    # waveguide.rotate(90)
    waveguide.center = nanowire.center
    waveguide.xmax = nanowire.xmax

    if add_channel_protection:
        rinner = 2000
        router = rinner

        # Add the second protection layer
        PROTECTION_LAYER2 = gf.components.rectangle(
            size=(
                waveguide_xs.radius / 15,
                nanowire.xsize,
            ),
            layer=waveguide_xs.layer,
        ).copy()
        ROUNDED_PROTECTION_LAYER2 = gf.Component()
        for p in PROTECTION_LAYER2.get_polygons(layers=[waveguide_xs.layer])[
            gf.get_layer(waveguide_xs.layer)
        ]:
            p_round = p.round_corners(rinner, router, 200)
            ROUNDED_PROTECTION_LAYER2.add_polygon(p_round, layer=waveguide_xs.layer)

        protection_rect2 = C << ROUNDED_PROTECTION_LAYER2
        protection_rect2.center = (nanowire.center[0], nanowire.center[1])

        # Add the first protection layer

        ROUNDED_PROTECTION_LAYER = gf.Component()
        protection_rect = C << ROUNDED_PROTECTION_LAYER
        PROTECTION_LAYER1 = gf.components.rectangle(
            size=(
                # channel_length,
                nanowire.xsize / 2,
                (9 + channel_width + hairpin_pitch),
            ),
            layer=waveguide_xs.layer,
        ).copy()
        for p in PROTECTION_LAYER1.get_polygons(layers=[waveguide_xs.layer])[
            gf.get_layer(waveguide_xs.layer)
        ]:
            p_round = p.round_corners(rinner, router, 200)
            ROUNDED_PROTECTION_LAYER.add_polygon(p_round, layer=waveguide_xs.layer)

        # Position the center over the center of the wire
        protection_rect.center = (
            nanowire.center[0] + channel_length / 2,
            nanowire.center[1],
        )
        protection_rect.xmin = protection_rect2.xmax - 2

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
    channel_width: float = 0.5,
    channel_length: float = 10,
    channel_pitch: float = 0.3,
    add_channel_protection: bool = True,
    fine_wire_cross_section: str = "nbtin",
    coarse_wire_cross_section: str = "course_nbtin",
    add_choke: bool = True,
    choke_offset: float = 2,
    choke_pitch: float = 1,
    choke_cross_section: str = "nbtin",
    waveguide_cross_section: str = "strip",
    waveguide_extension: float = 0,
    corner_type: str = "round",
) -> gf.Component:
    waveguide_xs = gf.get_cross_section(waveguide_cross_section)
    fine_wire_xs = gf.get_cross_section(fine_wire_cross_section)
    coarse_wire_xs = gf.get_cross_section(coarse_wire_cross_section)
    choke_xs = gf.get_cross_section(choke_cross_section)

    # Add the nanowire
    C = gf.Component()
    LINE = gf.Component()
    HAIRPIN = _round_hairpin(
        width=channel_width,
        length=channel_length,
        cross_section=fine_wire_xs,
        pitch=channel_pitch,
    )
    hairpin = LINE << HAIRPIN
    BEND_90_FINE = gf.components.bend_euler(
        radius=2 * choke_pitch,
        cross_section=fine_wire_xs,
    )
    in_bend = LINE << BEND_90_FINE
    out_bend = LINE << BEND_90_FINE
    in_bend.connect(
        in_bend.ports["e2"],
        hairpin.ports["e1"],
    )
    hairpin.connect(
        hairpin.ports["e2"],
        out_bend.ports["e1"],
    )
    # LINE.show()

    if add_choke:
        choke = LINE << variable_length_meander_constriction(
            channel_width=choke_xs.width,
            channel_pitch=choke_pitch,
            size=(5, 5),
            coarse_cross_section=choke_xs,
            fine_cross_section=choke_xs,
        )
        in_taper = LINE << gf.components.taper_cross_section(
            cross_section1=fine_wire_xs, cross_section2=choke_xs, length=1
        )
        out_bend.connect("e2", in_taper.ports["e1"])
        connector = LINE << gf.components.straight(
            length=choke_offset,
            width=choke_xs.width,
            cross_section=choke_xs,
        )
        connector.connect(
            connector.ports["e1"], out_bend.ports["e2"], allow_width_mismatch=True
        )
        choke.connect(
            choke.ports["e1"], connector.ports["e2"], allow_width_mismatch=True
        )

        LINE.add_port(
            name="e1",
            port=in_bend.ports["e2"],
            cross_section=fine_wire_xs,
        )
        LINE.add_port(
            name="e2",
            port=choke.ports["e2"],
            cross_section=choke_xs,
        )
        LINE.show()
    else:
        LINE.add_port(
            name="e1",
            port=in_bend.ports["e2"],
            cross_section=fine_wire_xs,
        )
        LINE.add_port(
            name="e2",
            port=out_bend.ports["e2"],
            cross_section=fine_wire_xs,
        )

    # LINE.draw_ports()
    # LINE.show()
    nanowire = C << LINE
    # Add the waveguide to the middle of the nanowire
    waveguide = C << straight_waveguide(
        length=nanowire.xsize / 2,
        width=channel_width + channel_pitch + 1,
        cross_section=waveguide_cross_section,
    )
    # waveguide.rotate(90)
    waveguide.center = nanowire.center
    waveguide.xmax = nanowire.xmax

    if add_channel_protection:
        rinner = 2000
        router = rinner

        # Add the second protection layer
        PROTECTION_LAYER2 = gf.components.rectangle(
            size=(
                waveguide_xs.radius / 15,
                nanowire.xsize,
            ),
            layer=waveguide_xs.layer,
        ).copy()
        ROUNDED_PROTECTION_LAYER2 = gf.Component()
        for p in PROTECTION_LAYER2.get_polygons(layers=[waveguide_xs.layer])[
            gf.get_layer(waveguide_xs.layer)
        ]:
            p_round = p.round_corners(rinner, router, 200)
            ROUNDED_PROTECTION_LAYER2.add_polygon(p_round, layer=waveguide_xs.layer)

        protection_rect2 = C << ROUNDED_PROTECTION_LAYER2
        protection_rect2.center = (nanowire.center[0], nanowire.center[1])

        # Add the first protection layer

        ROUNDED_PROTECTION_LAYER = gf.Component()
        protection_rect = C << ROUNDED_PROTECTION_LAYER
        PROTECTION_LAYER1 = gf.components.rectangle(
            size=(
                # channel_length,
                nanowire.xsize / 2,
                (9 + channel_width + channel_pitch),
            ),
            layer=waveguide_xs.layer,
        ).copy()
        for p in PROTECTION_LAYER1.get_polygons(layers=[waveguide_xs.layer])[
            gf.get_layer(waveguide_xs.layer)
        ]:
            p_round = p.round_corners(rinner, router, 200)
            ROUNDED_PROTECTION_LAYER.add_polygon(p_round, layer=waveguide_xs.layer)

        # Position the center over the center of the wire
        protection_rect.center = (
            nanowire.center[0] + channel_length / 2,
            nanowire.center[1],
        )
        protection_rect.xmin = protection_rect2.xmax - 2

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
def meander_snspd(
    channel_width: float = 0.5,
    channel_pitch: float = 0.3,
    size: tuple[float, float] = (5, 5),
    add_channel_protection: bool = True,
    fine_wire_cross_section: str = "nbtin",
    coarse_wire_cross_section: str = "course_nbtin",
    waveguide_cross_section: str = "strip",
) -> gf.Component:
    waveguide_xs = gf.get_cross_section(waveguide_cross_section)

    # Add the nanowire
    C = gf.Component()
    LINE = variable_length_meander_constriction(
        channel_width=channel_width,
        channel_pitch=channel_pitch,
        size=size,
        fine_cross_section=fine_wire_cross_section,
        coarse_cross_section=coarse_wire_cross_section,
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

    if add_channel_protection:
        rinner = 2000
        router = rinner

        # Add the second protection layer
        PROTECTION_LAYER2 = gf.components.rectangle(
            size=(
                waveguide_xs.radius / 15,
                nanowire.xsize,
            ),
            layer=waveguide_xs.layer,
        ).copy()
        ROUNDED_PROTECTION_LAYER2 = gf.Component()
        for p in PROTECTION_LAYER2.get_polygons(layers=[waveguide_xs.layer])[
            gf.get_layer(waveguide_xs.layer)
        ]:
            p_round = p.round_corners(rinner, router, 200)
            ROUNDED_PROTECTION_LAYER2.add_polygon(p_round, layer=waveguide_xs.layer)

        protection_rect2 = C << ROUNDED_PROTECTION_LAYER2
        protection_rect2.center = (nanowire.center[0], nanowire.center[1])

        # Add the first protection layer

        ROUNDED_PROTECTION_LAYER = gf.Component()
        protection_rect = C << ROUNDED_PROTECTION_LAYER
        PROTECTION_LAYER1 = gf.components.rectangle(
            size=(size[0] + 1, size[1] * 1.4 + 2),
            layer=waveguide_xs.layer,
        ).copy()
        for p in PROTECTION_LAYER1.get_polygons(layers=[waveguide_xs.layer])[
            gf.get_layer(waveguide_xs.layer)
        ]:
            p_round = p.round_corners(rinner, router, 200)
            ROUNDED_PROTECTION_LAYER.add_polygon(p_round, layer=waveguide_xs.layer)

        # Position the center over the center of the wire
        protection_rect.center = (
            nanowire.center[0] + channel_pitch / 2,
            nanowire.center[1],
        )
        protection_rect.xmin = protection_rect2.xmax - 2

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
