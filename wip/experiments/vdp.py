from typing import List
import gdsfactory as gf


def vdp(
    die_parameters: utility.DieParameters = utility.DieParameters(),
    layers_to_probe: List[int] = [2],
    layers_to_outline: None | List[int] = None,
    text: None | str = None,
) -> gf.Component:
    r"""Creates an experiment containing a Van Der Pauw structure between 4 contact
    pads.

    Parameters:
        die_parameters (DieParameters): the die's parameters.
        layers_to_probe (list of int): The layers on which to place the VDP structure.
        layers_to_outline (list of int): Among the VDP layers, the ones for which structure must not be filled but outlined.
        text (str, optional): If None, the text is f"lay={layers_to_probe}".
    Returns:
        DIE_VANDP (Device): The created device.
    """
    # Initialize parameters left to default (=None)

    if text is None:
        text = f"lay={layers_to_probe}"
    if layers_to_outline is None:
        layers_to_outline = [
            die_parameters.die_layer
        ]  # default layer to outline if None is given

    DIE_VANDP = gf.Component()

    device_max_w = min(die_parameters.unit_die_size) - 2 * (
        die_parameters.pad_size[1] + 2 * die_parameters.outline
    )  # width of max device size for this cell
    contact_w = device_max_w / 10  # choosing a contact width 10 times smaller
    device_w = (
        device_max_w - 2 * contact_w
    )  # choosing a smaller device to have space for routing from pad to contact

    # Creates the DIE, it contains only the cell text and bordure

    DIE = utility.die_cell(
        die_parameters=die_parameters,
        device_max_size=(device_max_w, device_max_w),
        ports={},
        ports_gnd=[],
        text=f"VDP \n{text}",
    )
    DIE_VANDP << DIE.flatten()

    # Creates the vdp structure, add pads and route

    VDP = gf.Component()

    ## VDP probed area
    AREA = test.vdp(device_w, contact_w)
    VDP << AREA

    ## pads (creates a die and keeps the pads only)
    pads_parameters = utility.DieParameters(
        unit_die_size=die_parameters.unit_die_size,
        pad_size=die_parameters.pad_size,
        contact_l=0,
        outline=die_parameters.outline,
        die_layer=0,
        pad_layer=die_parameters.pad_layer,
        positive_tone=die_parameters.positive_tone,
        fill_pad_layer=False,
        text_size=die_parameters.text_size,
        pad_tolerance=0,
    )

    PADS = utility.die_cell(
        die_parameters=pads_parameters,
        contact_w=die_parameters.pad_size[0],
        device_max_size=(device_max_w, device_max_w),
        ports={"N": 1, "E": 1, "W": 1, "S": 1},
        ports_gnd=["N", "E", "W", "S"],
        text="PADS ONLY",
    )
    PADS.remove_layers([die_parameters.pad_layer], invert_selection=True)
    VDP << PADS

    ## routes from pads to probing area
    # ROUTES = utility.route_to_dev(PADS.get_ports(), AREA.ports)
    # VDP << ROUTES
    gf.routing.route_bundle(
        VDP,
        PADS.ports,
        AREA.ports,
    )

    VDP.flatten(0)

    # Outline the vdp structure for layers that need to be outlined

    DEVICE = gf.Component()

    for layer in layers_to_probe:
        TEST_LAYER = VDP.copy()
        if layer in layers_to_outline:
            TEST_LAYER = pg.outline(TEST_LAYER, die_parameters.outline)
        TEST_LAYER.name = f"VDP(lay={layer})"
        DEVICE << TEST_LAYER.flatten(single_layer=layer)

    DIE_VANDP << DEVICE

    # Add pads if they are not in already present
    if die_parameters.pad_layer not in layers_to_probe:
        PADS = pg.union(PADS, layer=die_parameters.pad_layer)
        PADS.name = "PADS"
        DIE_VANDP << PADS

    return DIE_VANDP
