from functools import partial
import gdsfactory as gf

# from gdsfactory.components.bends import bend_euler, bend_circular, bend_s
# from gdsfactory.components import wire_corner, wire_straight

# Euler bends
bend_euler_s = partial(
    gf.components.bend_euler, npoints=100, cross_section="asic", radius=100
)
bend_euler = partial(
    gf.components.bend_euler, npoints=100, cross_section="asic", radius=100
)
bend_euler_all_angle = partial(
    gf.components.bend_euler, npoints=100, cross_section="asic", radius=100
)
bend_euler_90 = partial(
    gf.components.bend_euler, npoints=100, angle=90, cross_section="asic", radius=100
)
bend_euler_180 = partial(
    gf.components.bend_euler, npoints=100, angle=180, cross_section="asic", radius=100
)

bend_circular = partial(gf.components.bend_circular, npoints=100, cross_section="asic")
bend_circular_all_angle = partial(
    gf.components.bend_circular, npoints=100, angle=0, cross_section="asic"
)
bend_circular_180 = partial(
    gf.components.bend_circular, npoints=100, angle=180, cross_section="asic"
)

# # S bends
bezier = partial(gf.components.bezier, cross_section="asic")
bend_s = partial(gf.components.bend_s, cross_section="asic")
