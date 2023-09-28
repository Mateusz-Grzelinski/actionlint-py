import configparser
import logging
import os
from dataclasses import dataclass
from typing import Iterable
from version import VERSION_ACTIONLINT_TXT, reset_dev_version, get_actionlint_version, get_pip_version, VERSION

import requests
import semver
from requests_html import HTMLSession

README_MD = os.path.join(os.path.dirname(__file__), "..", "README.md")
assert os.path.isfile(README_MD), (os.getcwd(), README_MD)

ACTIONLINT_RELEASES = "https://github.com/rhysd/actionlint/releases/"  # must end with "/"
SETUP_CFG = os.path.join(os.path.dirname(__file__), "checksums.cfg")
GITHUB_OUT = os.getenv("GITHUB_OUTPUT")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def get_release_page_links():
    session = HTMLSession()
    r = session.get(ACTIONLINT_RELEASES)
    return r.html.links


def get_checksum_file(newest_release_link: str) -> str:
    checksums_file = requests.get("https://github.com" + newest_release_link)
    # checksum_file_name = newest_release_link.split('/')[-1]
    content = checksums_file.content.decode("utf-8")
    return content


def get_newest_release_link(links: Iterable[str]) -> str:
    newest_release_link = None
    for link in links:
        link: str
        if link.endswith("_checksums.txt"):
            newest_release_link = link
            break
    return newest_release_link


def update_config(checksum_file_content: str, current_version: str, newest_version_str: str) -> None:
    """Update tag and checksum in config file

    Config file format:

    ```
    [python_platform-python_machine]
    file_name=actionlint_1.6.25_linux_amd64.tar.gz  ; format of this file is important
    checksum=...
    url=...  ; download url
    ```
    """
    config = configparser.ConfigParser()
    config.read(SETUP_CFG)
    checksums: dict[str, ChecksumInfo] = {c.filename: c for c in get_checksums(checksum_file_content)}
    for sec in config.sections():
        platform_config = config[sec]
        new_file_name = platform_config["file_name"].replace(current_version, newest_version_str)
        platform_config["file_name"] = new_file_name
        url = f"https://github.com/rhysd/actionlint/releases/download/v{newest_version_str}/{new_file_name}"
        platform_config["url"] = url
        platform_config["checksum"] = checksums[new_file_name].checksum

    with open(SETUP_CFG, "w") as file:
        config.write(file, space_around_delimiters=True)


def update_actionlint_version(newest_version_str):
    with open(VERSION_ACTIONLINT_TXT, "w") as file:
        file.write(newest_version_str)
    reset_dev_version()  # just to be sure


def update_readme(current_version: str, new_version: str):
    """execute as last - the order of version is re-read from files"""
    with open(README_MD, "r") as readme_ro:
        contents = readme_ro.read()
        contents = contents.replace(VERSION, get_pip_version())
        contents = contents.replace(current_version, new_version)
    with open(README_MD, "w") as readme_rw:
        readme_rw.write(contents)


@dataclass(frozen=True)
class ChecksumInfo:
    version: str
    filename: str
    postfix: str
    checksum: str


def get_checksums(checksum_file_content):
    for line in checksum_file_content.split("\n"):
        if not line:
            continue
        checksum, file = line.split()
        exe_name, version, platform, machine_with_extension = file.split("_")
        file_ending = "_" + platform + "_" + machine_with_extension
        yield ChecksumInfo(
            version=checksum,
            checksum=checksum,
            filename=file,
            postfix=file_ending,
        )


def write_github_output(newest_version, newest_version_str, is_update_required: bool):
    if GITHUB_OUT is None:
        return
    with open(GITHUB_OUT, "a") as file:
        file.write(f"version={newest_version_str}\n")
        file.write(f"update_required={is_update_required}\n")
        file.write(f"release_url={ACTIONLINT_RELEASES}tag/v{newest_version}\n")


def main():
    links = get_release_page_links()
    newest_release_link = get_newest_release_link(links)
    newest_version_str = newest_release_link.split("/")[-2].lstrip("v")
    log.info(f"Newest version: {newest_version_str}")
    newest_version = semver.Version.parse(newest_version_str)
    current_version = semver.Version.parse(get_actionlint_version())
    if newest_version.compare(current_version) != 1:
        log.info("Local version is newest, all good. Exiting.")
        write_github_output(newest_version, newest_version_str, is_update_required=False)
        exit(0)
    checksum_file_content = get_checksum_file(newest_release_link)
    update_config(checksum_file_content, str(current_version), newest_version_str)
    update_actionlint_version(newest_version_str)
    update_readme(str(current_version), newest_version_str)
    log.info("Local file 'checksums.cfg' and 'VERSION_ACTIONLINT.txt' and 'README.md' updated successfully. ")
    log.warning("A new commit is required.")
    write_github_output(newest_version, newest_version_str, is_update_required=True)


if __name__ == "__main__":
    main()
