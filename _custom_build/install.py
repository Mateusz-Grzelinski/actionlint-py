from __future__ import annotations

from setuptools.command.install import install as orig_install


class install(orig_install):
    sub_commands = orig_install.sub_commands + [('install_actionlint', None)]
