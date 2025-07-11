import numpy as np
import gdsfactory as gf
from gdsfactory import Component
from gdsfactory.typings import LayerSpec, CrossSectionSpec, Port
from gdsfactory.cross_section import port_names_electrical, port_types_electrical
from functools import partial

# taper = partial(gf.components.taper)
# from gdsfactory.components import taper

taper = partial(gf.components.taper, cross_section="asic")
optical_taper = taper
electrical_taper = partial(gf.components.taper_electrical, cross_section="nbtin")


@gf.cell
def sine_taper(
    length: float = 10.0,
    width1: float = 0.5,
    width2: float | None = None,
    cross_section: CrossSectionSpec = "asic",
    npoints=100,
    **kwargs,
) -> gf.Component:
    # IMPORTANT
    # This method only works if we use the str version of the cross_section.
    # no idea why, but it does not work with the CrossSection object, it ignores the second width
    if not isinstance(cross_section, str):
        cross_section = cross_section.name
    cs1 = gf.get_cross_section(cross_section, width=width1)
    cs2 = gf.get_cross_section(cross_section, width=width2)

    transition = gf.cross_section.Transition(cross_section1=cs1, cross_section2=cs2)
    path = gf.path.straight(length=length, npoints=npoints)
    return gf.path.extrude_transition(path, transition)


@gf.cell
def neg_taper(
    length: float = 10.0,
    width1: float = 0.5,
    width2: float | None = None,
    layer: LayerSpec | None = None,
    port: Port | None = None,
    with_two_ports: bool = True,
    cross_section: CrossSectionSpec = "strip",
    port_names: tuple[str, str] = ("o1", "o2"),
    port_types: tuple[str, str] = ("optical", "optical"),
    with_bbox: bool = True,
) -> gf.Component:
    """Linear taper, which tapers only the main cross section section.

    Args:
        length: taper length.
        width1: width of the west/left port.
        width2: width of the east/right port. Defaults to width1.
        layer: layer for the taper.
        port: can taper from a port instead of defining width1.
        with_two_ports: includes a second port.
            False for terminator and edge coupler fiber interface.
        cross_section: specification (CrossSection, string, CrossSectionFactory dict).
        port_names: input and output port names. Second name only used if with_two_ports.
        port_types: input and output port types. Second type only used if with_two_ports.
        with_bbox: box in bbox_layers and bbox_offsets to avoid DRC sharp edges.
    """
    if len(port_types) != 2:
        raise ValueError("port_types should have two elements")

    x1 = gf.get_cross_section(cross_section, width=width1)
    if width2:
        width2 = gf.snap.snap_to_grid2x(width2)
        x2 = gf.get_cross_section(cross_section, width=width2)
    else:
        x2 = x1

    width1 = x1.width
    width2 = x2.width
    width_max = max([width1, width2])
    if layer:
        x = gf.get_cross_section(cross_section, width=width_max, layer=layer)
    else:
        x = gf.get_cross_section(cross_section, width=width_max)
    layer = layer or x.layer
    assert layer is not None

    if isinstance(port, gf.Port):
        width1 = port.width

    width2 = width2 or width1
    c = gf.Component()
    y1 = width1 / 2
    y2 = width2 / 2

    if length:
        mp1 = gf.kdb.DPolygon(
            [
                gf.kdb.DPoint(0, y1),
                gf.kdb.DPoint(length, y2),
                gf.kdb.DPoint(length, -y2),
                gf.kdb.DPoint(0, -y1),
            ]
        )
        # c.add_polygon(p1, layer=layer)

        s0_width = 0  # x.sections[0].width
        polies = []
        for section in x.sections[1:3]:
            delta_width = abs(section.width - s0_width)
            y1 = (width1 + delta_width) / 2
            y2 = (width2 + delta_width) / 2
            polies.append(
                gf.kdb.DPolygon(
                    [
                        gf.kdb.DPoint(0, y1),
                        gf.kdb.DPoint(length, y2),
                        gf.kdb.DPoint(length, -y2),
                        gf.kdb.DPoint(0, -y1),
                    ]
                )
            )
            # c.add_polygon(p1, layer=section.layer)

        p1: gf.kdb.DPolygon = polies.pop(0)
        p2: gf.kdb.DPolygon = polies.pop(0)
        r0 = gf.Region(mp1.to_itype(gf.kcl.dbu))
        r1 = gf.Region(p1.to_itype(gf.kcl.dbu))
        r2 = gf.Region(p2.to_itype(gf.kcl.dbu))
        r3 = r1 + r2
        r4 = r3 - r0
        c.add_polygon(r4, layer=layer)

        for section in x.sections[3:]:
            delta_width = abs(section.width - s0_width)
            y1 = (width1 + delta_width) / 2
            y2 = (width2 + delta_width) / 2
            polies.append(
                gf.kdb.DPolygon(
                    [
                        gf.kdb.DPoint(0, y1),
                        gf.kdb.DPoint(length, y2),
                        gf.kdb.DPoint(length, -y2),
                        gf.kdb.DPoint(0, -y1),
                    ]
                )
            )
            c.add_polygon(p1, layer=section.layer)

    if with_bbox:
        x.add_bbox(c)
    c.add_port(
        name=port_names[0],
        center=(0, 0),
        width=width1,
        orientation=180,
        layer=layer,
        cross_section=x1,
        port_type=port_types[0],
    )
    if with_two_ports:
        c.add_port(
            name=port_names[1],
            center=(length, 0),
            width=width2,
            orientation=0,
            layer=layer,
            cross_section=x2,
            port_type=port_types[1],
        )

    c.info["length"] = length
    c.info["width1"] = float(width1)
    c.info["width2"] = float(width2)
    return c


neg_optical_taper = partial(neg_taper, cross_section="neg_asic")
neg_electrical_taper = partial(
    neg_taper,
    cross_section="neg_asic",
    port_names=port_names_electrical,
    port_types=port_types_electrical,
)


@gf.cell
def taper_to_ridge(
    width1: float = 0.5,
    width2: float = 0.5,
    length: float = 10.0,
    slab_length: float = 5,
    w_slab1: float = 0.15,
    w_slab2: float = 6.0,
    main_cross_section: CrossSectionSpec = "asic",
    slab_cross_section: CrossSectionSpec = "sio2",
    use_slab_port: bool = True,
    port_type: str = "optical",
    type: str = "sine",
) -> gf.Component:
    r"""Linear taper between layers.

    Used to transition between layers of the same port type (optical or electrical)

    .. attention::

        Only works when both layers have the same port type.

    Args:
        length: taper length (um).
        width1: in um.
        width2: in um.
        w_slab1: slab width in um.
        w_slab2: slab width in um.
        layer_wg: for input waveguide.
        layer_slab: for output waveguide with slab.
        cross_section: for input waveguide.
        use_slab_port: if True adds a second port for the slab.

    .. code::

                      __________________________
                     /           |
             _______/____________|______________
                   /             |
       width1     |w_slab1       | w_slab2  width2
             ______\_____________|______________
                    \            |
                     \__________________________

    """
    main_xs = gf.get_cross_section(main_cross_section)
    slab_xs = gf.get_cross_section(slab_cross_section)

    taper_slab = sine_taper(
        length=slab_length,
        width1=w_slab1,
        width2=w_slab2,
        cross_section=slab_cross_section,
    )
    taper_wg = sine_taper(
        length=length,
        width1=width1,
        width2=width2,
        cross_section=main_cross_section,
    )

    c = gf.Component()
    taper_ref_wg = c << taper_wg
    taper_ref_slab = c << taper_slab

    c.info["length"] = length
    if port_type == "optical":
        c.add_port(name="o1", port=taper_ref_wg.ports["o2"])
        if not use_slab_port:
            c.add_port(name="o2", port=taper_ref_slab.ports["o1"])
        else:
            c.add_port(name="o2", port=taper_ref_wg.ports["o1"])
    elif port_type == "electrical":
        c.add_port(name="e1", port=taper_ref_slab.ports["e2"])
        if not use_slab_port:
            c.add_port(name="e2", port=taper_ref_slab.ports["e1"])
        else:
            c.add_port(name="e2", port=taper_ref_wg.ports["e1"])
    else:
        raise ValueError("Unknown port type")

    # if length:
    # xs.add_bbox(c)
    c.flatten()
    return c


# @gf.cell
# def optical_transition_taper(
#     width1: float | None = None,
#     width2: float | None = None,
#     cross_section_start: CrossSectionSpec | str = "strip",
#     cross_section_end: CrossSectionSpec | str = "rib",
#     length: float = 50,
#     end_width: float | None = None,
#     start_width: float | None = None,
# ) -> gf.Component:
#     """Transition taper from one cross section to another.

#     Parameters
#     -----------
#     cross_section_start: CrossSectionSpec | str
#         The starting cross section of the taper.
#     cross_section_end: CrossSectionSpec | str
#         The ending cross section of the taper.
#     length: float
#         The length of the taper.
#     end_width: float | None
#         The width at the end of the taper. If None, defaults to the width of the starting cross section.
#     start_width: float | None
#         The width at the start of the taper. If None, defaults to the width of the ending cross section.

#     Returns
#     --------
#     gf.Component
#         The component representing the transition taper.
#     """
#     if isinstance(cross_section_start, str):
#         cross_section_start = gf.get_cross_section(cross_section_start)
#     if isinstance(cross_section_end, str):
#         cross_section_end = gf.get_cross_section(cross_section_end)
#     if end_width is None:
#         end_width = cross_section_start.width
#     if start_width is None:
#         start_width = cross_section_end.width

#     return gf.components.taper_strip_to_ridge(
#         layer_wg=cross_section_start.layer,
#         layer_slab=cross_section_end.layer,
#         length=length,
#         width1=cross_section_start.width,
#         width2=end_width,
#         w_slab1=start_width,
#         w_slab2=cross_section_end.width,
#         use_slab_port=True,
#         # cross_section=cross_section_end,
#     )


# @gf.cell
# def electrical_transition_taper(
#     length: float = 50,
#     cross_section_start: CrossSectionSpec | str = "metal2",
#     cross_section_end: CrossSectionSpec | str = "metal1",
#     end_width: float | None = None,
#     start_width: float | None = None,
#     **kwargs,
# ):
#     if isinstance(cross_section_start, str):
#         cross_section_start = gf.get_cross_section(cross_section_start)
#     if isinstance(cross_section_end, str):
#         cross_section_end = gf.get_cross_section(cross_section_end)
#     # if width1 is None:
#     #     width1 = cross_section_start.width
#     # if width2 is None:
#     #     width2 = cross_section_end.width
#     if end_width is None:
#         end_width = cross_section_start.width
#     if start_width is None:
#         start_width = cross_section_end.width

#     xs = gf.get_cross_section(cross_section_start)

#     taper_wg = electrical_taper(
#         length=length,
#         cross_section=cross_section_start,
#         # layer=layer_wg,
#     )
#     taper_slab = electrical_taper(
#         length=length,
#         cross_section=cross_section_end,
#         with_bbox=False,
#         # layer=layer_slab,
#     )

#     c = gf.Component()
#     taper_ref_wg = c << taper_wg
#     taper_ref_slab = c << taper_slab

#     c.info["length"] = length
#     c.add_port(name="e1", port=taper_ref_wg.ports["e1"])
#     c.add_port(name="e2", port=taper_ref_slab.ports["e2"])

#     if length:
#         xs.add_bbox(c)
#     c.flatten()
#     return c


if __name__ == "__main__":
    # c = transition_taper(
    #     width1=1.0,
    #     width2=0.5,
    #     length=10.0,
    #     cross_section_start="strip",
    #     cross_section_end="metal1",
    # )
    # c = electrical_transition_taper()
    c = taper_to_ridge(
        length=50,
        width1=1.0,
        width2=0.5,
        w_slab1=0.5,
        w_slab2=0.5,
        layer_wg="WG",
        layer_slab="WG",
        cross_section="strip",
    )
    c.draw_ports()
    c.show()
