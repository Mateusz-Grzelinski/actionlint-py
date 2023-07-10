from __future__ import annotations

from distutils.command.build import build as orig_build


class build(orig_build):
    sub_commands = orig_build.sub_commands + [('fetch_binaries', None)]
