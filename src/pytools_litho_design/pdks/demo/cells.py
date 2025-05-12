import gdsfactory as gf
from gdsfactory.get_factories import get_cells
from ...components import (
    couplers,
    geometries,
    markers,
    superconductors,
    rings,
    pads,
)

# Add all the default cells and some custom ones
DEMO_CELLS = get_cells(
    [
        # gf.components,
        couplers,
        markers,
        superconductors,
        rings,
        pads,
        geometries,
    ]
)

DEMO_CONTAINERS_DICT = get_cells(
    [
        gf.containers,
    ]
)
