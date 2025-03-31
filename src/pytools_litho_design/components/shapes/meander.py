"""Layouts for resistors and resistors with superconducting contacts."""

import numpy as np

import gdsfactory as gf
from typing import Tuple, Optional


# def meander(
#     width: float = 2,
#     pitch: float = 4,
#     squares: float = 100,
#     max_length: Optional[float] = 20,
#     layer: int = 1,
# ) -> gf.Component:
#     """Create resistor meander with specified number of squares.

#     If squares*width > max_length or max_length is None, meander the resistor,
#     otherwise just return a straight line.

#     Args:
#         width (float): wire width in microns
#         pitch (float): desired pitch of meander in microns
#         squares (float or None): desired number of squares
#         max_length (float): desired length of device
#         layer (int): GDS layer

#     Returns:
#         D (Device): the resistor meander
#     """
#     D = gf.Component()

#     meander_spacing = (pitch - width) / width

#     if max_length is None or width * squares < max_length:
#         # just make a straight
#         return gf.components.straight(size=(width, width * squares), layer=layer)

#     # make meander
#     def hairpin(hp_length):
#         """Create hairpin used in meander."""
#         H = gf.Component()
#         straight = gf.components.rectangle(size=(hp_length - width, width), layer=layer)
#         conn = gf.components.rectangle(
#             size=(width, (2 + meander_spacing) * width), layer=layer
#         )
#         for i in range(2):
#             s = H << straight
#             s.move((-s.xmax, -s.ymin + (1 + meander_spacing) * width * i))
#         c = H << conn
#         c.move((-c.xmin, -c.ymin))
#         H.add_port(
#             name="1",
#             center=(-hp_length + width, width / 2),
#             width=width,
#             orientation=180,
#             layer=layer,
#         )
#         H.add_port(
#             name="2",
#             center=(-hp_length + width, (1 + meander_spacing) * width + width / 2),
#             width=width,
#             orientation=180,
#             layer=layer,
#         )
#         return H

#     def stub(orientation):
#         """Create stub to connect to meander ends."""
#         S = gf.Component()
#         straight = gf.components.rectangle(size=(width, 2 * width), layer=layer)
#         s = S << straight
#         s.move((-s.x, -s.ymin))
#         S.add_port(
#             name="1",
#             center=(0, width / 2),
#             width=width,
#             orientation=orientation,
#             layer=layer,
#         )
#         S.add_port(
#             name="2", center=(0, 2 * width), width=width, orientation=90, layer=layer
#         )
#         return S

#     # solve system for hairpin length (hp_length), number of (double) turns (n_turn),
#     # meander width (width_m) given:
#     #   - meander height (height),
#     #   - number of squares (squares),
#     #   - meander pitch (pitch),
#     #   - wire width (width)
#     n_turn = int(np.ceil((max_length - 3 * width) / pitch))
#     # calculate the hairpin length
#     # correction of 1.09 is the total number of squares contributed by the two
#     # corners of the hairpin
#     # ================+
#     #                 |
#     # ================+
#     # = : squares / n_turn squares
#     # | : (pitch - width) / width squares
#     # + : 1.09 squares
#     # squares - 3.09 for corners connecting meander to contacts
#     # these contributions lead to the following equation for the toal number of squares
#     # n_turn * (2*hp_length/width + 1.09 + (pitch - width) / width) = squares - 3.09
#     hp_length = (
#         (squares - 3.09) / n_turn - 1.09 - (pitch - width) / width
#     ) * width / 2 + width
#     hp = hairpin(hp_length)
#     hp_prev = None
#     for i in range(n_turn):
#         hp_i = D << hp
#         if hp_prev is not None:
#             hp_i.connect(hp_i.ports[str(2 - (i % 2))], hp_prev.ports[str(2 - (i % 2))])
#         else:
#             stub_top = D << stub(0)
#             stub_top.connect(stub_top.ports["1"], hp_i.ports["2"])
#         hp_prev = hp_i
#     stub_bot = D << stub(180 * (n_turn % 2))
#     stub_bot.connect(stub_bot.ports["1"], hp_prev.ports[str(2 - (n_turn % 2))])
#     E = gf.Component()
#     E.add_port(name="1", port=stub_top.ports["2"])
#     E.add_port(name="2", port=stub_bot.ports["2"])
#     E.info = locals()
#     return E
