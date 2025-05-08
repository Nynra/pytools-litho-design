import gdsfactory as gf
from functools import partial


# die_with_pads = partial(
#     gf.components.die_with_pads,
#     grating_coupler="grating_coupler_traditional",
#     with_loopback=False,
# )
# from gdsfactory.components import die_with_pads

die_with_pads = partial(
    gf.components.die_with_pads,
    grating_coupler="grating_coupler_traditional",
    with_loopback=False,
    cross_section="asic",
    layer_floorplan="WAFER",
)

splitter_tree = partial(gf.components.splitter_tree, cross_section="asic")
