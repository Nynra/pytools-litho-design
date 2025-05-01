# import gdsfactory as gf


# def directional_coupler(
#     wg_port,
#     cell,
#     Pattern_layer=1,
#     Heater_layer=10,
#     Gold_layer=8,
#     waveguide_width=1,
#     Gap=0.3,
#     waveguide_length=10,
#     coupling_length=30,
#     Thermo_Length=250,
#     Heater=1,
#     Thermo_coupler_loc="Right",
# ):
#     ######
#     contact_width = 200

#     # Grating Coupler
#     origin = wg_port.current_port.origin

#     angle = wg_port.current_port.angle

#     splitter_length = 100
#     splitter_width = 100
#     splitter = gf.components.mmi1x2(
#         origin=origin,
#         angle=angle,
#         total_length=splitter_length,
#         wg_width_root=1,
#         sep=splitter_width + Gap + waveguide_width,
#     )

#     waveguide_2 = Waveguide.make_at_port(splitter.right_branch_port)
#     waveguide_2.add_straight_segment(length=Thermo_Length)

#     # DC2 = DirectionalCoupler.make_at_port(
#     #     port=waveguide_2.current_port,
#     #     length=coupling_length,
#     #     gap=Gap,
#     #     bend_radius=splitter_width / 4,
#     #     bend_angle=pi / 2,
#     #     which=0,
#     # )
#     DC2 = gf.components.couplers.coupler_full(
#         length=coupling_length,
#         gap=Gap,
#         dw=0.1,
#         cladding_layers=[(Pattern_layer, 0)],
#         cladding_offsets=[3],
#         cross_section="strip",
#     )

#     waveguide_3 = Waveguide.make_at_port(DC2.right_ports[0])

#     waveguide_3.add_straight_segment(length=waveguide_length)

#     waveguide_4 = Waveguide.make_at_port(DC2.right_ports[1])
#     waveguide_4.add_straight_segment(length=waveguide_length)

#     waveguide_6 = Waveguide.make_at_port(splitter.left_branch_port)
#     waveguide_6.add_straight_segment(length=Thermo_Length)

#     cell.add_to_layer(Pattern_layer, DC2, splitter, waveguide_2, waveguide_6)

#     # text1 = Text((center_x, center_y+35+4*bend_radius), height=20, text='Width:'+str(waveguide_width)+' Gap:'+str(Gap)+' CL:'+str(coupling_length)+' Radius:'+str(bend_radius)+' TL:'+str(Thermo_Length), alignment='left-top', angle=0.0, font='stencil', line_spacing=2, true_bbox_alignment=False)
#     # cell.add_to_layer(Text_layer,text1)
#     #######
#     # Heater

#     if Thermo_coupler_loc == "Right":
#         if Heater == 1:
#             Heater_1 = Waveguide.make_at_port(
#                 splitter.right_branch_port, angle=angle, width=waveguide_width
#             )
#             Heater_1.add_straight_segment(length=Thermo_Length)
#             Heater_1.add_bend(-1 * np.pi / 2, 10)
#             Gold_layer_1 = Waveguide.make_at_port(
#                 Heater_1.current_port,
#                 angle=Heater_1.current_port.angle,
#                 width=waveguide_width,
#             )

#             Heater_1.add_straight_segment(contact_width, final_width=contact_width)
#             Gold_layer_1.add_straight_segment(contact_width, final_width=contact_width)
#             # Heater_1.add_straight_segment(contact_width)

#             Heater_2 = Waveguide.make_at_port(
#                 splitter.right_branch_port, angle=angle - np.pi, width=waveguide_width
#             )
#             Heater_2.add_bend(np.pi / 2, 10)
#             Gold_layer_2 = Waveguide.make_at_port(
#                 Heater_2.current_port,
#                 angle=Heater_2.current_port.angle,
#                 width=waveguide_width,
#             )
#             Heater_2.add_straight_segment(contact_width, final_width=contact_width)
#             Gold_layer_2.add_straight_segment(contact_width, final_width=contact_width)
#             # Heater_2.add_straight_segment(contact_width)
#             Heater_all = geometric_union([Heater_1, Heater_2])
#             cell.add_to_layer(Heater_layer, Heater_all)

#             Gold_all = geometric_union([Gold_layer_1, Gold_layer_2])
#             cell.add_to_layer(Gold_layer, Gold_all)
#     if Thermo_coupler_loc == "Left":
#         if Heater == 1:
#             Heater_1 = Waveguide.make_at_port(
#                 splitter.left_branch_port, angle=angle, width=waveguide_width
#             )
#             Heater_1.add_straight_segment(length=Thermo_Length)
#             Heater_1.add_bend(1 * np.pi / 2, 10)
#             Gold_layer_1 = Waveguide.make_at_port(
#                 Heater_1.current_port,
#                 angle=Heater_1.current_port.angle,
#                 width=waveguide_width,
#             )

#             Heater_1.add_straight_segment(contact_width, final_width=contact_width)
#             Gold_layer_1.add_straight_segment(contact_width, final_width=contact_width)
#             # Heater_1.add_straight_segment(contact_width)

#             Heater_2 = Waveguide.make_at_port(
#                 splitter.left_branch_port, angle=angle + np.pi, width=waveguide_width
#             )
#             Heater_2.add_bend(-1 * np.pi / 2, 10)
#             Gold_layer_2 = Waveguide.make_at_port(
#                 Heater_2.current_port,
#                 angle=Heater_2.current_port.angle,
#                 width=waveguide_width,
#             )
#             Heater_2.add_straight_segment(contact_width, final_width=contact_width)
#             Gold_layer_2.add_straight_segment(contact_width, final_width=contact_width)
#             # Heater_2.add_straight_segment(contact_width)
#             Heater_all = geometric_union([Heater_1, Heater_2])
#             cell.add_to_layer(Heater_layer, Heater_all)

#             Gold_all = geometric_union([Gold_layer_1, Gold_layer_2])
#             cell.add_to_layer(Gold_layer, Gold_all)

#     return waveguide_3, waveguide_4
