import gdsfactory as gf
import numpy as np


# @gf.cell
# def wg_to_snspd(
#     wgnw_width=0.1,
#     wgnw_length=100,
#     wgnw_gap=0.15,
#     num_squares=5000.0,
#     meander_width=0.4,
#     meander_fill_factor=0.5,
#     wg_width=0.75,
#     layer=1,
# ):
#     """Waveguide coupled to SNSPD with inductor (meander).
#     The length and width of the meander are chosen so that it is approximately square

#     Args:
#         meander_width (float): nanowire width within meander inductor
#         num_squares (float): total squares in meander and out-and-back
#         wgnw_width (float): width of out-and-back nanowire
#         wgnw_length (float): length of out-and-back
#         wgnw_gap (float): spacing between the out-and-back wires
#         wg_width (float): waveguide width

#     Ports:
#         el_1: wiring port
#         el_gnd: wiring port
#         wg_in: input optical port
#         de_edge: edge of explicit waveguide on the SNSPD side
#     """

#     D = gf.Component()

#     # Calculations and checks
#     numsquares_wgnw = 2 * wgnw_length / wgnw_width
#     numsquares_meander = num_squares - numsquares_wgnw
#     if numsquares_meander < 1000:
#         print(
#             "Warning: Not enough squares in SNSPD meander. Clipped to 1000 from {:.1f}".format(
#                 numsquares_meander
#             )
#         )
#         numsquares_meander = 1000
#     meander_pitch = meander_width / meander_fill_factor
#     meander_length = np.sqrt(numsquares_meander * meander_width * meander_pitch)
#     wgnw_pitch = wgnw_width + wgnw_gap
#     wgnw_distance_to_edge = wg_width / 2 - wgnw_width - wgnw_gap / 2
#     if wgnw_distance_to_edge < 0:
#         print(
#             "Warning: nanowire will overhang side of waveguide by {:.3f} um".format(
#                 -wgnw_distance_to_edge
#             )
#         )

#     numsquares_per_taper = 3  # approximate
#     D.info["num_squares"] = (
#         numsquares_meander
#         + numsquares_wgnw
#         - meander_length / meander_width
#         + 3 * numsquares_per_taper
#     )
#     # D.info['expected_resistance'] = D.info['num_squares']*EXPECTED_RSQ_WSI
#     D.info["wire_width"] = wgnw_width
#     D.info["length"] = wgnw_length

#     # Geometry
#     meander = D << gf.components.superconductors.snspd(
#         wire_width=meander_width,
#         wire_pitch=meander_pitch,
#         terminals_same_side=False,
#         size=(meander_length, None),
#         num_squares=numsquares_meander,
#         layer=layer,
#     )
#     meander.mirror(p1=(0, 0), p2=(1, 0))

#     Taper = gf.components.superconductors.optimal_step(
#         start_width=wgnw_width,
#         end_width=meander_width,
#         num_pts=50,
#         width_tol=1e-3,
#         anticrowding_factor=1.2,
#         layer=layer,
#     )

#     # Due to a bug the ports are alsways set as optical
#     for port in Taper.ports:
#         port.port_type = "electrical"

#     taper1 = D << Taper
#     taper1.connect(1, meander.ports[0])

#     wgnw = D << gf.components.optimal_hairpin(
#         width=wgnw_width, pitch=wgnw_pitch, length=wgnw_length, layer=layer
#     )
#     wgnw.connect(1, taper1.ports[0])

#     taper2 = D << Taper
#     taper2.mirror()
#     taper2.connect(0, wgnw.ports[0])

#     # Electrical ports
#     exit_bend = D << gf.components.superconductors.optimal_90deg(
#         width=meander_width, num_pts=15, length_adjust=1, layer=layer
#     )
#     exit_bend.connect(1, taper2.ports[1])
#     D.add_port("el_gnd", port=exit_bend.ports[0])

#     exit_taper = D << gf.components.superconductors.optimal_step(
#         start_width=meander_width,
#         end_width=meander_width * 4,
#         num_pts=50,
#         width_tol=1e-3,
#         anticrowding_factor=1.2,
#         layer=layer,
#     )
#     exit_taper.connect(0, meander.ports[1])
#     D.add_port("el_1", port=exit_taper.ports[1])

#     # Waveguide and optical ports
#     wg = D << gf.components.compass(
#         size=[wgnw_length + wgnw_distance_to_edge, wg_width], layer=layer
#     )
#     wg.xmax = wgnw.xmax
#     wg.y = wgnw.y

#     D.add_port("de_edge", port=wg.ports["E"])
#     D.add_port("wg_in", port=wg.ports["W"])
#     D.ports["de_edge"].info["is_waveguide_edge"] = True

#     pos = D.ports["wg_in"].center
#     D.move(-1 * pos)

#     return D


# if __name__ == "__main__":
#     import matplotlib.pyplot as plt

#     c = wg_to_snspd()
#     c.plot()
#     plt.show()


@gf.cell
def rectangle_meander(
    num_of_boxes=23,
    width=0.5,
    length=10,
    bending_radius=0.5,
    insulator_width=0.75,
    wire_width=5,
    layer=(2, 1),
):
    MEANDER = gf.Component()

    # Initialize a list to store the devices that will become the "ports" of the meander
    boxes = []

    def renaming_func(ports: str) -> str:
        for cnt, port in enumerate(ports):
            match port.name:
                case "e1":
                    replacement = "W"
                case "e2":
                    replacement = "N"
                case "e3":
                    replacement = "E"
                case "e4":
                    replacement = "S"
                case _:
                    raise ValueError(f"Unknown port name: {port.name}")

            ports[cnt].name = replacement
        return ports

    BOX = gf.components.compass(
        size=[length, width],
        layer=layer,
    )
    for i in range(num_of_boxes):  # We need 25 boxes to create 24 turns
        # Create and place the box
        # box = meander << pg.compass(size=[length, width],layer=write_on_layer).move([0, i * (width+insulator_width)])
        box = MEANDER << BOX
        box.move([0, i * (width + insulator_width)])

        # Add the boxes to the list
        boxes.append(box)

    # Now create the connecting paths
    BEND = gf.Component()
    reference = BEND << gf.components.bend_euler(
        radius=bending_radius,
        width=width,
        layer=layer,
        allow_min_radius_violation=True,
        angle=90,
        npoints=100,
    )
    for port in reference.ports:
        if port.port_type == "optical":
            port.port_type = "electrical"
            port.name = "e" + port.name[1:]

        BEND.add_port(
            name=port.name,
            port=port,
        )
    # Change the ports to elektrical

    BEND.pprint_ports()
    BEND.draw_ports()
    BEND.show()
    for i in range(0, len(boxes) - 1, 2):  # Skip every second box
        gf.routing.route_single(
            component=MEANDER,
            port1=boxes[i].ports["e3"],
            port2=boxes[i + 1].ports["e3"],
            route_width=width,
            layer=layer,
            bend=BEND,
            # bend=gf.components.bend_euler(
            #     radius=bending_radius, allow_min_radius_violation=True, width=width
            # ),
        )
        gf.routing.route_single(
            component=MEANDER,
            port1=boxes[i + 1].ports["e1"],
            port2=boxes[i + 2].ports["e1"],
            route_width=width,
            layer=layer,
            # bend=bend,
        )

    MEANDER.add_port(
        name="IN1",
        midpoint=[
            length / 2,
            ((num_of_boxes - 1) * width + (num_of_boxes - 1) * insulator_width),
        ],
        width=width,
        orientation=0,
    )
    MEANDER.add_port(
        name="IN2", midpoint=[length / -2, 0], width=width, orientation=180
    )
    MEANDER.rotate(-90, center=(0, 0))

    # Create the taper object
    TAPER = gf.components.taper(
        width1=wire_width, width2=width, length=2 * wire_width, layer=layer
    )
    TAPER.add_port(name="input", center=[0, 0], width=wire_width, orientation=180)
    TAPER.add_port(
        name="output", center=[2 * wire_width, 0], width=width, orientation=0
    )

    # Create the input taper
    taper_device_in = MEANDER << TAPER
    taper_device_out = MEANDER << TAPER

    # Connect the input tapers to the meander
    taper_device_in.connect("output", MEANDER.ports["IN2"])
    taper_device_out.connect("output", MEANDER.ports["IN1"])

    # Add ports to the main device meander
    MEANDER.add_port(name="input", port=taper_device_in.ports["input"])
    MEANDER.add_port(name="output", port=taper_device_out.ports["input"])

    return MEANDER


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    c = rectangle_meander(layer=(2, 5))
    c.plot()
    plt.show()
