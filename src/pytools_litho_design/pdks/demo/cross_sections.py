from functools import partial
import gdsfactory as gf
from gdsfactory.cross_section import port_names_electrical, port_types_electrical
from gdsfactory.cross_section import cross_section, CrossSection
from gdsfactory import typings

port_names_optical = ["o1", "o2"]
port_types_optical = ["optical", "optical"]


@gf.xsection
def xs_generic_neg_cross_section(
    width: float = 2,
    layer="asic",
    radius=1,
    port_names: list[str] = port_names_optical,
    port_types: list[str] = port_types_optical,
    trench_width=2,
    **kwargs,
):
    return gf.cross_section.CrossSection(
        radius=radius,
        sections=(
            gf.Section(
                width=width,
                offset=0,
                layer=layer,
                port_names=port_names,
                port_types=port_types,
                name="_default",
                hidden=True,
            ),
            gf.Section(
                width=trench_width,
                offset=1 / 2 * (width + trench_width),
                layer=layer,
                name="left_trench",
            ),
            gf.Section(
                width=trench_width,
                offset=-1 / 2 * (width + trench_width),
                layer=layer,
                name="right_trench",
            ),
        ),
        **kwargs,
    )


# Markers and pads
au = partial(
    gf.cross_section.metal1,
    layer="AU",
    port_names=port_names_electrical,
    port_types=port_types_electrical,
)
au_routing = partial(
    au,
    radius_min=80,
)
# neg_au = partial(
#     xs_generic_neg_cross_section,
#     layer="NEG_AU",
#     port_names=port_names_electrical,
#     port_types=port_types_electrical,
# )
# neg_au_routing = partial(neg_au, radius_min=80)

# Thermal oxide
sio2_bot = partial(gf.cross_section.strip, layer="SIO2_BOT")
# neg_sio2_bot = partial(
#     xs_generic_neg_cross_section,
#     layer="NEG_SIO2_BOT",
#     port_names=port_names_electrical,
#     port_types=port_types_electrical,
# )

# Waveguide cross sections
asic = partial(gf.cross_section.strip, layer="ASIC", width=0.8)
asic_routing = partial(asic, radius_min=100)

asic_sio2_rib = partial(
    gf.cross_section.rib,
    layer="ASIC",
    cladding_layers=["SIO2_TOP"],
    cladding_offsets=[3],
    width=0.8,
)
asic_sio2_rib_routing = partial(
    asic_sio2_rib,
    radius_min=100,
)

# neg_asic = partial(
#     xs_generic_neg_cross_section,
#     layer="NEG_ASIC",
#     port_names=port_names_optical,
#     port_types=port_types_optical,
# )

# neg_asic_routing = partial(
#     neg_asic,
#     radius_min=80,
# )

# Metal cross section
fine_nbtin = partial(
    gf.cross_section.metal1,
    layer="FINE_NBTIN",
    radius_min=20,
    port_names=port_names_electrical,
    port_types=port_types_electrical,
)
fine_nbtin_routing = partial(fine_nbtin, radius_min=80)
coarse_nbtin = partial(fine_nbtin, layer="COARSE_NBTIN", width=5)
coarse_nbtin_routing = partial(coarse_nbtin, radius_min=100)
# neg_nbtin = partial(nbtin, layer="NEG_NBTIN")
# neg_nbtin_routing = partial(neg_nbtin, layer="NEG_NBTIN")

ti = partial(
    gf.cross_section.metal1,
    layer="TI",
    port_names=port_names_electrical,
    port_types=port_types_electrical,
)
ti_routing = partial(ti, radius_min=100)
# neg_ti = partial(ti, layer="NEG_TI")
# neg_ti_routing = partial(ti_routing, layer="NEG_TI")

# Cladding layers
sio2_top = partial(gf.cross_section.strip, layer="SIO2_TOP")
neg_sio2_top = partial(gf.cross_section.strip, layer="NEG_SIO2_TOP")

DEMO_CROSS_SECTIONS = {
    "au": au,
    "au_routing": au_routing,
    # "neg_au": neg_au,
    # "neg_au_routing": neg_au_routing,
    "sio2_bot": sio2_bot,
    # "neg_sio2_bot": neg_sio2_bot,
    "asic": asic,
    "asic_routing": asic_routing,
    "asic_sio2_rib": asic_sio2_rib,
    "asic_sio2_rib_routing": asic_sio2_rib_routing,
    # "neg_asic": neg_asic,
    # "neg_asic_routing": neg_asic_routing,
    "fine_nbtin": fine_nbtin,
    "fine_nbtin_routing": fine_nbtin_routing,
    "coarse_nbtin": coarse_nbtin,
    "coarse_nbtin_routing": coarse_nbtin_routing,
    # "neg_nbtin": neg_nbtin,
    # "neg_nbtin_routing": neg_nbtin_routing,
    "ti": ti,
    "ti_routing": ti_routing,
    # "neg_ti": neg_ti,
    # "neg_ti_routing": neg_ti_routing,
    "sio2_top": sio2_top,
    "neg_sio2_top": neg_sio2_top,
}
