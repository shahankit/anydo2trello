import os
import sys

HOME = os.path.expanduser("~/")
ANYDO_API = HOME + "python-anydo/"

sys.path.append(ANYDO_API)

from anydo.api import AnyDoAP

del sys.path[-1]

