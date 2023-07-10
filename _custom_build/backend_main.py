from __future__ import annotations

import configparser
import os
import platform
import sys

from _file_ops import download
from _file_ops import extract
from _file_ops import save_executable
from setuptools import build_meta as _orig
from setuptools.build_meta import *

SETUP_CFG = 'setup.cfg'

conf = configparser.ConfigParser()
conf.read(os.path.join(os.path.dirname(__file__), SETUP_CFG))


# def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
#     metadata = _orig.prepare_metadata_for_build_wheel(
#         metadata_directory, config_settings
#     )
#     return None
#
#
# # def build_sdist(self, sdist_directory, config_settings=None):
# def build_sdist(sdist_directory, config_settings=None):
#     from fetch_binaries import fetch_binaries
#
#     fetch_binaries(_orig.Distribution.patch())
#
#     sdist = _orig.build_sdist(sdist_directory, config_settings)
#     return None
#
#
# # def build_wheel(self, wheel_directory, config_settings=None, metadata_directory=None):
# def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
#     wheel = _orig.build_wheel(wheel_directory, config_settings, metadata_directory)
#     return None
