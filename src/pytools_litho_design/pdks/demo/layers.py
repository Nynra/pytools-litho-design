from gdsfactory.typings import Layer
from gdsfactory.technology import LayerLevel, LayerMap, LayerStack, LayerViews


class DEMO_LAYERS(LayerMap):
    WAFER: Layer = (999, 0)
    AU_PADS: Layer = (1, 0)  # Gold pads for wire bonding
    MARKERS: Layer = (2, 0)  # Markers for alignment and registration
    NEG_NBTIN: Layer = (3, 0)  # Negative resist NBTIN for superconducting lines
    NBTIN: Layer = (4, 0)  # NBTIN layer for superconducting lines
    SIO2: Layer = (5, 0)  # Silicon dioxide for insulation
    SHALLOW_ETCH: Layer = (6, 0)  # Shallow etch for patterning
    DEEP_ETCH: Layer = (7, 0)  # Deep etch for patterning
    WAVEGUIDE: Layer = (8, 0)  # Waveguide layer for photonic circuits
    CLADDING: Layer = (9, 0)  # Cladding layer for waveguides
