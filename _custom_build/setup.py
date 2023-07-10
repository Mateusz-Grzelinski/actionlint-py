from __future__ import annotations

import configparser
import os

from distutils.command.build import build as orig_build
from setuptools import setup
from setuptools.build_meta import *
from setuptools.command.install import install as orig_install


class build(orig_build):
    sub_commands = orig_build.sub_commands + [('fetch_binaries', None)]


class install(orig_install):
    sub_commands = orig_install.sub_commands + [('install_actionlint', None)]

    def run(self):
        super().run()


command_overrides = {
    'install': install,
    'build': build,
    'build_py': build,
}

try:
    from wheel.bdist_wheel import bdist_wheel as orig_bdist_wheel
except ImportError:
    pass
else:

    class bdist_wheel(orig_bdist_wheel):
        def finalize_options(self):
            orig_bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package
            self.root_is_pure = False

        def get_tag(self):
            _, _, plat = orig_bdist_wheel.get_tag(self)
            # We don't contain any python source, nor any python extensions
            return 'py2.py3', 'none', plat

    command_overrides['bdist_wheel'] = bdist_wheel

if __name__ == '__main__':
    setup(cmdclass=command_overrides)
