from __future__ import annotations

import os.path

from .bdist_wheel import bdist_wheel
from .build import build
from .fetch_binaries import fetch_binaries
from .install import install
from .install_actionlint import install_actionlint

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
    VERSION = f.read().strip()
