import gdsfactory as gf
from gdsfactory.get_factories import get_cells
from ...components import (
    bends,
    containers,
    couplers,
    geometries,
    markers,
    superconductors,
    texts,
    waveguides,
    rings,
    pads,
    mmi,
)

# Add all the default cells and some custom ones
DEMO_CELLS = get_cells(
    [
        # gf.components,
        couplers,
        markers,
        superconductors,
        bends,
        texts,
        waveguides,
        rings,
        pads,
        geometries,
        containers,
        mmi,
    ]
)

DEMO_CONTAINERS_DICT = get_cells(
    [
        gf.containers,
    ]
)
