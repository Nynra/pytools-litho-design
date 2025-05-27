import gdsfactory as gf
from gdsfactory.typings import LayerSpec, ComponentSpec


@gf.cell
def add_protection_mask(
    component: ComponentSpec,
    protection_layer: LayerSpec,
    component_layers: list[LayerSpec] = [],
    offset: int = 3,
    corner_radius: float | None = None,
) -> gf.Component:
    """Adds a protection mask to a component.

    The protection mask is a dilated version of the component geometries
    on the specified protection layer.

    .. attention::
        This method uses :meth:`flatten()` to merge the geometries, which may
        result in loss of hierarchy or segmentation errors. Make sure to perform this
        operation only on components that are suitable for flattening.

    Parameters
    ----------
    component: ComponentSpec
        The component to which the protection mask will be added.
    protection_layer: LayerSpec
        The layer on which the protection mask will be created.
    component_layers: list[LayerSpec]
        The layers of the component that will be protected.
    offset: int
        The distance by which the protection mask will be dilated.
    corner_radius: float | None
        The radius of the corners of the protection mask. If None, corners will not be rounded.

    Returns
    -------
    gf.Component
        A new component with the protection mask added.
    """
    # Get the specs in the right format
    if not isinstance(component, gf.Component):
        component = gf.get_component(component)
    if not isinstance(protection_layer, (list, tuple)):
        protection_layer = gf.get_layer_tuple(protection_layer)

    if not isinstance(component_layers, (tuple, list)):
        # Layers are fiven as strings, convert them to tuples
        component_layers = [component_layers]

        for layer in component_layers:
            if not isinstance(layer, (list, tuple)):
                layer = gf.get_layer_tuple(layer)

    elif not all(isinstance(layer, (list, tuple)) for layer in component_layers):
        # Layers are fiven as strings, convert them to tuples
        component_layers = [gf.get_layer_tuple(layer) for layer in component_layers]

    # Create a copy to use as a template
    temp = gf.Component()
    temp << component.copy()
    temp.flatten()

    # Remap every geometry to the protection layer
    mapping = {layer: protection_layer for layer in component_layers}
    temp.remap_layers(mapping, recursive=True)

    # Merge the geometries with the protection layer and dillate the component
    temp.flatten()
    temp.offset(
        distance=offset,
        layer=protection_layer,
    )

    # Round the corners if specified
    if corner_radius is not None:
        rounded_temp = gf.Component()
        for p in temp.get_polygons(by="tuple", layers=[protection_layer])[
            protection_layer
        ]:
            p_round = p.round_corners(corner_radius, corner_radius * 1e3, 200)
            rounded_temp.add_polygon(p_round, layer=protection_layer)
        temp = rounded_temp

    # Create a new component and combine the original component with the protection mask
    final_component = gf.Component()
    final_component << component
    final_component << temp
    final_component.flatten()
    final_component.add_ports(
        component.ports,
    )
    return final_component


if __name__ == "__main__":
    c = gf.Component()
    c << add_protection_mask(
        component=gf.components.straight(
            cross_section=gf.cross_section.strip(layer="WG")
        ),
        protection_layer="WGCLAD",
        component_layers=["WG"],
        offset=1,
        corner_radius=0.5,
    )
    c.show()
