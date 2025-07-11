import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.generic_tech import LAYER
from gdsfactory.typings import Float2, Layer

from gplugins.klayout.drc.write_drc import (
    check_area,
    check_density,
    check_enclosing,
    check_separation,
    check_space,
    check_width,
    write_drc_deck_macro,
)

rules = [
    # Everything on the wafer
    check_enclosing(width=1, layer1="WAFER", layer2="ASIC"),
    check_enclosing(width=1, layer1="WAFER", layer2="FINE_NBTIN"),
    check_enclosing(width=1, layer1="WAFER", layer2="COARSE_NBTIN"),
    # Waveguide rules
    check_width(layer="ASIC", value=0.1),
    check_space(layer="ASIC", value=0.5),
    check_area(layer="ASIC", value=0.01),
    # Metal rules
    # Pad rules
    # Cladding rules
]

drc_check_deck = write_drc_deck_macro(rules, layers=LAYER, shortcut="Ctrl+Shift+D")
