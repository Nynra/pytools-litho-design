import gdsfactory as gf
from functools import cache


@cache
def get_demo_pdk(activate: bool = False) -> gf.Pdk:
    import gdsfactory as gf

    from .layers import (
        DEMO_LAYERS,
        DEMO_PORT_MARKER_LAYER_TO_TYPE,
        DEMO_PORT_LAYER_TO_TYPE,
    )
    from .transitions import DEMO_TRANSITIONS
    from .cells import DEMO_CELLS, DEMO_CONTAINERS_DICT
    from .cross_sections import DEMO_CROSS_SECTIONS

    DEMO_CONSTANTS = {
        "fiber_input_to_output_spacing": 200,
        "metal_spacing": 10,
        "pad_pitch": 100,
        "pad_size": (100, 100),
    }

    generic_pdk = gf.generic_tech.get_generic_pdk()
    pdk = gf.Pdk(
        name="demo",
        layers=DEMO_LAYERS,
        layer_views=generic_pdk.layer_views,
        layer_transitions=DEMO_TRANSITIONS,
        constants=DEMO_CONSTANTS,
        cross_sections=DEMO_CROSS_SECTIONS,
        cells=DEMO_CELLS,
        containers=DEMO_CONTAINERS_DICT,
    )

    if activate:
        pdk.activate()

    return pdk
