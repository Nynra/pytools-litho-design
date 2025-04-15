from ...cross_sections import (
    strip,
    metal1,
    nbtin,
    waveguide,
    metal_routing,
    rib,
    neg_nbtin,
)

DEMO_CROSS_SECTIONS = {
    "strip": strip,
    "metal1": metal1,
    "nbtin": nbtin,
    "neg_nbtin": neg_nbtin,
    "waveguide": waveguide,
    "metal_routing": metal_routing,
    "rib": rib,
}
