import os

# VERSION_ACTIONLINT.txt is version of actionlint library
_this_dir = os.path.dirname(__file__)
with open(os.path.join(_this_dir, "VERSION_ACTIONLINT.txt")) as f:
    # VERSION_BUILD_SYSTEM.txt is version of this build system
    with open(os.path.join(_this_dir, "VERSION_BUILD_SYSTEM.txt")) as ff:
        # used by pyproject.toml
        VERSION = ".".join([f.read().strip(), ff.read().strip()])

if __name__ == "__main__":
    print(VERSION)
