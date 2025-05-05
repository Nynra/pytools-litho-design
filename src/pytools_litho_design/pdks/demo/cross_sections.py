from functools import partial
import gdsfactory as gf
from gdsfactory.cross_section import port_names_electrical, port_types_electrical
from gdsfactory.cross_section import cross_section, CrossSection
from gdsfactory import typings

# Waveguide cross sections
strip = partial(gf.cross_section.strip, width=0.5, layer="WAVEGUIDE")
waveguide_tight_corners = strip
waveguide_low_loss_routing = partial(
    gf.cross_section.strip, width=0.5, layer="WAVEGUIDE", radius_min=100
)
rib = partial(
    gf.cross_section.rib,
    width=0.5,
    layer="WAVEGUIDE",
    radius_min=100,
    cladding_layers=["CLADDING"],
    # cladding_offsets=(3,),
    # cladding_simplify=(50 * 10e-9,),
)

# Metal cross sections
nbtin = partial(
    gf.cross_section.metal1,
    width=10,
    layer="NBTIN",
    radius_min=10,
    port_names=port_names_electrical,
    port_types=port_types_electrical,
)
neg_nbtin = partial(
    gf.cross_section.metal1,
    width=10,
    radius_min=10,
    layer="NEG_NBTIN",
    port_names=port_names_electrical,
    port_types=port_types_electrical,
)
metal1 = nbtin
metal2 = neg_nbtin

au = partial(
    gf.cross_section.metal1,
    width=10,
    layer="AU",
    port_names=port_names_electrical,
    port_types=port_types_electrical,
)

au_pads = au

DEMO_CROSS_SECTIONS = {
    "waveguide_low_loss_routing": waveguide_low_loss_routing,
    "waveguide_tight_corners": waveguide_tight_corners,
    "strip": strip,
    "rib": rib,
    "nbtin": nbtin,
    "neg_nbtin": neg_nbtin,
    "metal1": metal1,
    "metal2": metal2,
    "au": au,
    "au_pads": au_pads,
}
