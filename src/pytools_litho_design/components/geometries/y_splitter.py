import gdsfactory as gf
from gdsfactory.typings import ComponentSpec, CrossSectionSpec


@gf.cell
def y_split(
    width=3,
    length=40,
    cross_section="strip",
) -> ComponentSpec:
    """Creates a Y-splitter component."""
    c = gf.Component()

    checkpoint = c << gf.get_component(
        "straight",
        cross_section=cross_section,
        length=0.1,
    )
    O1 = c << gf.get_component(
        "straight",
        cross_section=cross_section,
        length=0.1,
    )
    O2 = c << gf.get_component(
        "straight",
        cross_section=cross_section,
        length=0.1,
    )
    O3 = c << gf.get_component(
        "straight",
        cross_section=cross_section,
        length=0.1,
    )

    checkpoint.center = (0, 0)
    O2.center = (length, width / 2)
    O3.center = (length, -width / 2)

    gf.routing.route_bundle_sbend(
        c,
        [
            O3.ports["o1"],
            O2.ports["o1"],
        ],
        [
            checkpoint.ports["o2"],
            checkpoint.ports["o2"],
        ],
        cross_section=cross_section,
    )
    c.add_port("o1", port=checkpoint.ports["o1"])
    c.add_port("o2", port=O2.ports["o2"])
    c.add_port("o3", port=O3.ports["o2"])
    c.flatten()
    return c


@gf.cell
def y_split_trench(
    angle: float = 30.0,  # Angle between split arms (degrees)
    bend_radius: float = 20.0,  # Radius for Euler bend
    stem_length: float = 10.0,  # Length of the input straight
    arm_length: float = 20.0,  # Length of straight output arms
    cross_section: CrossSectionSpec = "rib_with_trenches",
) -> gf.Component:
    """Trench-compatible Y-splitter using symmetric Euler bends."""
    c = gf.Component()

    # Central input straight
    stem = gf.components.straight(length=stem_length, cross_section=cross_section)
    ref_stem = c.add_ref(stem)

    # Create one bend and clone it for both arms
    bend = gf.components.bend_euler(
        angle=angle, radius=bend_radius, cross_section=cross_section
    )

    # Left bend
    ref_bend_left = c.add_ref(bend)
    ref_bend_left.connect(port="o1", other=ref_stem.ports["o2"])

    # Right bend (mirrored)
    ref_bend_right = c.add_ref(bend)
    ref_bend_right.mirror(p1=(0, 0), p2=(1, 0))
    ref_bend_right.connect(port="o1", other=ref_stem.ports["o2"])

    # Output arms (straight waveguides)
    arm = gf.components.straight(length=arm_length, cross_section=cross_section)

    ref_out1 = c.add_ref(arm)
    ref_out1.connect(port="o1", other=ref_bend_left.ports["o2"])

    ref_out2 = c.add_ref(arm)
    ref_out2.connect(port="o1", other=ref_bend_right.ports["o2"])

    # Define ports
    c.add_port("o1", port=ref_stem.ports["o1"])
    c.add_port("o2", port=ref_out1.ports["o2"])
    c.add_port("o3", port=ref_out2.ports["o2"])
    c.flatten()
    return c


def add_trenches_postprocess(
    component: gf.Component, layer_core: tuple = (30, 0), trench_cross_section=None
) -> gf.Component:
    """Adds trenches to an existing component by extruding paths on a core layer.

    Args:
        component: layout with waveguides drawn on core (abstract) layer.
        layer_core: layer where core waveguides are drawn (e.g., WG_ABSTRACT).
        trench_cross_section: cross_section with trench geometry, like rib_with_trenches.

    Returns:
        Modified component with trenches added.
    """
    import shapely.geometry as sg
    from gdsfactory.geometry.get_paths import get_paths

    # Default trench cross-section
    trench_cross_section = trench_cross_section or "rib_with_trenches"

    # Get core paths (single-line centerlines from polygons)
    paths = get_paths(component, layer=layer_core)

    # Add trench extrusion for each path
    for path in paths:
        trench = path.extrude(cross_section=trench_cross_section)
        component.add_ref(trench)

    return component


if __name__ == "__main__":
    c = y_split_trench()
    cs = add_trenches_postprocess(c, layer_core="ASIC_RIDGE")
    cs.draw_ports()
    cs.show()
