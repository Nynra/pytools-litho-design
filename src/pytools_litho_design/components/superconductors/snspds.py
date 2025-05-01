import gdsfactory as gf
import numpy as np
from gdsfactory.typings import Layer
from .constrictions import variable_length_constriction, spot_constriction
from gdsfactory.components.waveguides import straight as straight_waveguide
from typing import Union


@gf.cell
def straight_snspd(
    channel_w: float = 0.5,
    channel_l: float = 10,
    wire_cross_section: gf.CrossSection | str = "nbtin",
    anticrowding_factor: float = 1.2,
    waveguide_cross_section: gf.CrossSection | str = "strip",
) -> gf.Component:
    if isinstance(wire_cross_section, str):
        wire_cross_section = gf.get_cross_section(wire_cross_section)
    if isinstance(waveguide_cross_section, str):
        waveguide_cross_section = gf.get_cross_section(waveguide_cross_section)

    # Add the nanowire
    C = gf.Component()
    nanowire = C << variable_length_constriction(
        channel_w=channel_w,
        channel_l=channel_l,
        anticrowding_factor=anticrowding_factor,
        cross_section=wire_cross_section,
    )

    waveguide = C << straight_waveguide(
        cross_section=waveguide_cross_section,
        length=10,
    )

    # Position the waveguide in the middle of the nanowire
    waveguide.rotate(90)
    waveguide.center = (
        nanowire.xmin + nanowire.xsize / 2,
        nanowire.ymin + nanowire.ysize / 2,
    )

    # Add the ports
    for port in nanowire.ports:
        C.add_port(name=port.name, port=port, cross_section=wire_cross_section)
    for port in waveguide.ports:
        C.add_port(name=port.name, port=port, cross_section=waveguide_cross_section)

    return C


@gf.cell
def spot_snspd(
    channel_w: float = 0.5,
    wire_cross_section: Union[gf.CrossSection, str] = "metal1",
    anticrowding_factor: float = 1.2,
    waveguide_cross_section: Union[gf.CrossSection, str] = "strip",
    waveguide_extension: float = 0,
    add_output_grating: bool = False,
    output_grating: str | gf.Component = "grating_coupler_traditional",
) -> gf.Component:
    if isinstance(wire_cross_section, str):
        wire_cross_section = gf.get_cross_section(wire_cross_section)
    if isinstance(waveguide_cross_section, str):
        waveguide_cross_section = gf.get_cross_section(waveguide_cross_section)

    # Add the nanowire
    C = gf.Component()
    nanowire = C << spot_constriction(
        channel_w=channel_w,
        anticrowding_factor=anticrowding_factor,
        cross_section=wire_cross_section,
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

    # Add the ports
    if add_output_grating:
        if isinstance(output_grating, str):
            output_grating = gf.get_component(
                output_grating, cross_section=waveguide_cross_section
            )
        grating = C << output_grating
        grating.rotate(90)
        grating.connect(
            "o1",
            waveguide.ports["o2"],
        )
    else:
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

    for port in nanowire.ports:  # Nanowire ports
        C.add_port(name=port.name, port=port, cross_section=wire_cross_section)

    return C


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


# @gf.cell
# def wg_to_snspd(
#     wgnw_width=0.1,
#     wgnw_length=100,
#     wgnw_gap=0.15,
#     num_squares=5000.0,
#     meander_width=0.4,
#     meander_fill_factor=0.5,
#     wg_width=0.75,
#     layer=1,
# ):
#     """Waveguide coupled to SNSPD with inductor (meander).
#     The length and width of the meander are chosen so that it is approximately square

#     Args:
#         meander_width (float): nanowire width within meander inductor
#         num_squares (float): total squares in meander and out-and-back
#         wgnw_width (float): width of out-and-back nanowire
#         wgnw_length (float): length of out-and-back
#         wgnw_gap (float): spacing between the out-and-back wires
#         wg_width (float): waveguide width

#     Ports:
#         el_1: wiring port
#         el_gnd: wiring port
#         wg_in: input optical port
#         de_edge: edge of explicit waveguide on the SNSPD side
#     """

#     D = gf.Component()

#     # Calculations and checks
#     numsquares_wgnw = 2 * wgnw_length / wgnw_width
#     numsquares_meander = num_squares - numsquares_wgnw
#     if numsquares_meander < 1000:
#         print(
#             "Warning: Not enough squares in SNSPD meander. Clipped to 1000 from {:.1f}".format(
#                 numsquares_meander
#             )
#         )
#         numsquares_meander = 1000
#     meander_pitch = meander_width / meander_fill_factor
#     meander_length = np.sqrt(numsquares_meander * meander_width * meander_pitch)
#     wgnw_pitch = wgnw_width + wgnw_gap
#     wgnw_distance_to_edge = wg_width / 2 - wgnw_width - wgnw_gap / 2
#     if wgnw_distance_to_edge < 0:
#         print(
#             "Warning: nanowire will overhang side of waveguide by {:.3f} um".format(
#                 -wgnw_distance_to_edge
#             )
#         )

#     numsquares_per_taper = 3  # approximate
#     D.info["num_squares"] = (
#         numsquares_meander
#         + numsquares_wgnw
#         - meander_length / meander_width
#         + 3 * numsquares_per_taper
#     )
#     # D.info['expected_resistance'] = D.info['num_squares']*EXPECTED_RSQ_WSI
#     D.info["wire_width"] = wgnw_width
#     D.info["length"] = wgnw_length

#     # Geometry
#     meander = D << gf.components.superconductors.snspd(
#         wire_width=meander_width,
#         wire_pitch=meander_pitch,
#         terminals_same_side=False,
#         size=(meander_length, None),
#         num_squares=numsquares_meander,
#         layer=layer,
#     )
#     meander.mirror(p1=(0, 0), p2=(1, 0))

#     Taper = gf.components.superconductors.optimal_step(
#         start_width=wgnw_width,
#         end_width=meander_width,
#         num_pts=50,
#         width_tol=1e-3,
#         anticrowding_factor=1.2,
#         layer=layer,
#     )

#     # Due to a bug the ports are alsways set as optical
#     for port in Taper.ports:
#         port.port_type = "electrical"

#     taper1 = D << Taper
#     taper1.connect(1, meander.ports[0])

#     wgnw = D << gf.components.optimal_hairpin(
#         width=wgnw_width, pitch=wgnw_pitch, length=wgnw_length, layer=layer
#     )
#     wgnw.connect(1, taper1.ports[0])

#     taper2 = D << Taper
#     taper2.mirror()
#     taper2.connect(0, wgnw.ports[0])

#     # Electrical ports
#     exit_bend = D << gf.components.superconductors.optimal_90deg(
#         width=meander_width, num_pts=15, length_adjust=1, layer=layer
#     )
#     exit_bend.connect(1, taper2.ports[1])
#     D.add_port("el_gnd", port=exit_bend.ports[0])

#     exit_taper = D << gf.components.superconductors.optimal_step(
#         start_width=meander_width,
#         end_width=meander_width * 4,
#         num_pts=50,
#         width_tol=1e-3,
#         anticrowding_factor=1.2,
#         layer=layer,
#     )
#     exit_taper.connect(0, meander.ports[1])
#     D.add_port("el_1", port=exit_taper.ports[1])

#     # Waveguide and optical ports
#     wg = D << gf.components.compass(
#         size=[wgnw_length + wgnw_distance_to_edge, wg_width], layer=layer
#     )
#     wg.xmax = wgnw.xmax
#     wg.y = wgnw.y

#     D.add_port("de_edge", port=wg.ports["E"])
#     D.add_port("wg_in", port=wg.ports["W"])
#     D.ports["de_edge"].info["is_waveguide_edge"] = True

#     pos = D.ports["wg_in"].center
#     D.move(-1 * pos)

#     return D


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # c = spot_snspd()
    # c = rectangle_meander()
    # c.plot()
    # plt.show()
