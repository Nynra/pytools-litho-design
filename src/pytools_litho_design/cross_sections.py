from gdsfactory.cross_section import cross_section, strip
import gdsfactory as gf
import gdsfactory.typings as typings
from gdsfactory.cross_section import CrossSection
from gdsfactory.cross_section import port_names_electrical, port_types_electrical


@gf.xsection
def waveguide(
    width: float = 0.5,
    layer: typings.LayerSpec = "WAVEGUIDE",
    radius: float = 10.0,
    radius_min: float = 5,
    **kwargs: typings.Any,
) -> CrossSection:
    """Return Waveguide cross section."""
    return cross_section(
        width=width,
        layer=layer,
        radius=radius,
        radius_min=radius_min,
        **kwargs,
    )


@gf.xsection
def strip(
    width: float = 0.5,
    layer: typings.LayerSpec = "WAVEGUIDE",
    radius: float = 10.0,
    radius_min: float = 5,
    **kwargs: typings.Any,
) -> CrossSection:
    """Return Waveguide cross section."""
    return waveguide(
        width=width,
        layer=layer,
        radius=radius,
        radius_min=radius_min,
        **kwargs,
    )


@gf.xsection
def rib(
    width: float = 0.5,
    layer: typings.LayerSpec = "WAVEGUIDE",
    radius: float = 10.0,
    radius_min: float | None = None,
    cladding_layers: typings.LayerSpecs = ("CLADDING",),
    cladding_offsets: typings.Floats = (3,),
    cladding_simplify: typings.Floats = (50 * 10e-9,),
    **kwargs: typings.Any,
) -> CrossSection:
    """Return Rib cross_section."""
    return cross_section(
        width=width,
        layer=layer,
        radius=radius,
        radius_min=radius_min,
        cladding_layers=cladding_layers,
        cladding_offsets=cladding_offsets,
        cladding_simplify=cladding_simplify,
        **kwargs,
    )


def nbtin(
    width: float = 10,
    layer: typings.LayerSpec = "NEG_NBTIN",
    radius: float | None = None,
    port_names: typings.IOPorts = port_names_electrical,
    port_types: typings.IOPorts = port_types_electrical,
    **kwargs: typings.Any,
) -> CrossSection:
    """Return NbTiN Strip cross_section."""
    return cross_section(
        width=width,
        layer=layer,
        radius=radius,
        port_names=port_names,
        port_types=port_types,
        **kwargs,
    )


@gf.xsection
def metal1(
    width: float = 10,
    layer: typings.LayerSpec = "NEG_NBTIN",
    radius: float | None = None,
    port_names: typings.IOPorts = port_names_electrical,
    port_types: typings.IOPorts = port_types_electrical,
    **kwargs: typings.Any,
) -> CrossSection:
    """Return NbTiN Strip cross_section."""
    return nbtin(
        width=width,
        layer=layer,
        radius=radius,
        port_names=port_names,
        port_types=port_types,
        **kwargs,
    )


@gf.xsection
def metal_routing(
    width: float = 10,
    layer: typings.LayerSpec = "NEG_NBTIN",
    radius: float | None = None,
    port_names: typings.IOPorts = port_names_electrical,
    port_types: typings.IOPorts = port_types_electrical,
    **kwargs: typings.Any,
) -> CrossSection:
    """Return Metal Strip cross_section."""
    return cross_section(
        width=width,
        layer=layer,
        radius=radius,
        port_names=port_names,
        port_types=port_types,
        **kwargs,
    )
