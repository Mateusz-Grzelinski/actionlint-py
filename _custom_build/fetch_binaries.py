from __future__ import annotations

import configparser
import logging
import os
import platform
import sys

from distutils.core import Command
from setuptools import Command
from setuptools.command.build import SubCommand

from ._file_ops import download
from ._file_ops import extract
from ._file_ops import save_executable

logging.basicConfig(level=logging.INFO)
SETUP_CFG = os.path.join(os.path.dirname(__file__), 'setup.cfg')


class fetch_binaries(Command):
    build_temp = None
    user_options: list[tuple] = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.set_undefined_options('build', ('build_temp', 'build_temp'))

    def run(self):
        # save binary to self.build_temp
        # url, sha256 = get_download_url()
        config = configparser.ConfigParser()
        config.read(SETUP_CFG)
        section = sys.platform + '-' + platform.machine()
        url = config[section]['url']
        sha256 = config[section]['checksum']
        archive = download(url, sha256)
        data = extract(url, archive)
        out = save_executable(data, self.build_temp)
        print(f'Downloaded executable for {section}: {out}')
