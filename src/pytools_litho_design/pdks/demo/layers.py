from gdsfactory.typings import Layer
from gdsfactory.technology import LayerLevel, LayerMap, LayerStack, LayerViews


class DEMO_LAYERS(LayerMap):
    WAFER: Layer = (999, 0)
    AU_PADS: Layer = (1, 0)  # Gold pads for wire bonding
    AU: Layer = (10, 0)
    NEG_NBTIN: Layer = (3, 0)  # Negative resist NBTIN for superconducting lines
    NBTIN: Layer = (4, 0)  # NBTIN layer for superconducting lines
    SIO2: Layer = (5, 0)  # Silicon dioxide for insulation
    ASIO2: Layer = (11, 0)
    SHALLOW_ETCH: Layer = (6, 0)  # Shallow etch for patterning
    DEEP_ETCH: Layer = (7, 0)  # Deep etch for patterning
    WAVEGUIDE: Layer = (8, 0)  # Waveguide layer for photonic circuits
    CLADDING: Layer = (9, 0)  # Cladding layer for waveguides


DEMO_PORT_MARKER_LAYER_TO_TYPE = {
    DEMO_LAYERS.AU_PADS: "dc",
    DEMO_LAYERS.AU: "dc",
    DEMO_LAYERS.NEG_NBTIN: "dc",
    DEMO_LAYERS.NBTIN: "dc",
    DEMO_LAYERS.SIO2: "optical",
    DEMO_LAYERS.ASIO2: "optical",
    DEMO_LAYERS.WAVEGUIDE: "optical",
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
