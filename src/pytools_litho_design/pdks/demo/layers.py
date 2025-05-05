from gdsfactory.typings import Layer
from gdsfactory.technology import LayerLevel, LayerMap, LayerStack, LayerViews


class DEMO_LAYERS(LayerMap):
    WAFER: Layer = (999, 0)
    AU: Layer = (10, 0)
    NBTIN: Layer = (4, 0)  # NBTIN layer for superconducting lines
    SIO2: Layer = (5, 0)  # Silicon dioxide for insulation
    SHALLOW_ETCH: Layer = (6, 0)  # Shallow etch for patterning
    DEEP_ETCH: Layer = (7, 0)  # Deep etch for patterning
    CLADDING: Layer = (9, 0)  # Cladding layer for waveguides


DEMO_PORT_MARKER_LAYER_TO_TYPE = {
    DEMO_LAYERS.AU: "dc",
    DEMO_LAYERS.NBTIN: "dc",
    DEMO_LAYERS.SIO2: "optical",
    DEMO_LAYERS.SHALLOW_ETCH: "optical",
    DEMO_LAYERS.DEEP_ETCH: "optical",
    DEMO_LAYERS.CLADDING: "optical",
}

DEMO_PORT_LAYER_TO_TYPE = DEMO_PORT_MARKER_LAYER_TO_TYPE

PORT_TYPE_TO_MARKER_LAYER = {v: k for k, v in DEMO_PORT_MARKER_LAYER_TO_TYPE.items()}


# LAYER_CONNECTIVITY = [
#     ("NPP", "VIAC", "M1"),
#     ("PPP", "VIAC", "M1"),
#     ("M1", "VIA1", "M2"),
#     ("M2", "VIA2", "M3"),
# ]
