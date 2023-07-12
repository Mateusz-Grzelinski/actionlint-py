from distutils.command.build import build as orig_build


# todo do not change to setuptools it causes infinite recursion. Do not know why...
# from setuptools.command.build_ext import build_ext as orig_build


class build(orig_build):
    sub_commands = orig_build.sub_commands + [("fetch_binaries", None)]
