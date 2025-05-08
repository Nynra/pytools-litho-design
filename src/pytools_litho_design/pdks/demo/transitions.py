from .layers import DEMO_LAYERS
from functools import partial
import gdsfactory as gf
from ...components.transitions.tapers import (
    electrical_taper,
    optical_taper,
    taper_to_ridge,
)


# LAYER_CONNECTIVITY = [
#     ("NPP", "VIAC", "M1"),
#     ("PPP", "VIAC", "M1"),
#     ("M1", "VIA1", "M2"),
#     ("M2", "VIA2", "M3"),
# ]


DEMO_TRANSITIONS = {
    DEMO_LAYERS.AU: partial(
        electrical_taper,
        cross_section="au",
    ),
    # DEMO_LAYERS.NEG_AU: partial(electrical_taper, cross_section="neg_au"),
    DEMO_LAYERS.NBTIN: partial(
        electrical_taper,
        cross_section="nbtin",
    ),
    # DEMO_LAYERS.NEG_NBTIN: partial(
    #     electrical_taper,
    #     cross_section="neg_nbtin",
    # ),
    DEMO_LAYERS.TI: partial(
        electrical_taper,
        cross_section="ti",
    ),
    # DEMO_LAYERS.NEG_TI: partial(
    #     electrical_taper,
    #     cross_section="neg_ti",
    # ),
    DEMO_LAYERS.SIO2: partial(optical_taper, cross_section="sio2"),
    # DEMO_LAYERS.NEG_SIO2: partial(optical_taper, cross_section="neg_sio2"),
    DEMO_LAYERS.ASIC: partial(optical_taper, cross_section="asic"),
    # DEMO_LAYERS.NEG_ASIC: partial(optical_taper, cross_section="neg_asic"),
    DEMO_LAYERS.SHALLOW_ETCH: partial(optical_taper, cross_section="shallow_etch"),
    DEMO_LAYERS.DEEP_ETCH: partial(optical_taper, cross_section="deep_etch"),
    # Layer Transitions
    # (DEMO_LAYERS.NBTIN, DEMO_LAYERS.AU): partial(
    #     taper_to_ridge,
    #     layer_wg="NBTIN",
    #     layer_slab="AU",
    #     cross_section="au",
    #     port_type="electrical",
    #     use_slab_port=True,
    # ),
    # (DEMO_LAYERS.AU, DEMO_LAYERS.NBTIN): partial(
    #     taper_to_ridge,
    #     layer_wg="AU",
    #     layer_slab="NBTIN",
    #     cross_section="au",
    #     port_type="electrical",
    #     use_slab_port=True,
    # ),
    # (DEMO_LAYERS.SIO2, DEMO_LAYERS.CLADDING): partial(
    #     taper_to_ridge,
    #     layer_wg="SIO2",
    #     layer_slab="CLADDING",
    #     cross_section="sio2",
    #     port_type="optical",
    #     use_slab_port=False,
    # ),
}
