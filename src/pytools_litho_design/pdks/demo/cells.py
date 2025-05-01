import gdsfactory as gf
from gdsfactory.get_factories import get_cells
from ...components import couplers, markers, superconductors, tapers


# Add all the default cells and some custom ones
DEMO_CELLS = get_cells(
    [
        gf.components,
        couplers,
        markers,
        superconductors,
        tapers,
    ]
)

DEMO_CONTAINERS_DICT = get_cells(
    [
        gf.containers,
    ]
)
