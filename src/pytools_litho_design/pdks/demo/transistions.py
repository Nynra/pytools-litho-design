from .layers import DEMO_LAYERS
from functools import partial
import gdsfactory as gf
from ...components.tapers.transition_tapers import (
    taper_nbtin_au,
    taper_au_nbtin,
)


# LAYER_CONNECTIVITY = [
#     ("NPP", "VIAC", "M1"),
#     ("PPP", "VIAC", "M1"),
#     ("M1", "VIA1", "M2"),
#     ("M2", "VIA2", "M3"),
# ]


DEMO_TRANSITIONS = {
    DEMO_LAYERS.AU_PADS: partial(
        gf.components.taper_electrical,
        layer=DEMO_LAYERS.AU_PADS,
        port_names=("e1", "e2"),
        port_types=("electrical", "electrical"),
    ),
    DEMO_LAYERS.NEG_NBTIN: partial(
        gf.components.taper_electrical,
        layer=DEMO_LAYERS.NEG_NBTIN,
        port_names=("e1", "e2"),
        port_types=("electrical", "electrical"),
    ),
    DEMO_LAYERS.NBTIN: partial(
        gf.components.taper_electrical,
        layer=DEMO_LAYERS.NBTIN,
        port_names=("e1", "e2"),
        port_types=("electrical", "electrical"),
    ),
    (DEMO_LAYERS.NEG_NBTIN, DEMO_LAYERS.AU_PADS): partial(
        taper_nbtin_au,
        layer_nbtin=DEMO_LAYERS.NEG_NBTIN,
        layer_au=DEMO_LAYERS.AU_PADS,
        cross_section=gf.cross_section.metal_routing(layer=DEMO_LAYERS.NEG_NBTIN),
    ),
    (DEMO_LAYERS.AU_PADS, DEMO_LAYERS.NEG_NBTIN): partial(
        taper_au_nbtin,
        layer_nbtin=DEMO_LAYERS.NEG_NBTIN,
        layer_au=DEMO_LAYERS.AU_PADS,
        cross_section=gf.cross_section.metal_routing(layer=DEMO_LAYERS.NEG_NBTIN),
    ),
}
