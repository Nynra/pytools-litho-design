import gdsfactory as gf
from .cross_sections import DEMO_CROSS_SECTIONS
from .layers import DEMO_LAYERS
from .transistions import DEMO_TRANSITIONS
from gdsfactory.technology import LayerMap


# Define the layers that can be used


# Define the tapers used for layer transitions


def get_demo_pdk(
    layer_stack: LayerMap = None,
    layer_transitions: dict = None,
    cross_sections: dict = None,
    set_active: bool = True,
) -> gf.Pdk:
    """Returns the Demo PDK.

    .. note::

        While the PDK can also be used to define available components here we only
        use it to define the available layers and layer transitions so we can route
        between components easier.

    Parameters
    ----------
    layer_stack : LayerStack, optional
        The layer stack to use, by default None. If none is set the default `DEMO_LAYERS`
        will be used.
    layer_transitions : dict, optional
        The layer transitions to use, by default None. If none is set the default
        `DEMO_TRANSITIONS` will be used.
    cross_sections : dict, optional
        The cross sections to use, by default None. If none is set the default
        `DEMO_CROSS_SECTIONS` will be used.
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
    pdk.name = "DemoPDK"
    pdk.version = "0.0.1"

    # Set the layerstack
    if not layer_stack:
        pdk.layers = DEMO_LAYERS
    else:
        pdk.layers = layer_stack

    # Set the layer transitions
    if not layer_transitions:
        pdk.layer_transitions = DEMO_TRANSITIONS

    # Set the cross sections
    if not cross_sections:
        pdk.cross_sections = DEMO_CROSS_SECTIONS

    if set_active:
        pdk.activate()
    return pdk
