import gdsfactory as gf
from functools import partial


# coupler_ring = partial(gf.components.coupler_ring)
from gdsfactory.components import coupler_ring
from .muxing import two_ring_muxer, bend_two_ring_demuxer
