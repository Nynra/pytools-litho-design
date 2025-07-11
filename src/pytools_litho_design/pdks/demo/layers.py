from gdsfactory.typings import Layer
from gdsfactory.technology import LayerLevel, LayerMap, LayerStack, LayerViews


class DEMO_LAYERS(LayerMap):
    WAFER: Layer = (0, 0)
    SIO2_BOT: Layer = (1, 0)  # Silicon dioxide for cladding
    # NEG_SIO2_BOT: Layer = (2, 0)
    # Metals
    FINE_NBTIN: Layer = (3, 0)  # NBTIN layer for superconducting lines
    COARSE_NBTIN: Layer = (4, 0)
    TI: Layer = (5, 0)
    # NEG_TI: Layer = (6, 0)
    # Waveguides
    ASIC: Layer = (7, 0)  # Amorphous silicon carbide
    # NEG_ASIC: Layer = (8, 0)
    # Cladding
    SIO2_TOP: Layer = (9, 0)
    NEG_SIO2_TOP: Layer = (10, 0)
    # Markers and pads
    AU: Layer = (11, 0)
    # NEG_AU: Layer = (12, 0)


DEMO_PORT_MARKER_LAYER_TO_TYPE = {
    # Markers and pads
    DEMO_LAYERS.AU: "dc",
    # DEMO_LAYERS.NEG_AU: "dc",
    # Thermal Oxide
    DEMO_LAYERS.SIO2_BOT: "optical",
    # DEMO_LAYERS.NEG_SIO2_BOT: "optical",
    # Metals
    DEMO_LAYERS.FINE_NBTIN: "dc",
    DEMO_LAYERS.COARSE_NBTIN: "dc",
    DEMO_LAYERS.TI: "dc",
    # DEMO_LAYERS.NEG_TI: "dc",
    # Waveguides
    DEMO_LAYERS.ASIC: "optical",
    # DEMO_LAYERS.NEG_ASIC: "optical",
    # Cladding
    DEMO_LAYERS.SIO2_TOP: "optical",
    DEMO_LAYERS.NEG_SIO2_TOP: "optical",
}

DEMO_PORT_LAYER_TO_TYPE = DEMO_PORT_MARKER_LAYER_TO_TYPE

PORT_TYPE_TO_MARKER_LAYER = {v: k for k, v in DEMO_PORT_MARKER_LAYER_TO_TYPE.items()}


# LAYER_CONNECTIVITY = [
#     ("NPP", "VIAC", "M1"),
#     ("PPP", "VIAC", "M1"),
#     ("M1", "VIA1", "M2"),
#     ("M2", "VIA2", "M3"),
# ]
