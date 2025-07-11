"""Library of pre-built cells containing text, border marks, and an experiment,
connected to pads for wirebonding."""

from phidl import Device
import phidl.geometry as pg
import phidl.routing as pr
from typing import Tuple, List, Union, Optional
import math
import numpy as np
from numpy.typing import ArrayLike

import qnngds.tests as test
import qnngds.devices as devices
import qnngds.circuits as circuit
import qnngds.utilities as utility

# basics


## devices:
