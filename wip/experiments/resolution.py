import math
import gdsfactory as gf
from typing import List
from ..devices import tests


@gf.cell
def resolution_test(
    die_parameters: utility.DieParameters = utility.DieParameters(),
    layer_to_resolve: int = 1,
    resolutions_to_test: List[float] = [
        0.025,
        0.05,
        0.075,
        0.1,
        0.25,
        0.5,
        1,
        1.5,
        2.0,
    ],
    text: None | str = None,
) -> gf.Component:
    r"""Creates an experiment containing a resolution test.

    Parameters:
        die_parameters (DieParameters): the die's parameters.
        layer_to_resolve (int): The layer to put the resolution test on.
        resolutions_to_test (list of float): The resolutions to test in µm.
        text (str, optional): If None, the text is f"lay={layer_to_resolve}".

    Returns:
        DIE_RES_TEST (Device): The created device.
    """

    if text is None:
        text = f"lay={layer_to_resolve}"
    DIE_RES_TEST = gf.Component()

    ## Create the test structure
    TEST_RES = gf.Component()
    test_res = TEST_RES << tests.resolution_test(
        resolutions=resolutions_to_test, inverted=False, layer=layer_to_resolve
    )
    test_res_invert = TEST_RES << tests.resolution_test(
        resolutions=resolutions_to_test,
        inverted=resolutions_to_test[-1],
        layer=layer_to_resolve,
    )
    test_res_invert.movey(
        test_res_invert.ymin, test_res.ymax + 5 * resolutions_to_test[-1]
    )

    DIE_RES_TEST << TEST_RES.move(TEST_RES.center, (0, 0))

    ## Create the die
    n = math.ceil((TEST_RES.xsize) / die_parameters.unit_die_size[0])
    m = math.ceil((TEST_RES.ysize) / die_parameters.unit_die_size[1])
    BORDER = utility.die_cell(
        die_parameters=die_parameters,
        n_m_units=(n, m),
        ports={},
        ports_gnd=[],
        text=f"RES TEST \n{text}",
    )

    DIE_RES_TEST << BORDER.flatten()
    return DIE_RES_TEST
