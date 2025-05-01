import math
import gdsfactory as gf
from typing import List
from ..devices import tests


@gf.cell
def alignment(
    die_parameters: utility.DieParameters = utility.DieParameters(),
    layers_to_align: List[int] = [2, 3],
    text: None | str = None,
) -> gf.Component:
    """Creates alignment marks in an integer number of unit cells.

    Parameters:
        die_parameters (DieParameters): the die's parameters.
        layers_to_align (list of int): Layers to align.
        text (str, optional): If None, the text is f"lay={layers_to_align}".

    Returns:
        DIE_ALIGN (Device): A device that centers the alignment marks in an n*m unit cell.
    """

    if text is None:
        text = f"lay={layers_to_align}"
    DIE = gf.Component()

    ALIGN = tests.alignment_mark(layers_to_align)

    n = math.ceil((ALIGN.xsize) / die_parameters.unit_die_size[0])
    m = math.ceil((ALIGN.ysize) / die_parameters.unit_die_size[1])

    BORDER = utility.die_cell(
        die_parameters=die_parameters,
        n_m_units=(n, m),
        device_max_size=(ALIGN.xsize + 20, ALIGN.ysize + 20),
        ports={},
        ports_gnd={},
        text=f"ALIGN {text}",
    )

    DIE << BORDER.flatten()
    DIE << ALIGN

    return DIE
