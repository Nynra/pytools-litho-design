from gdsfactory.typings import Layer
from gdsfactory.technology import LayerLevel, LayerMap, LayerStack, LayerViews


class DEMO_LAYERS(LayerMap):
    WAFER: Layer = (899, 0)
    AU: Layer = (1, 0)
    # NEG_AU: Layer = (2, 0)
    NBTIN: Layer = (3, 0)  # NBTIN layer for superconducting lines
    # NEG_NBTIN: Layer = (4, 0)
    TI: Layer = (5, 0)
    # NEG_TI: Layer = (6, 0)
    SIO2: Layer = (7, 0)  # Silicon dioxide for insulation
    NEG_SIO2_BOT: Layer = (8, 0)
    NEG_SIO2_TOP: Layer = (9, 0)
    ASIC: Layer = (10, 0)  # Amorphous silicon carbide
    # NEG_ASIC: Layer = (10, 0)
    SHALLOW_ETCH: Layer = (11, 0)  # Shallow etch for patterning
    DEEP_ETCH: Layer = (12, 0)  # Deep etch for patterning


DEMO_PORT_MARKER_LAYER_TO_TYPE = {
    DEMO_LAYERS.AU: "dc",
    # DEMO_LAYERS.NEG_AU: "dc",
    DEMO_LAYERS.NBTIN: "dc",
    # DEMO_LAYERS.NEG_NBTIN: "dc",
    DEMO_LAYERS.TI: "dc",
    # DEMO_LAYERS.NEG_TI: "dc",
    DEMO_LAYERS.SIO2: "optical",
    DEMO_LAYERS.NEG_SIO2_BOT: "optical",
    DEMO_LAYERS.NEG_SIO2_TOP: "optical",
    DEMO_LAYERS.ASIC: "optical",
    # DEMO_LAYERS.NEG_ASIC: "optical",
    DEMO_LAYERS.SHALLOW_ETCH: "optical",
    DEMO_LAYERS.DEEP_ETCH: "optical",
}

DEMO_PORT_LAYER_TO_TYPE = DEMO_PORT_MARKER_LAYER_TO_TYPE

PORT_TYPE_TO_MARKER_LAYER = {v: k for k, v in DEMO_PORT_MARKER_LAYER_TO_TYPE.items()}


# LAYER_CONNECTIVITY = [
#     ("NPP", "VIAC", "M1"),
#     ("PPP", "VIAC", "M1"),
#     ("M1", "VIA1", "M2"),
#     ("M2", "VIA2", "M3"),
# ]
