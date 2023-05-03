#!/usr/bin/env python3
from __future__ import annotations

import configparser
import hashlib
import http
import io
import os.path
import platform
import stat
import sys
import tarfile
import urllib.request
import zipfile

from distutils.command.build import build as orig_build
from distutils.core import Command
from setuptools import setup
from setuptools.command.install import install as orig_install

conf = configparser.ConfigParser()
conf.read('./setup.cfg')

# with open("setup.cfg") as configfile:

ACTIONLINT_VERSION = conf['files-to-download']['tag']
POSTFIX_SHA256 = {
    ('linux', 'x86_64'): '_linux_amd64.tar.gz',
    ('darwin', 'x86_64'): '_darwin_amd64.tar.gz',
    ('win32', 'AMD64'): '_windows_amd64.zip',
}
POSTFIX_SHA256[('cygwin', 'x86_64')] = POSTFIX_SHA256[('win32', 'AMD64')]
POSTFIX_SHA256[('darwin', 'x86_64')] = POSTFIX_SHA256[('darwin', 'x86_64')]
POSTFIX_SHA256[('linux', 'x86_64')] = POSTFIX_SHA256[('linux', 'x86_64')]
PY_VERSION = '2'


def get_download_url() -> tuple[str, str]:
    postfix = POSTFIX_SHA256[(sys.platform, platform.machine())]
    sha256 = conf['files-to-download'][postfix]
    url = (
        f'https://github.com/rhysd/actionlint/releases/download/'
        f'v{ACTIONLINT_VERSION}/actionlint_{ACTIONLINT_VERSION}{postfix}'
    )
    return url, sha256


def download(url: str, sha256: str) -> bytes:
    with urllib.request.urlopen(url) as resp:
        code = resp.getcode()
        if code != http.HTTPStatus.OK:
            raise ValueError(f'HTTP failure. Code: {code}')
        data = resp.read()

    checksum = hashlib.sha256(data).hexdigest()
    if checksum != sha256:
        raise ValueError(f'sha256 mismatch, expected {sha256}, got {checksum}')

    return data


def extract(url: str, data: bytes) -> bytes:
    with io.BytesIO(data) as bio:
        if '.tar.' in url:
            with tarfile.open(fileobj=bio) as tarf:
                for info in tarf.getmembers():
                    if info.isfile() and info.name.endswith('actionlint'):
                        return tarf.extractfile(info).read()
        elif url.endswith('.zip'):
            with zipfile.ZipFile(bio) as zipf:
                for info in zipf.infolist():
                    if info.filename.endswith('.exe'):
                        return zipf.read(info.filename)

    raise AssertionError(f'unreachable {url}')


def save_executable(data: bytes, base_dir: str):
    exe = 'actionlint' if sys.platform != 'win32' else 'actionlint.exe'
    output_path = os.path.join(base_dir, exe)
    os.makedirs(base_dir)

    with open(output_path, 'wb') as fp:
        fp.write(data)

    # Mark as executable.
    # https://stackoverflow.com/a/14105527
    mode = os.stat(output_path).st_mode
    mode |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    os.chmod(output_path, mode)


class build(orig_build):
    sub_commands = orig_build.sub_commands + [('fetch_binaries', None)]


class install(orig_install):
    sub_commands = orig_install.sub_commands + [('install_actionlint', None)]


class fetch_binaries(Command):
    build_temp = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.set_undefined_options('build', ('build_temp', 'build_temp'))

    def run(self):
        # save binary to self.build_temp
        url, sha256 = get_download_url()
        archive = download(url, sha256)
        data = extract(url, archive)
        save_executable(data, self.build_temp)


class install_actionlint(Command):
    description = 'install the actionlint executable'
    outfiles = ()
    build_dir = install_dir = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        # this initializes attributes based on other commands' attributes
        self.set_undefined_options('build', ('build_temp', 'build_dir'))
        self.set_undefined_options(
            'install', ('install_scripts', 'install_dir'),
        )

    def run(self):
        self.outfiles = self.copy_tree(self.build_dir, self.install_dir)

    def get_outputs(self):
        return self.outfiles


command_overrides = {
    'install': install,
    'install_actionlint': install_actionlint,
    'build': build,
    'fetch_binaries': fetch_binaries,
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
    setup(version=f'{ACTIONLINT_VERSION}.{PY_VERSION}', cmdclass=command_overrides)
