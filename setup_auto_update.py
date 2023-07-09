from __future__ import annotations

import configparser
import logging
from typing import Iterable

import requests
import semver
from requests_html import HTMLSession

import setup

ACTIONLINT_RELEASES = 'https://github.com/rhysd/actionlint/releases/'

SETUP_CFG = './setup.cfg'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def get_release_page_links():
    session = HTMLSession()
    r = session.get(ACTIONLINT_RELEASES)
    return r.html.links


def get_checksum_file(newest_release_link: str) -> str:
    checksums_file = requests.get('https://github.com' + newest_release_link)
    # checksum_file_name = newest_release_link.split('/')[-1]
    content = checksums_file.content.decode('utf-8')
    return content


def get_newest_release_link(links: Iterable[str]) -> str:
    newest_release_link = None
    for link in links:
        link: str
        # link.startswith("/rhysd/actionlint/releases/download/") and
        if link.endswith('_checksums.txt'):
            newest_release_link = link
            break
    return newest_release_link


def update_config(checksum_file_content: str, newest_version_str: str) -> None:
    """Update tag and checksum in config file"""
    config = configparser.ConfigParser()
    config.read(SETUP_CFG)
    files_to_download = config['files-to-download']
    files_to_download['tag'] = newest_version_str
    for line in checksum_file_content.split('\n'):
        if not line:
            continue
        checksum, file = line.split()
        file_ending = file.split('_')[-2:]
        file_ending = '_' + '_'.join(file_ending)
        files_to_download[file_ending] = checksum
    with open(SETUP_CFG, 'w') as file:
        config.write(file, space_around_delimiters=True)


def main():
    links = get_release_page_links()
    newest_release_link = get_newest_release_link(links)
    newest_version_str = newest_release_link.split('/')[-2].lstrip('v')
    log.info(f'Newest version: {newest_version_str}')
    newest_version = semver.Version.parse(newest_version_str)
    current_version = semver.Version.parse(setup.ACTIONLINT_VERSION)
    if newest_version.compare(current_version) != 1:
        log.info('Local version is newest, all good. Exiting.')
        exit(0)
    checksum_file_content = get_checksum_file(newest_release_link)
    update_config(checksum_file_content, newest_version_str)
    log.info('Local config updated.')


if __name__ == '__main__':
    main()
