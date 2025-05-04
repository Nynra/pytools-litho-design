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
    cladding_layers="CLADDING",
    cladding_offsets=(3,),
    cladding_simplify=(50 * 10e-9,),
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
    layer="NBTIN_NEG",
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


# @gf.xsection
# def waveguide(
#     width: float = 0.5,
#     layer: typings.LayerSpec = "WAVEGUIDE",
#     radius: float = 120,
#     radius_min: float = 100,
#     **kwargs: typings.Any,
# ) -> CrossSection:
#     """Return Waveguide cross section.

#     Create a waveguide without cladding.

#     Returns
#     -------
#     CrossSection
#         A cross-section object representing the waveguide.
#     """
#     return cross_section(
#         width=width,
#         layer=layer,
#         radius=radius,
#         radius_min=radius_min,
#         **kwargs,
#     )


# @gf.xsection
# def strip(
#     width: float = 0.5,
#     layer: typings.LayerSpec = "WAVEGUIDE",
#     radius: float = 100,
#     radius_min: float = 100,
#     **kwargs: typings.Any,
# ) -> CrossSection:
#     """Return Waveguide cross section.

#     This cross section is an alias for the waveguide cross section.
#     """
#     return waveguide(
#         width=width,
#         layer=layer,
#         radius=radius,
#         radius_min=radius_min,
#         **kwargs,
#     )


# @gf.xsection
# def rib(
#     width: float = 0.5,
#     layer: typings.LayerSpec = "WAVEGUIDE",
#     radius: float = 100,
#     radius_min: float | None = 100,
#     cladding_layers: typings.LayerSpecs = ("CLADDING",),
#     cladding_offsets: typings.Floats = (3,),
#     cladding_simplify: typings.Floats = (50 * 10e-9,),
#     **kwargs: typings.Any,
# ) -> CrossSection:
#     """Return Rib cross_section.

#     The rib cross section is an extension of the waveguide cross section
#     with additional cladding layers. It is used to create a ribbed
#     structure for optical waveguides.

#     Parameters
#     ----------
#     width : float
#         Width of the rib (waveguides).
#     layer : str
#         Layer name for the rib.
#     radius : float
#         Radius used for bends in the routing of the rib.
#     radius_min : float or None
#         Minimum acceptable bend radius. If None, no minimum is set.
#     cladding_layers : list of str
#         List of layer names for the cladding layers.
#     cladding_offsets : list of float
#         List of offsets for the cladding layers.
#     cladding_simplify : list of float
#         List of tolerances for the cladding simplification algorithm.
#         All points that can be removed without changing the resulting
#         polygon by more than the value listed here will be removed.
#     kwargs : dict
#         Additional parameters for the cross-section that will be passed
#         to the :func:`gf.cross_sections.cross_section` function.

#     Returns
#     -------
#     CrossSection
#         A cross-section object representing the rib.
#     """
#     return cross_section(
#         width=width,
#         layer=layer,
#         radius=radius,
#         radius_min=radius_min,
#         cladding_layers=cladding_layers,
#         cladding_offsets=cladding_offsets,
#         cladding_simplify=cladding_simplify,
#         **kwargs,
#     )


# @gf.xsection
# def nbtin(
#     width: float = 10,
#     layer: typings.LayerSpec = "NBTIN",
#     radius: float | None = None,
#     port_names: typings.IOPorts = port_names_electrical,
#     port_types: typings.IOPorts = port_types_electrical,
#     **kwargs: typings.Any,
# ) -> CrossSection:
#     """Return NbTiN Strip cross_section."""
#     return cross_section(
#         width=width,
#         layer=layer,
#         radius=radius,
#         port_names=port_names,
#         port_types=port_types,
#         **kwargs,
#     )


# @gf.xsection
# def neg_nbtin(
#     width: float = 10,
#     layer: typings.LayerSpec = "NEG_NBTIN",
#     bbox_offsets: typings.Floats = (0,),
#     bbox_layers: typings.LayerSpecs = ("NEG_NBTIN",),
#     radius: float | None = None,
#     port_names: typings.IOPorts = port_names_electrical,
#     port_types: typings.IOPorts = port_types_electrical,
#     **kwargs: typings.Any,
# ) -> CrossSection:
#     """Return Negative NbTiN Strip cross_section.

#     The negative NbTiN cross-section is used for the negative
#     NbTiN layer process where a film of NbTiN is deposited on the
#     substrate and then etched to create the desired pattern.

#     Parameters
#     ----------
#     width : float
#         Width of the strip.
#     layer : str
#         Layer name for the strip.
#     bbox_offsets : list of float
#         List of offsets for the bounding box layers. This is the gap that
#         will be left between the strip and the surrounding material.
#     bbox_layers : list of str
#         List of layer names for the bounding box layers. These layers
#         will be used to create the bounding box around the strip.
#     radius : float or None, optional
#         Radius used for bends in the routing of the strip. If None, no bends are
#         created. Defaults to None.
#     port_names : list, optional
#         List of port names for the strip. Defaults to electrical ports.
#     port_types : list, optional
#         List of port types for the strip. Defaults to electrical ports.
#     kwargs : dict
#         Additional parameters for the cross-section that will be passed
#         to the :func:`gf.cross_sections.cross_section` function.

#     Returns
#     -------
#     CrossSection
#         A cross-section object representing the negative NbTiN strip.
#     """
#     return cross_section(
#         width=width,
#         layer=layer,
#         bbox_offsets=bbox_offsets,
#         bbox_layers=bbox_layers,
#         radius=radius,
#         port_names=port_names,
#         port_types=port_types,
#         **kwargs,
#     )


# @gf.xsection
# def metal1(
#     width: float = 10,
#     layer: typings.LayerSpec = "NEG_NBTIN",
#     radius: float | None = None,
#     port_names: typings.IOPorts = port_names_electrical,
#     port_types: typings.IOPorts = port_types_electrical,
#     **kwargs: typings.Any,
# ) -> CrossSection:
#     """Return NbTiN cross_section."""
#     return nbtin(
#         width=width,
#         layer=layer,
#         radius=radius,
#         port_names=port_names,
#         port_types=port_types,
#         **kwargs,
#     )


# @gf.xsection
# def metal_routing(
#     width: float = 10,
#     layer: typings.LayerSpec = "NEG_NBTIN",
#     radius: float | None = None,
#     port_names: typings.IOPorts = port_names_electrical,
#     port_types: typings.IOPorts = port_types_electrical,
#     **kwargs: typings.Any,
# ) -> CrossSection:
#     """Return Neg NbTiN cross_section."""
#     return cross_section(
#         width=width,
#         layer=layer,
#         radius=radius,
#         port_names=port_names,
#         port_types=port_types,
#         **kwargs,
#     )


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
