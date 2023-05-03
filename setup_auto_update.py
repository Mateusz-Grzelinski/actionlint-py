from __future__ import annotations

import configparser
import re

import requests
import semver
from requests_html import HTMLSession

import setup

if __name__ == '__main__':
    session = HTMLSession()

    r = session.get('https://github.com/rhysd/actionlint/releases/')

    links = r.html.links

    newest_release_link = None
    for link in links:
        link: str
        # link.startswith("/rhysd/actionlint/releases/download/") and
        if link.endswith('_checksums.txt'):
            newest_release_link = link
            break
    print(newest_release_link)
    # '/rhysd/actionlint/releases/download/v1.6.24/actionlint_1.6.24_checksums.txt'
    newest_version_str = newest_release_link.split('/')[-2].lstrip('v')

    newest_version = semver.Version.parse(newest_version_str)
    current_version = semver.Version.parse(setup.ACTIONLINT_VERSION)
    if newest_version.compare(current_version) != 1:
        exit(0)

    checksums_file = requests.get('https://github.com' + newest_release_link)
    content = checksums_file.content.decode('utf-8')

    config = configparser.ConfigParser()
    config.read('./setup.cfg')
    files_to_download = config['files-to-download']
    files_to_download['tag'] = newest_version_str
    for line in content.split('\n'):
        if not line:
            continue
        checksum, file = line.split()
        file_ending = file.split('_')[-2:]
        file_ending = '_' + '_'.join(file_ending)
        files_to_download[file_ending] = checksum
    with open('./setup.cfg', 'w') as file:
        config.write(file, space_around_delimiters=True)

    checksum_file_name = newest_release_link.split('/')[-1]
