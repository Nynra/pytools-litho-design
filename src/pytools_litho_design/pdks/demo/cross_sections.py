from functools import partial
import gdsfactory as gf
from gdsfactory.cross_section import port_names_electrical, port_types_electrical
from gdsfactory.cross_section import cross_section, CrossSection
from gdsfactory import typings

# Waveguide cross sections
asic = partial(gf.cross_section.strip, layer="ASIC", radius_min=10)
asic_routing = partial(asic, radius=120, radius_min=100)
sio2 = partial(gf.cross_section.strip, layer="SIO2")
sio2_routing = partial(sio2, radius=120, radius_min=100)
neg_sio2_bot = partial(gf.cross_section.strip, layer="NEG_SIO2_BOT")
neg_sio2_top = partial(gf.cross_section.strip, layer="NEG_SIO2_TOP")

# Metal cross section
nbtin = partial(
    gf.cross_section.metal1,
    layer="NBTIN",
    radius_min=10,
    port_names=port_names_electrical,
    port_types=port_types_electrical,
)
nbtin_routing = partial(nbtin, radius_min=50)
# neg_nbtin = nbtin
# neg_nbtin_routing = nbtin_routing
au = partial(
    gf.cross_section.metal1,
    layer="AU",
    port_names=port_names_electrical,
    port_types=port_types_electrical,
    radius_min=100,
)
au_routing = partial(
    au,
    radius_min=100,
)
marker = au
ti = partial(
    gf.cross_section.metal1,
    layer="TI",
    port_names=port_names_electrical,
    port_types=port_types_electrical,
    radius_min=100,
)
ti_routing = partial(ti, radius_min=50)

# neg_au = au
# neg_au_routing = au_routing
shallow_etch = partial(gf.cross_section.metal1, layer="SHALLOW_ETCH", radius_min=10)
deep_etch = partial(gf.cross_section.metal1, layer="DEEP_ETCH", radius_min=10)

DEMO_CROSS_SECTIONS = {
    "marker": marker,
    "asic": asic,
    "asic_routing": asic_routing,
    "sio2": sio2,
    "sio2_routing": sio2_routing,
    "neg_sio2_bot": neg_sio2_bot,
    "neg_sio2_top": neg_sio2_top,
    "nbtin": nbtin,
    "nbtin_routing": nbtin_routing,
    "au": au,
    "au_routing": au_routing,
    "ti": ti,
    "ti_routing": ti_routing,
    "deep_etch": deep_etch,
}
