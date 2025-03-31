import gdsfactory as gf
import numpy as np


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


# if __name__ == "__main__":
#     import matplotlib.pyplot as plt

#     c = wg_to_snspd()
#     c.plot()
#     plt.show()
