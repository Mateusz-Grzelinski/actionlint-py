import os
from argparse import ArgumentParser

_this_dir = os.path.dirname(__file__)
# VERSION_ACTIONLINT.txt is version of actionlint library
VERSION_ACTIONLINT_TXT = os.path.join(_this_dir, "VERSION_ACTIONLINT.txt")
VERSION_BUILD_SYSTEM_TXT = os.path.join(_this_dir, "VERSION_BUILD_SYSTEM.txt")
VERSION_DEV_TXT = os.path.join(_this_dir, "VERSION_DEV.txt")
GITHUB_OUT = os.getenv("GITHUB_OUTPUT")


def get_pip_version():
    global VERSION
    with open(VERSION_ACTIONLINT_TXT) as f:
        # VERSION_BUILD_SYSTEM.txt is version of this build system
        with open(VERSION_BUILD_SYSTEM_TXT) as f_build:
            with open(VERSION_DEV_TXT) as f_dev:
                # used by pyproject.toml
                v = ".".join([f.read().strip(), f_build.read().strip()])
                __dev_version = f_dev.read().strip()
                if __dev_version != "0":
                    v += f".dev.{__dev_version}"
                return v


def get_actionlint_version():
    with open(VERSION_ACTIONLINT_TXT) as r:
        return r.read().strip()


VERSION = get_pip_version()


def increment_build_version():
    with open(VERSION_BUILD_SYSTEM_TXT) as f:
        version = int(f.read().strip())
    with open(VERSION_BUILD_SYSTEM_TXT, "w") as f_w:
        f_w.write(f"{version + 1}\n")


def increment_dev_version():
    with open(VERSION_DEV_TXT) as f:
        version = int(f.read().strip())
    with open(VERSION_DEV_TXT, "w") as f_w:
        f_w.write(f"{version + 1}\n")


def reset_dev_version():
    with open(VERSION_DEV_TXT, "w") as f_w:
        f_w.write(f"0\n")


def main():
    args = ArgumentParser()
    args.add_argument("--release", help="error if in version contains '.dev.N' string", action="store_true")
    args.add_argument("--increment-build", help="increment VERSION_BUILD_SYSTEM.txt", action="store_true")
    args.add_argument("--increment-dev", help="increment VERSION_DEV.txt", action="store_true")
    args.add_argument("--reset-dev", help="set VERSION_DEV.txt to 0", action="store_true")
    return args.parse_args()


README = os.path.join(_this_dir, "..", "README.md")


def fix_readme(old_version: str, new_version: str):
    with open(README, "r") as f_r:
        f_content = f_r.read()
    with open(README, "w") as f_w:
        new_f_content = f_content.replace(old_version, new_version)
        f_w.write(new_f_content)


if __name__ == "__main__":
    args = main()
    if args.release and ".dev." in VERSION:
        print(f"ERROR: the version is {VERSION} and should not contain .dev.N")
        exit(1)
    prev_version = get_pip_version()
    if args.increment_build:
        increment_build_version()
    if args.increment_dev:
        increment_dev_version()
    if args.reset_dev:
        reset_dev_version()
    current_version = get_pip_version()
    if prev_version != current_version:
        fix_readme(prev_version, current_version)
    print(current_version)
