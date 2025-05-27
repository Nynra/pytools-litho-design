from functools import partial
import gdsfactory as gf
from .racetrack import spiral_racetrack, spiral_racetrack_fixed_length
from .angled_tapers import angled_taper
from .hyper_tapers import hyper_taper
from .tapers import taper, taper_to_ridge, optical_taper, electrical_taper, sine_taper
from .y_splitter import y_split
from .protection_masks import add_protection_mask

rectangle = partial(gf.components.rectangle, layer="ASIC")
