import numpy as np
import gdsfactory as gf
from gdsfactory import Component
from gdsfactory.typings import LayerSpec, CrossSectionSpec
from gdsfactory.components.tapers import *


# @gf.cell
# def taper_metal_to_pad(
#     length: float = 10.0,
#     width1: float = 0.5,
#     width2: float = 0.5,
#     w_slab1: float = 0.15,
#     w_slab2: float = 6.0,
#     layer_metal: LayerSpec = "NEG_NBTIN",
#     layer_slab: LayerSpec = "AU_PADS",
#     cross_section: CrossSectionSpec = "metal1",
#     use_slab_port: bool = False,
# ) -> Component:
#     r"""Linear taper from metal to pad.

#     This is a transition from a strip to a slab. The taper is made of two
#     parts: a strip taper and a slab taper. The strip taper is made of two
#     linear tapers, one for each width. The slab taper is made of two
#     linear tapers, one for each width. The two tapers are connected at the

#     Args:
#         length: taper length (um).
#         width1: in um.
#         width2: in um.
#         w_slab1: slab width in um.
#         w_slab2: slab width in um.
#         layer_wg: for input waveguide.
#         layer_slab: for output waveguide with slab.
#         cross_section: for input waveguide.
#         use_slab_port: if True adds a second port for the slab.

#     .. code::

#                       __________________________
#                      /           |
#              _______/____________|______________
#                    /             |
#        width1     |w_slab1       | w_slab2  width2
#              ______\_____________|______________
#                     \            |
#                      \__________________________

#     """
#     xs = gf.get_cross_section(cross_section)

#     taper_wg = taper(
#         length=length,
#         width1=width1,
#         width2=width2,
#         cross_section=cross_section,
#         layer=layer_metal,
#     )
#     taper_slab = taper(
#         length=length,
#         width1=w_slab1,
#         width2=w_slab2,
#         cross_section=cross_section,
#         with_bbox=False,
#         layer=layer_slab,
#     )

#     c = gf.Component()
#     taper_ref_wg = c << taper_wg
#     taper_ref_slab = c << taper_slab

#     c.info["length"] = length
#     c.add_port(name="o1", port=taper_ref_wg.ports["o1"])
#     if use_slab_port:
#         c.add_port(name="o2", port=taper_ref_slab.ports["o2"])
#     else:
#         c.add_port(name="o2", port=taper_ref_wg.ports["o2"])

#     if length:
#         xs.add_bbox(c)
#     c.flatten()
#     return c


@gf.cell
def transition_taper(
    cross_section_start: CrossSectionSpec | str = "strip",
    cross_section_end: CrossSectionSpec | str = "metal1",
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
        # cross_section=cross_section_end,
    )


# @gf.cell
# def taper_nbtin_au(
#     nbtin_length: float = 10.0,
#     nbtin_end_width: float = 0.5,
#     nbtin_cross_section: CrossSectionSpec = "nbtin",
#     au_cross_section: CrossSectionSpec = "au",
#     au_end_width: float = 0.5,
# ) -> gf.Component:
#     """Taper from strip to nitride."""
#     return gf.components.taper(
#         layer_wg=nbtin_cross_section.layer,
#         layer_slab=au_cross_section.layer,
#         length=nbtin_length,
#         width1=nbtin_cross_section.width,
#         width2=nbtin_end_width,
#         w_slab1=nbtin_cross_section.width,
#         w_slab2=au_end_width,
#         use_slab_port=True,
#         cross_section=nbtin_cross_section,
#     )


# @gf.cell
# def taper_au_nbtin(
#     width1: float = 1,
#     width2: float = 0.5,
#     length: float = 20,
#     layer_nbtin: LayerSpec = "NEG_NBTIN",
#     layer_au: LayerSpec = "AU_PADS",
#     width_tip_nbtin: float = 0.15,
#     width_tip_au: float = 0.15,
#     cross_section: CrossSectionSpec = "metal1",
# ) -> gf.Component:
#     """Taper from Au to NbTiN."""
#     c = gf.Component()
#     taper = taper_nbtin_au(
#         width1=width2,
#         width2=width1,
#         length=length,
#         layer_nbtin=layer_nbtin,
#         layer_au=layer_au,
#         width_tip_au=width_tip_au,
#         width_tip_nbtin=width_tip_nbtin,
#         cross_section=cross_section,
#     )
#     c.copy_child_info(taper)
#     ref = c << taper
#     ref.mirror_x()
#     c.add_ports(ref.ports)
#     c.auto_rename_ports()
#     c.flatten()
#     return c


if __name__ == "__main__":
    c = transition_taper()
    c.show()
