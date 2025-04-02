import gdsfactory as gf
from gdsfactory.technology import LayerLevel, LayerMap, LayerStack, LayerViews
from gdsfactory.config import CONF
from gdsfactory.component import Component
from gdsfactory.typings import Layer
from gdsfactory.pdk import (
    Pdk,
    constants,
    floorplan_with_block_letters,
    ConfigDict,
    Field,
    LayerEnum,
    Any,
    Callable,
    LayerTransitions,
    ComponentFactory,
    CrossSectionFactory,
    MaterialSpec,
    RoutingStrategies,
    ConnectivitySpec,
    nm,
    Sequence,
)
from functools import partial
from ..components.superconductors.constrictions import (
    spot_constriction,
    variable_length_constriction,
)
from ..components.tapers.tapers import (
    taper_nbtin_au,
    taper_au_nbtin,
)
from ..cross_sections import strip, metal1, nbtin, waveguide, metal_routing, rib


# Define the layers that can be used
class IMPHYS_LAYERS(LayerMap):
    WAFER: Layer = (999, 0)
    AU_PADS: Layer = (1, 0)  # Gold pads for wire bonding
    MARKERS: Layer = (2, 0)  # Markers for alignment and registration
    NEG_NBTIN: Layer = (3, 0)  # Negative resist NBTIN for superconducting lines
    SIO2: Layer = (4, 0)  # Silicon dioxide for insulation
    WAVEGUIDE: Layer = (8, 0)  # Waveguide layer for photonic circuits
    CLADDING: Layer = (9, 0)  # Cladding layer for waveguides


# Define the tapers used for layer transitions
IMPHYS_LAYER_TRANSITIONS = {
    IMPHYS_LAYERS.AU_PADS: partial(
        gf.components.taper_electrical,
        layer=IMPHYS_LAYERS.AU_PADS,
        port_names=("e1", "e2"),
        port_types=("electrical", "electrical"),
    ),
    IMPHYS_LAYERS.NEG_NBTIN: partial(
        gf.components.taper_electrical,
        layer=IMPHYS_LAYERS.NEG_NBTIN,
        port_names=("e1", "e2"),
        port_types=("electrical", "electrical"),
    ),
    (IMPHYS_LAYERS.NEG_NBTIN, IMPHYS_LAYERS.AU_PADS): partial(
        taper_nbtin_au,
        layer_nbtin=IMPHYS_LAYERS.NEG_NBTIN,
        layer_au=IMPHYS_LAYERS.AU_PADS,
        cross_section=gf.cross_section.metal_routing(layer=IMPHYS_LAYERS.NEG_NBTIN),
    ),
    (IMPHYS_LAYERS.AU_PADS, IMPHYS_LAYERS.NEG_NBTIN): partial(
        taper_au_nbtin,
        layer_nbtin=IMPHYS_LAYERS.NEG_NBTIN,
        layer_au=IMPHYS_LAYERS.AU_PADS,
        cross_section=gf.cross_section.metal_routing(layer=IMPHYS_LAYERS.NEG_NBTIN),
    ),
}


CROSS_SECTIONS = {
    "strip": strip,
    "metal1": metal1,
    "nbtin": nbtin,
    "waveguide": waveguide,
    "metal_routing": metal_routing,
    "rib": rib,
}


def get_imphys_pdk(
    layer_stack: LayerMap = None,
    layer_transitions: dict = None,
    cross_sections: dict = None,
    set_active: bool = True,
) -> gf.Pdk:
    """Returns the ImPhys PDK.

    The PDK contains the available layers and layer transitions for the
    ImPhys group.

    .. note::

        While the PDK can also be used to define available components here we only
        use it to define the available layers and layer transitions so we can route
        between components easier.

    Parameters
    ----------
    layer_stack : LayerStack, optional
        The layer stack to use, by default None. If none is set the default `IMPHYS_LAYERS`
        will be used.
    layer_transitions : dict, optional
        The layer transitions to use, by default None. If none is set the default
        `IMPHYS_LAYER_TRANSITIONS` will be used.
    cross_sections : dict, optional
        The cross sections to use, by default None. If none is set the default
        `CROSS_SECTIONS` will be used.
    set_active : bool, optional
        Whether to set the PDK as active, by default True. If set to False the PDK
        will not be set as active and will not be used for any components.

    Returns
    -------
    gf.Pdk
        The ImPhys PDK.
    """
    pdk: gf.Pdk = gf.generic_tech.get_generic_pdk()

    # Set version info
    pdk.name = "ImPhysPDK"
    pdk.version = "0.0.1"

    # Set the layerstack
    if not layer_stack:
        pdk.layers = IMPHYS_LAYERS
    else:
        pdk.layers = layer_stack

    # Set the layer transitions
    if not layer_transitions:
        pdk.layer_transitions = IMPHYS_LAYER_TRANSITIONS

    # Set the cross sections
    if not cross_sections:
        pdk.cross_sections = CROSS_SECTIONS

    if set_active:
        pdk.activate()
    return pdk


# class ImphysPdk(gf.Pdk):
#     """Store layers, cross_sections, cell functions, simulation_settings ...

#     only one Pdk can be active at a given time.

#     Parameters:
#         name: PDK name.
#         version: PDK version.
#         cross_sections: dict of cross_sections factories.
#         cells: dict of parametric cells that return Components.
#         containers: dict of containers that return Components. A container is a cell that contains other cells.
#         models: dict of models names to functions.
#         symbols: dict of symbols names to functions.
#         default_symbol_factory:
#         base_pdk: a pdk to copy from and extend.
#         default_decorator: decorate all cells, if not otherwise defined on the cell.
#         layers: maps name to gdslayer/datatype.
#             For example dict(si=(1, 0), sin=(34, 0)).
#         layer_stack: maps name to layer numbers, thickness, zmin, sidewall_angle.
#             if can also contain material properties
#             (refractive index, nonlinear coefficient, sheet resistance ...).
#         layer_views: includes layer name to color, opacity and pattern.
#         layer_transitions: transitions between different cross_sections.
#         constants: dict of constants for the PDK.
#         materials_index: material spec names to material spec, which can be:
#             string: material name.
#             float: refractive index.
#             float, float: refractive index real and imaginary part.
#             function: function of wavelength.
#         routing_strategies: functions enabled to route.
#         bend_points_distance: default points distance for bends in um.
#         connectivity: defines connectivity between layers through vias.

#     """

#     name: str = "IMPHYS_PDK"
#     version: str = "0.0.1"
#     cross_sections: dict[str, CrossSectionFactory] = Field(
#         default_factory=lambda: CROSS_SECTIONS
#     )
#     cross_section_default_names: dict[str, str] = Field(
#         default_factory=lambda: {
#             "strip": "strip",
#             "metal1": "metal1",
#             "nbtin": "nbtin",
#             "waveguide": "waveguide",
#             "metal_routing": "metal_routing",
#             "rib": "rib",
#         }
#     )
#     cells: dict[str, ComponentFactory] = Field(default_factory=dict, exclude=True)
#     containers: dict[str, ComponentFactory] = Field(default_factory=dict, exclude=True)
#     models: dict[str, Callable[..., Any]] = Field(default_factory=dict, exclude=True)
#     symbols: dict[str, ComponentFactory] = Field(default_factory=dict)
#     default_symbol_factory: ComponentFactory = Field(
#         default=floorplan_with_block_letters, exclude=True
#     )
#     base_pdks: list[Pdk] = Field(default_factory=list)
#     default_decorator: Callable[[Component], None] | None = Field(
#         default=None, exclude=True
#     )
#     layers: type[LayerEnum] | None = None
#     layer_stack: LayerStack | None = None
#     layer_views: LayerViews | None = None
#     layer_transitions: LayerTransitions = Field(default_factory=dict)
#     constants: dict[str, Any] = constants
#     materials_index: dict[str, MaterialSpec] = Field(default_factory=dict)
#     routing_strategies: RoutingStrategies | None = None
#     bend_points_distance: float = 20 * nm
#     connectivity: Sequence[ConnectivitySpec] | None = None
#     max_cellname_length: int = CONF.max_cellname_length

#     model_config = ConfigDict(
#         arbitrary_types_allowed=True,
#         extra="forbid",
#     )
