from functools import partial
import gdsfactory as gf
from gdsfactory.cross_section import port_names_electrical, port_types_electrical
from gdsfactory.cross_section import cross_section, CrossSection
from gdsfactory import typings

# Waveguide cross sections
sio2 = partial(gf.cross_section.strip, layer="SIO2")
sio2_rib = partial(gf.cross_section.rib, layer="SIO2", cladding_layers=["CLADDING"])
sio2_routing = partial(sio2, radius=120, radius_min=100)
sio_rib_routing = partial(sio2_rib, radius=120, radius_min=100)

nbtin = partial(
    gf.cross_section.metal1,
    width=10,
    layer="NBTIN",
    radius_min=10,
    port_names=port_names_electrical,
    port_types=port_types_electrical,
)

au = partial(
    gf.cross_section.metal1,
    width=10,
    layer="AU",
    port_names=port_names_electrical,
    port_types=port_types_electrical,
)

shallow_etch = partial(gf.cross_section.metal1, layer="SHALLOW_ETCH")
deep_etch = partial(gf.cross_section.metal1, layer="DEEP_ETCH")
cladding = partial(gf.cross_section.strip, layer="CLADDING")

# For compatibility with generic gdsfacoty models
strip = sio2
rib = sio2_rib
metal1 = nbtin
metal2 = au
metal_routing = au

DEMO_CROSS_SECTIONS = {
    "sio2": sio2,
    "sio2_rib": sio2_rib,
    "sio2_routing": sio2_routing,
    "sio_rib_routing": sio_rib_routing,
    "nbtin": nbtin,
    "au": au,
    "shallow_etch": shallow_etch,
    "deep_etch": deep_etch,
    "cladding": cladding,
    "strip": strip,
    "rib": rib,
    "metal1": metal1,
    "metal2": metal2,
    "metal_routing": metal_routing,
}
