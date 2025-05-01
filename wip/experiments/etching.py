import math
import gdsfactory as gf


def etch_test(
    die_parameters: utility.DieParameters = utility.DieParameters(),
    layers_to_etch: List[List[int]] = [[3]],
    text: Union[None, str] = None,
) -> gf.Component:
    """Creates etch test structures in an integer number of unit cells.

    These test structures are thought to be used by probing on pads (with a
    simple multimeter) that should be isolated one from another if the etching
    is complete.

    Parameters:
        die_parameters (DieParameters): the die's parameters.
        layers_to_etch (list of list of int): Each element of the list corresponds to one test point, to put on the list of layers specified.
                                               Example: [[1, 2], [1], [2]]
        text (str, optional): If None, the text is f"lay={layers_to_etch}".

    Returns:
        DIE_ETCH_TEST (Device): A device (with size n*m of unit cells) with etch tests in its center.
    """

    if text is None:
        text = f"lay={layers_to_etch}"
    DIE_ETCH_TEST = gf.Component()

    TEST = gf.Component()

    ## Create the probing areas

    margin = 0.12 * min(die_parameters.unit_die_size)
    rect = gf.components.rectangle(
        (
            die_parameters.unit_die_size[0] - 2 * margin,
            die_parameters.unit_die_size[1] - 2 * margin,
        )
    )
    for i, layer_to_etch in enumerate(layers_to_etch):
        probe = gf.Component()
        probe.add_array(rect, 2, 1, die_parameters.unit_die_size)
        for layer in layer_to_etch:
            TEST << gf.components.containers.outline(
                probe, -die_parameters.outline, layer=layer
            ).movey(i * die_parameters.unit_die_size[1])

    ## Create the die

    n = math.ceil(
        (TEST.xsize + 2 * die_parameters.die_border_w) / die_parameters.unit_die_size[0]
    )
    m = math.ceil(
        (TEST.ysize + 2 * die_parameters.die_border_w) / die_parameters.unit_die_size[1]
    )
    BORDER = utility.die_cell(
        die_parameters=die_parameters,
        n_m_units=(n, m),
        ports={},
        ports_gnd={},
        text=f"ETCH TEST {text}",
    )

    BORDER.move(TEST.center)
    DIE_ETCH_TEST << BORDER.flatten()
    DIE_ETCH_TEST << TEST.flatten()
    DIE_ETCH_TEST.move(DIE_ETCH_TEST.center, (0, 0))

    return DIE_ETCH_TEST
