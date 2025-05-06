import gdsfactory as gf
from gdsfactory.get_factories import get_cells
from ...components import (
    couplers,
    markers,
    superconductors,
    transitions,
    bends,
    texts,
    waveguides,
    rings,
    pads,
    geometries,
    dies,
)

# Add all the default cells and some custom ones
DEMO_CELLS = get_cells(
    [
        # gf.components,
        couplers,
        markers,
        superconductors,
        transitions,
        bends,
        texts,
        waveguides,
        rings,
        pads,
        geometries,
        dies,
    ]
)

DEMO_CONTAINERS_DICT = get_cells(
    [
        gf.containers,
    ]
)
