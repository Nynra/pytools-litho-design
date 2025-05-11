import gdsfactory as gf


def two_ring_muxer(radius_list: list[10, 20], cross_section="asic_ridge"):
    if isinstance(cross_section, str):
        cross_section = gf.get_cross_section(cross_section)

    CHIP = gf.Component()
    STRAIGHT = gf.get_component("straight", length=50.0, cross_section=cross_section)

    rings = [
        gf.components.ring_double_bend_coupler(
            radius=radius,
            cross_section_inner=cross_section,
            cross_section_outer=cross_section,
        )
        for radius in radius_list
    ]

    # Connect the rings
    ring_instance = [CHIP << ring for ring in rings]
    ring_instance[0].connect(port="o1", other=ring_instance[1].ports["o3"])

    # Connect the entrances and exits
    entrance = CHIP << STRAIGHT
    entrance.connect(port="o1", other=ring_instance[1].ports["o4"])
    exit1 = CHIP << STRAIGHT
    exit1.connect(port="o1", other=ring_instance[0].ports["o4"])
    exit2 = CHIP << STRAIGHT
    exit2.connect(port="o1", other=ring_instance[1].ports["o1"])

    CHIP.add_port("o1", port=entrance.ports["o2"])
    CHIP.add_port("o2", port=exit1.ports["o2"])
    CHIP.add_port("o3", port=exit2.ports["o2"])
    CHIP.flatten()
    return CHIP


def bend_two_ring_demuxer(
    radius1=40,
    radius2=70,
    ring_spacing=100,
    output_spacing=100,
    output_distance=55,
    gap=0.2,
    cross_section="asic_ridge",
    coupling_angle_coverage=70,
) -> gf.Component:
    assert radius1 < radius2, "radius1 must be less than radius2"

    C = gf.Component()
    r1 = C << gf.components.ring_double_bend_coupler(
        radius=radius1,
        gap=gap,
        coupling_angle_coverage=coupling_angle_coverage,
        # length_x=0.6,
        # length_y=0.6,
        cross_section_inner=cross_section,
        cross_section_outer=cross_section,
    )
    r2 = C << gf.components.ring_double_bend_coupler(
        radius=radius2,
        gap=gap,
        coupling_angle_coverage=coupling_angle_coverage,
        # length_x=0.6,
        # length_y=0.6,
        cross_section_inner=cross_section,
        cross_section_outer=cross_section,
    )
    # print(r2.ports)
    spacer = C << gf.get_component(
        "straight", cross_section=cross_section, length=ring_spacing
    )
    r1.connect("o1", spacer.ports["o1"])
    r2.connect("o2", spacer.ports["o2"])
    # C.flatten()
    # C.add_port("o1", port=r2.ports["o3"])
    # C.add_port("o2", port=r1.ports["o3"])
    # C.add_port("o3", port=r2.ports["o1"])

    O2 = gf.get_component("straight", cross_section=cross_section, length=10)
    O1 = gf.get_component("straight", cross_section=cross_section, length=10)
    O0 = gf.get_component("straight", cross_section=cross_section, length=10)
    GRID = gf.grid(
        components=[O0, O1, O2],
        shape=(3, 1),
        spacing=(output_distance, output_distance),
    )
    grid = C << GRID
    # grid.move((-200, 100))
    grid.center = (
        r1.xmin - output_spacing,
        r1.ymax - 10,
    )

    gf.routing.route_bundle_sbend(
        C,
        [
            r1.ports["o3"],
            r2.ports["o1"],
            r1.ports["o4"],
        ],
        [
            grid.ports["1_o2"],
            grid.ports["2_o2"],
            grid.ports["0_o2"],
        ],
        cross_section=cross_section,
    )

    # C.flatten()
    C.add_port("o3", port=grid.ports["2_o1"])
    C.add_port("o2", port=grid.ports["1_o1"])
    C.add_port("o1", port=grid.ports["0_o1"])
    C.add_port("o4", port=r2.ports["o3"])
    return C


if __name__ == "__main__":
    c = bend_two_ring_demuxer(cross_section="strip")
    c.draw_ports()
    c.show()
