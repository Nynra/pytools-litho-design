import gdsfactory as gf
from functools import partial

mmi = partial(gf.components.mmi, cross_section="asic")
mmi1x2 = partial(gf.components.mmi1x2, cross_section="asic")
