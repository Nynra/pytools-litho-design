from functools import partial
import gdsfactory as gf

pad = partial(
    gf.components.pad,
)
