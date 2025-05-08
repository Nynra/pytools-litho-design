import gdsfactory as gf
from ..waveguides import straight


def two_ring_muxer(radius_list: list[10, 20], cross_section="sio2"):
    if isinstance(cross_section, str):
        cross_section = gf.get_cross_section(cross_section)

    CHIP = gf.Component()
    STRAIGHT = straight(length=50.0, cross_section=cross_section)

    rings = [
        gf.components.ring_double(
            radius=radius,
            cross_section=cross_section,
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
