from .layers import DEMO_LAYERS
from functools import partial
import gdsfactory as gf
from ...components.tapers.tapers import (
    electrical_transition_taper,
    optical_transition_taper,
    electrical_taper,
    optical_taper,
    taper,
)


# LAYER_CONNECTIVITY = [
#     ("NPP", "VIAC", "M1"),
#     ("PPP", "VIAC", "M1"),
#     ("M1", "VIA1", "M2"),
#     ("M2", "VIA2", "M3"),
# ]


DEMO_TRANSITIONS = {
    # In layer tapers for auto tapering
    DEMO_LAYERS.AU_PADS: partial(
        electrical_taper,
        layer=DEMO_LAYERS.AU_PADS,
        port_names=("e1", "e2"),
        port_types=("electrical", "electrical"),
    ),
    DEMO_LAYERS.AU: partial(
        electrical_taper,
        layer=DEMO_LAYERS.AU,
        port_names=("e1", "e2"),
        port_types=("electrical", "electrical"),
    ),
    DEMO_LAYERS.NEG_NBTIN: partial(
        electrical_taper,
        layer=DEMO_LAYERS.NEG_NBTIN,
        port_names=("e1", "e2"),
        port_types=("electrical", "electrical"),
    ),
    DEMO_LAYERS.NBTIN: partial(
        electrical_taper,
        cross_section="nbtin",
        port_names=("e1", "e2"),
        port_types=("electrical", "electrical"),
    ),
    # Layer Transitions
    (DEMO_LAYERS.NEG_NBTIN, DEMO_LAYERS.AU_PADS): partial(
        electrical_transition_taper,
        cross_section_start="neg_nbtin",
        cross_section_end="au_pads",
    ),
    (DEMO_LAYERS.NEG_NBTIN, DEMO_LAYERS.AU): partial(
        electrical_transition_taper,
        cross_section_start="neg_nbtin",
        cross_section_end="au",
    ),
    (DEMO_LAYERS.NEG_NBTIN, DEMO_LAYERS.NBTIN): partial(
        electrical_transition_taper,
        cross_section_start="neg_nbtin",
        cross_section_end="nbtin",
    ),
    (DEMO_LAYERS.NBTIN, DEMO_LAYERS.AU_PADS): partial(
        electrical_transition_taper,
        cross_section_start="nbtin",
        cross_section_end="au_pads",
    ),
    (DEMO_LAYERS.NBTIN, DEMO_LAYERS.AU): partial(
        electrical_transition_taper,
        cross_section_start="nbtin",
        cross_section_end="au",
    ),
}
