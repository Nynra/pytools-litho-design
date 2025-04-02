import numpy as np
import gdsfactory as gf
from gdsfactory import Component
from gdsfactory.typings import LayerSpec, CrossSectionSpec
from gdsfactory.components.tapers import *


@gf.cell
def taper_metal_to_pad(
    length: float = 10.0,
    width1: float = 0.5,
    width2: float = 0.5,
    w_slab1: float = 0.15,
    w_slab2: float = 6.0,
    layer_metal: LayerSpec = "NEG_NBTIN",
    layer_slab: LayerSpec = "AU_PADS",
    cross_section: CrossSectionSpec = "metal1",
    use_slab_port: bool = False,
) -> Component:
    r"""Linear taper from metal to pad.

    This is a transition from a strip to a slab. The taper is made of two
    parts: a strip taper and a slab taper. The strip taper is made of two
    linear tapers, one for each width. The slab taper is made of two
    linear tapers, one for each width. The two tapers are connected at the

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
    xs = gf.get_cross_section(cross_section)

    taper_wg = taper(
        length=length,
        width1=width1,
        width2=width2,
        cross_section=cross_section,
        layer=layer_metal,
    )
    taper_slab = taper(
        length=length,
        width1=w_slab1,
        width2=w_slab2,
        cross_section=cross_section,
        with_bbox=False,
        layer=layer_slab,
    )

    c = gf.Component()
    taper_ref_wg = c << taper_wg
    taper_ref_slab = c << taper_slab

    c.info["length"] = length
    c.add_port(name="o1", port=taper_ref_wg.ports["o1"])
    if use_slab_port:
        c.add_port(name="o2", port=taper_ref_slab.ports["o2"])
    else:
        c.add_port(name="o2", port=taper_ref_wg.ports["o2"])

    if length:
        xs.add_bbox(c)
    c.flatten()
    return c


@gf.cell
def taper_nbtin_au(
    width1: float = 0.5,
    width2: float = 1,
    length: float = 20,
    layer_nbtin: LayerSpec = "NEG_NBTIN",
    layer_au: LayerSpec = "AU_PADS",
    width_tip_nbtin: float = 0.15,
    width_tip_au: float = 0.15,
    cross_section: CrossSectionSpec = "metal1",
) -> gf.Component:
    """Taper from strip to nitride."""
    return gf.components.taper(
        layer_wg=layer_nbtin,
        layer_slab=layer_au,
        length=length,
        width1=width1,
        width2=width_tip_nbtin,
        w_slab1=width_tip_au,
        w_slab2=width2,
        use_slab_port=True,
        cross_section=cross_section,
    )


@gf.cell
def taper_au_nbtin(
    width1: float = 1,
    width2: float = 0.5,
    length: float = 20,
    layer_nbtin: LayerSpec = "NEG_NBTIN",
    layer_au: LayerSpec = "AU_PADS",
    width_tip_nbtin: float = 0.15,
    width_tip_au: float = 0.15,
    cross_section: CrossSectionSpec = "metal1",
) -> gf.Component:
    """Taper from Au to NbTiN."""
    c = gf.Component()
    taper = taper_nbtin_au(
        width1=width2,
        width2=width1,
        length=length,
        layer_nbtin=layer_nbtin,
        layer_au=layer_au,
        width_tip_au=width_tip_au,
        width_tip_nbtin=width_tip_nbtin,
        cross_section=cross_section,
    )
    c.copy_child_info(taper)
    ref = c << taper
    ref.mirror_x()
    c.add_ports(ref.ports)
    c.auto_rename_ports()
    c.flatten()
    return c
