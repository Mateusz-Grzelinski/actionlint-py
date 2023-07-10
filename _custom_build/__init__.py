from __future__ import annotations

import os.path

from .fetch_binaries import fetch_binaries
from .install_actionlint import install_actionlint

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
    VERSION = f.read().strip()

from . import setup
