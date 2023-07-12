import os.path

from .commands import *

# VERSION_ACTIONLINT.txt is version of actionlint library
with open(os.path.join(os.path.dirname(__file__), "VERSION_ACTIONLINT.txt")) as f:
    # VERSION_BUILD_SYTEM.txt is version of this build system
    with open(os.path.join(os.path.dirname(__file__), "VERSION_BUILD_SYTEM.txt")) as ff:
        # used by pyproject.toml
        VERSION = ".".join([f.read().strip(), ff.read().strip()])
