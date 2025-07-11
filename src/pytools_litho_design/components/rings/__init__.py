import gdsfactory as gf
from functools import partial
from .muxing import two_ring_muxer, bend_two_ring_demuxer

coupler_ring = partial(gf.components.coupler_ring, cross_section="asic_ridge")
