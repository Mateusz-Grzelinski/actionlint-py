import configparser
import os
import platform
import sys

from setuptools import Command

from ..utils.file_ops import download
from ..utils.file_ops import extract
from ..utils.file_ops import save_executable

SETUP_CFG = os.path.join(os.path.dirname(__file__), "..", "checksums.cfg")


class fetch_binaries(Command):
    description = "fetch binaries based on config in checksums.cfg"
    build_temp = None
    user_options: "list[tuple]" = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.set_undefined_options("build", ("build_temp", "build_temp"))

    def run(self):
        # save binary to self.build_temp
        config = configparser.ConfigParser()
        config.read(SETUP_CFG)
        section = sys.platform + "-" + platform.machine()
        url = config[section]["url"]
        sha256 = config[section]["checksum"]
        archive = download(url, sha256)
        data = extract(url, archive)
        out = save_executable(data, self.build_temp)
        print(f"Downloaded executable for {section}: {out}")
