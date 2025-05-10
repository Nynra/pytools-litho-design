from functools import partial
import gdsfactory as gf


straight = partial(gf.components.straight, cross_section="asic")
spiral_racetrack = partial(
    gf.components.spiral_racetrack,
    cross_section="asic",
    cross_section_s="asic",
)
spiral_racetrack_fixed_length = partial(
    gf.components.spiral_racetrack_fixed_length,
    cross_section="asic",
    cross_section_s="asic",
)
# from gdsfactory.components import (
#     straight,
#     spiral_racetrack,
#     spiral_racetrack_fixed_length,
# )
