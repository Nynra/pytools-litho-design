from .layers import DEMO_LAYERS
from functools import partial
import gdsfactory as gf
from ...components.geometries.tapers import (
    electrical_taper,
    optical_taper,
    neg_electrical_taper,
    neg_optical_taper,
    taper_to_ridge,
    sine_taper,
)


# LAYER_CONNECTIVITY = [
#     ("NPP", "VIAC", "M1"),
#     ("PPP", "VIAC", "M1"),
#     ("M1", "VIA1", "M2"),
#     ("M2", "VIA2", "M3"),
# ]


DEMO_TRANSITIONS = {
    # Thermal Oxide
    DEMO_LAYERS.SIO2_BOT: partial(sine_taper, cross_section="sio2_bot"),
    # DEMO_LAYERS.NEG_SIO2_BOT: partial(neg_optical_taper, cross_section="neg_sio2_bot"),
    # Metals
    DEMO_LAYERS.FINE_NBTIN: partial(sine_taper, cross_section="fine_nbtin", length=20),
    DEMO_LAYERS.COARSE_NBTIN: partial(sine_taper, cross_section="coarse_nbtin"),
    DEMO_LAYERS.TI: partial(sine_taper, cross_section="ti"),
    # DEMO_LAYERS.NEG_TI: partial(neg_electrical_taper, cross_section="neg_ti"),
    # Waveguides
    DEMO_LAYERS.ASIC: partial(sine_taper, cross_section="asic"),
    # DEMO_LAYERS.NEG_ASIC: partial(neg_optical_taper, cross_section="neg_asic"),
    # Cladding
    DEMO_LAYERS.SIO2_TOP: partial(sine_taper, cross_section="sio2_top"),
    DEMO_LAYERS.NEG_SIO2_TOP: partial(neg_optical_taper, cross_section="neg_sio2_top"),
    # Markers and pads
    DEMO_LAYERS.AU: partial(sine_taper, cross_section="au"),
    # DEMO_LAYERS.NEG_AU: partial(neg_electrical_taper, cross_section="neg_au"),
    # Layer Transitions
    (DEMO_LAYERS.COARSE_NBTIN, DEMO_LAYERS.FINE_NBTIN): partial(
        taper_to_ridge,
        main_cross_section="fine_nbtin",
        slab_cross_section="coarse_nbtin",
        port_type="electrical",
        use_slab_port=True,
    ),
    (DEMO_LAYERS.FINE_NBTIN, DEMO_LAYERS.COARSE_NBTIN): partial(
        taper_to_ridge,
        main_cross_section="coarse_nbtin",
        slab_cross_section="fine_nbtin",
        port_type="electrical",
        use_slab_port=True,
    ),
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
