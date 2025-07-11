from functools import partial
import gdsfactory as gf

# from gdsfactory.components import pad, pad_array

pad = partial(gf.components.pad, layer="COARSE_NBTIN", size=(100, 100))

pad_array = partial(gf.components.pad_array, layer="COARSE_NBTIN")
