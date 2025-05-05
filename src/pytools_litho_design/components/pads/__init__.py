from functools import partial
import gdsfactory as gf

pad = partial(
    gf.components.pad,
)

pad_array = partial(
    gf.components.pad_array,
)
