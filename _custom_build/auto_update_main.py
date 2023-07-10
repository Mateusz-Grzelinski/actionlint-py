from __future__ import annotations

import configparser
import logging
import os
from dataclasses import dataclass
from typing import Iterable

import requests
import semver
from requests_html import HTMLSession

VERSION = os.path.join(os.path.dirname(__file__), "VERSION.txt")

ACTIONLINT_RELEASES = "https://github.com/rhysd/actionlint/releases/"
SETUP_CFG = os.path.join(os.path.dirname(__file__), "./setup.cfg")
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


def update_config(checksum_file_content: str, newest_version_str: str) -> None:
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
    checksums: dict[str, ChecksumInfo] = {
        c.filename: c for c in get_checksums(checksum_file_content, config)
    }
    for sec in config.sections():
        platform_config = config[sec]
        file_name = platform_config["file_name"]
        url = (
            f"https://github.com/rhysd/actionlint/releases/download/"
            f"v{newest_version_str}/{file_name}"
        )
        platform_config["url"] = url
        platform_config["checksum"] = checksums[file_name].checksum

    with open(SETUP_CFG, "w") as file:
        config.write(file, space_around_delimiters=True)


def update_version(newest_version_str):
    with open(VERSION, "w") as file:
        file.write(newest_version_str)


@dataclass(frozen=True)
class ChecksumInfo:
    version: str
    filename: str
    postfix: str
    checksum: str


def get_checksums(checksum_file_content, config):
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


def get_version():
    with open(VERSION) as r:
        return r.read()


def main():
    links = get_release_page_links()
    newest_release_link = get_newest_release_link(links)
    newest_version_str = newest_release_link.split("/")[-2].lstrip("v")
    log.info(f"Newest version: {newest_version_str}")
    newest_version = semver.Version.parse(newest_version_str)
    current_version = semver.Version.parse(get_version())
    if newest_version.compare(current_version) != 1:
        log.info("Local version is newest, all good. Exiting.")
        with open(GITHUB_OUT, "a") as file:
            file.write(f"version={newest_version_str}\n")
            file.write(f"update_required=false\n")
        exit(0)
    checksum_file_content = get_checksum_file(newest_release_link)
    update_config(checksum_file_content, newest_version_str)
    update_version(newest_version_str)
    log.warning(
        "Local config updated. A new commit is required, ending with error.",
    )
    with open(GITHUB_OUT, "a") as file:
        file.write(f"version={newest_version_str}\n")
        file.write(f"update_required=true\n")
    exit(1)


if __name__ == "__main__":
    main()
