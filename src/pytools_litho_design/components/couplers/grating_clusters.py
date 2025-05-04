import gdsfactory as gf
import pytools_litho_design as pld
import gdsfactory as gf


@gf.cell
def grating_coupler_cluster(
    coupler: gf.Component | str = "grating_coupler_traditional",
    row_offset: int = 150,
    column_offset: int = 600,
    cross_section: gf.CrossSection | str = "strip",
):
    if isinstance(cross_section, str):
        cross_section = gf.get_cross_section(cross_section)
    if isinstance(coupler, str):
        coupler = gf.get_component(coupler)

    # Create the chip and create the layout
    CHIP = gf.Component()
    grating1 = CHIP << coupler
    grating2 = CHIP << coupler
    grating3 = CHIP << coupler
    grating4 = CHIP << coupler
    grating5 = CHIP << coupler
    grating6 = CHIP << coupler
    grating7 = CHIP << coupler
    grating8 = CHIP << coupler

    # Position the gratings
    grating2.rotate(180)
    grating2.center = (grating1.x - column_offset, grating1.y)
    grating3.rotate(180)
    grating3.center = (grating1.x, grating1.y - row_offset)
    grating4.center = (grating2.x, grating2.y - row_offset)
    grating5.center = (grating3.x, grating3.y - row_offset)
    grating6.rotate(180)
    grating6.center = (grating4.x, grating4.y - row_offset)
    grating7.rotate(180)
    grating7.center = (grating5.x, grating5.y - row_offset)
    grating8.center = (grating6.x, grating6.y - row_offset)

    # Create 4 ports at the top and 4 at the bottom
    OUTPUT_GUIDE = gf.components.waveguides.straight(
        length=10,
        cross_section=cross_section,
    )
    output1 = CHIP << OUTPUT_GUIDE
    output2 = CHIP << OUTPUT_GUIDE
    output3 = CHIP << OUTPUT_GUIDE
    output4 = CHIP << OUTPUT_GUIDE
    output5 = CHIP << OUTPUT_GUIDE
    output6 = CHIP << OUTPUT_GUIDE
    output7 = CHIP << OUTPUT_GUIDE
    output8 = CHIP << OUTPUT_GUIDE

    # 1, 4, 5, 8 at the bottom
    guide_spacing = column_offset / 6
    output_offset = row_offset
    output5.rotate(-90)
    output5.center = (grating7.x - 1.5 * guide_spacing, grating7.y - output_offset)
    output1.rotate(-90)
    output1.center = (grating7.x - 2.5 * guide_spacing, grating7.y - output_offset)
    output8.rotate(-90)
    output8.center = (grating8.x - 1.5 * guide_spacing, grating8.y - output_offset)
    output4.rotate(-90)
    output4.center = (grating8.x - 2.5 * guide_spacing, grating8.y - output_offset)

    # 2, 3, 6, 7 at the top
    output6.rotate(90)
    output6.center = (grating1.x - 3.5 * guide_spacing, grating1.y + output_offset)
    output2.rotate(90)
    output2.center = (grating1.x - 4.5 * guide_spacing, grating1.y + output_offset)
    output3.rotate(90)
    output3.center = (grating1.x + 1.5 * guide_spacing, grating2.y + output_offset)
    output7.rotate(90)
    output7.center = (grating1.x + 2.5 * guide_spacing, grating2.y + output_offset)

    # Route the waveguides
    gf.routing.route_bundle(
        CHIP,
        [
            grating1.ports["o1"],
            grating5.ports["o1"],
        ],
        [
            output1.ports["o1"],
            output5.ports["o1"],
        ],
        cross_section=cross_section,
    )
    gf.routing.route_bundle(
        CHIP,
        [
            grating3.ports["o1"],
            grating7.ports["o1"],
        ],
        [
            output3.ports["o1"],
            output7.ports["o1"],
        ],
        cross_section=cross_section,
    )
    gf.routing.route_bundle(
        CHIP,
        [
            grating2.ports["o1"],
            grating6.ports["o1"],
            #         grating7.ports["o1"],
            #         grating8.ports["o1"],
        ],
        [
            output2.ports["o1"],
            output6.ports["o1"],
            #         output7.ports["o1"],
            #         output8.ports["o1"],
        ],
        cross_section=cross_section,
    )
    gf.routing.route_bundle(
        CHIP,
        [
            grating4.ports["o1"],
            grating8.ports["o1"],
        ],
        [
            output4.ports["o1"],
            output8.ports["o1"],
        ],
        cross_section=cross_section,
    )

    FINAL_CHIP = gf.Component()
    FINAL_CHIP << CHIP
    FINAL_CHIP.add_port("o1", port=output1.ports["o2"], cross_section="strip")
    FINAL_CHIP.add_port("o2", port=output2.ports["o2"], cross_section="strip")
    FINAL_CHIP.add_port("o3", port=output3.ports["o2"], cross_section="strip")
    FINAL_CHIP.add_port("o4", port=output4.ports["o2"], cross_section="strip")
    FINAL_CHIP.add_port("o5", port=output5.ports["o2"], cross_section="strip")
    FINAL_CHIP.add_port("o6", port=output6.ports["o2"], cross_section="strip")
    FINAL_CHIP.add_port("o7", port=output7.ports["o2"], cross_section="strip")
    FINAL_CHIP.add_port("o8", port=output8.ports["o2"], cross_section="strip")
    FINAL_CHIP.flatten()
    return FINAL_CHIP


if __name__ == "__main__":
    c = grating_coupler_cluster(
        coupler="grating_coupler_traditional",
        row_offset=150,
        column_offset=600,
    )
    c.show()
