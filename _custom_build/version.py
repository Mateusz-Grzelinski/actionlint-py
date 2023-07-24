import os
from argparse import ArgumentParser

# VERSION_ACTIONLINT.txt is version of actionlint library
_this_dir = os.path.dirname(__file__)
with open(os.path.join(_this_dir, "VERSION_ACTIONLINT.txt")) as f:
    # VERSION_BUILD_SYSTEM.txt is version of this build system
    with open(os.path.join(_this_dir, "VERSION_BUILD_SYSTEM.txt")) as f_build:
        with open(os.path.join(_this_dir, "VERSION_DEV.txt")) as f_dev:
            # used by pyproject.toml
            VERSION = ".".join([f.read().strip(), f_build.read().strip()])
            __dev_version = f_dev.read().strip()
            if __dev_version != "0":
                VERSION += f".dev.{__dev_version}"


def main():
    args = ArgumentParser()
    args.add_argument("--release", description="error if in version contains '.dev.N' string")
    return args.parse_args()


if __name__ == "__main__":
    args = main()
    if args.release and ".dev." in VERSION:
        print(f"ERROR: the version is {VERSION} and should not contain .dev.N")
        exit(1)
    print(VERSION)
