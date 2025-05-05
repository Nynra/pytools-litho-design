import numpy as np
import gdsfactory as gf
from gdsfactory import Component
from gdsfactory.typings import LayerSpec, CrossSectionSpec
from functools import partial

taper = partial(gf.components.taper)
optical_taper = partial(gf.components.taper)
electrical_taper = partial(
    gf.components.taper_electrical,
)


@gf.cell
def optical_transition_taper(
    width1: float | None = None,
    width2: float | None = None,
    cross_section_start: CrossSectionSpec | str = "strip",
    cross_section_end: CrossSectionSpec | str = "rib",
    length: float = 50,
    end_width: float | None = None,
    start_width: float | None = None,
) -> gf.Component:
    """Transition taper from one cross section to another.

    Parameters
    -----------
    cross_section_start: CrossSectionSpec | str
        The starting cross section of the taper.
    cross_section_end: CrossSectionSpec | str
        The ending cross section of the taper.
    length: float
        The length of the taper.
    end_width: float | None
        The width at the end of the taper. If None, defaults to the width of the starting cross section.
    start_width: float | None
        The width at the start of the taper. If None, defaults to the width of the ending cross section.

    Returns
    --------
    gf.Component
        The component representing the transition taper.
    """
    if isinstance(cross_section_start, str):
        cross_section_start = gf.get_cross_section(cross_section_start)
    if isinstance(cross_section_end, str):
        cross_section_end = gf.get_cross_section(cross_section_end)
    if end_width is None:
        end_width = cross_section_start.width
    if start_width is None:
        start_width = cross_section_end.width

    return gf.components.taper_strip_to_ridge(
        layer_wg=cross_section_start.layer,
        layer_slab=cross_section_end.layer,
        length=length,
        width1=cross_section_start.width,
        width2=end_width,
        w_slab1=start_width,
        w_slab2=cross_section_end.width,
        use_slab_port=True,
        # cross_section=cross_section_end,
    )


@gf.cell
def electrical_transition_taper(
    length: float = 50,
    width1: float | None = None,
    width2: float | None = None,
    w_slab1: float | None = None,
    w_slab2: float | None = None,
    cross_section_start: CrossSectionSpec | str = "metal2",
    cross_section_end: CrossSectionSpec | str = "metal1",
    end_width: float | None = None,
    start_width: float | None = None,
):
    if isinstance(cross_section_start, str):
        cross_section_start = gf.get_cross_section(cross_section_start)
    if isinstance(cross_section_end, str):
        cross_section_end = gf.get_cross_section(cross_section_end)
    if width1 is None:
        width1 = cross_section_start.width
    if width2 is None:
        width2 = cross_section_end.width
    if end_width is None:
        end_width = cross_section_start.width
    if start_width is None:
        start_width = cross_section_end.width

    xs = gf.get_cross_section(cross_section_start)

    taper_wg = electrical_taper(
        length=length,
        width1=width1,
        width2=width2,
        cross_section=cross_section_start,
        # layer=layer_wg,
    )
    taper_slab = electrical_taper(
        length=length,
        width1=w_slab1,
        width2=w_slab2,
        cross_section=cross_section_end,
        with_bbox=False,
        # layer=layer_slab,
    )

    c = gf.Component()
    taper_ref_wg = c << taper_wg
    taper_ref_slab = c << taper_slab

    c.info["length"] = length
    c.add_port(name="e1", port=taper_ref_wg.ports["e1"])
    c.add_port(name="e2", port=taper_ref_slab.ports["e2"])

    if length:
        xs.add_bbox(c)
    c.flatten()
    return c


taper_cross_section = partial(
    gf.components.taper_cross_section,
    cross_section1="strip_rib_tip",
    cross_section2="strip",
)
if __name__ == "__main__":
    # c = transition_taper(
    #     width1=1.0,
    #     width2=0.5,
    #     length=10.0,
    #     cross_section_start="strip",
    #     cross_section_end="metal1",
    # )
    # c = electrical_transition_taper()
    c = optical_transition_taper()
    c.draw_ports()
    c.show()
