import gdsfactory as gf
from functools import partial
from .superconductors import snspd
from .couplers import (
    grating_arrays,
    grating_coupler_array,
    grating_coupler_cluster,
    grating_coupler_opposing,
    grating_coupler_traditional,
)
from .rings import two_ring_muxer, bend_two_ring_demuxer
from .markers import ebl_marker, ebl_marker_jb
from .pads import pad, pad_array
from .geometries import (
    rectangle,
    spiral_racetrack,
    spiral_racetrack_fixed_length,
    y_split,
)

# Straight sections
straight = partial(gf.components.straight, cross_section="asic_ridge")
# spiral_racetrack = partial(
#     gf.components.spiral_racetrack,
#     cross_section="asic_ridge",
#     cross_section_s="asic_ridge",
# )
# spiral_racetrack_fixed_length = partial(
#     gf.components.spiral_racetrack_fixed_length,
#     cross_section="asic_ridge",
#     cross_section_s="asic_ridge",
# )
# from gdsfactory.components import (
#     straight,
#     spiral_racetrack,
#     spiral_racetrack_fixed_length,
# )

# Euler bends
bend_euler_s = partial(
    gf.components.bend_euler, npoints=100, cross_section="asic_ridge"
)
bend_euler = partial(gf.components.bend_euler, npoints=100, cross_section="asic_ridge")
bend_euler_all_angle = partial(
    gf.components.bend_euler, npoints=100, cross_section="asic_ridge"
)
bend_euler_90 = partial(
    gf.components.bend_euler, npoints=100, angle=90, cross_section="asic_ridge"
)
bend_euler_180 = partial(
    gf.components.bend_euler, npoints=100, angle=180, cross_section="asic_ridge"
)

bend_circular = partial(
    gf.components.bend_circular, npoints=100, cross_section="asic_ridge"
)
bend_circular_all_angle = partial(
    gf.components.bend_circular, npoints=100, angle=0, cross_section="asic_ridge"
)
bend_circular_180 = partial(
    gf.components.bend_circular, npoints=100, angle=180, cross_section="asic_ridge"
)

# S bends
bezier = partial(gf.components.bezier, cross_section="asic_ridge")
bend_s = partial(gf.components.bend_s, cross_section="asic_ridge")

# Misc components
# die_with_pads = partial(
#     gf.components.die_with_pads,
#     grating_coupler="grating_coupler_traditional",
#     with_loopback=False,
#     cross_section="asic_ridge",
#     layer_floorplan="WAFER",
# )

splitter_tree = partial(gf.components.splitter_tree, cross_section="asic_ridge")

# MMI's
mmi = partial(gf.components.mmi, cross_section="asic_ridge")
mmi1x2 = partial(gf.components.mmi1x2, cross_section="asic_ridge")


@gf.cell
def trenched_mmi1x2(
    width: float | None = None,
    width_taper: float = 1.0,
    length_taper: float = 10.0,
    length_mmi: float = 5.5,
    width_mmi: float = 2.5,
    gap_mmi: float = 0.25,
    cross_section: str = "xs_wg300",
    layer_trench: str = "ASIC_ETCH",
    trench_width: float = 1,
) -> gf.Component:
    """Creates a trenched MMI 1x2 component."""
    return gf.components.add_trenches(
        mmi1x2(
            width=width,
            width_taper=width_taper,
            length_taper=length_taper,
            length_mmi=length_mmi,
            width_mmi=width_mmi,
            gap_mmi=gap_mmi,
            cross_section=cross_section,
        ),
        cross_section=cross_section,
        layer_component=gf.get_cross_section(cross_section).layer,
        trench_width=trench_width,
        layer_trench=layer_trench,
    )


# Tekst
text = partial(gf.components.text, layer="COARSE_AU")
