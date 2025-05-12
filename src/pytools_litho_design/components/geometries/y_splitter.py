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


if __name__ == "__main__":
    cs = y_split(cross_section="strip")
    cs.draw_ports()
    cs.show()
