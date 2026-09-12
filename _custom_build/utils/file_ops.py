import hashlib
import http
import http.client
import io
import os
import stat
import sys
import tarfile
import time
import urllib.error
import urllib.request
import zipfile


def download(url: str, sha256: str) -> bytes:
    attempts = 5
    backoff_sec = 2
    last_exc = None
    for attempt in range(attempts):
        try:
            return _download(url, sha256)
        except urllib.error.HTTPError as e:
            if not (500 <= e.code < 600):
                raise e  # any other than server error = panic
            last_exc = e
        except (
            urllib.error.URLError,
            http.client.HTTPException,
            TimeoutError,
            OSError,
        ) as e:
            last_exc = e

        if attempt == attempts - 1:
            break  # dont sleep when retries are exhausted

        sleep_time = min(backoff_sec, 30)
        print(f"Download retry {attempt}: sleep {sleep_time}: {url}")
        time.sleep(sleep_time)
        backoff_sec *= 2
    # attempts exhausted, panic
    if last_exc:
        raise RuntimeError(f"download failed for {url}") from last_exc
    else:
        raise RuntimeError(f"download failed for {url}")


def _download(url: str, sha256: str) -> bytes:
    with urllib.request.urlopen(url, timeout=30) as resp:
        code = resp.getcode()
        if code != http.HTTPStatus.OK:
            raise ValueError(f"HTTP failure. Code: {code}")
        data = resp.read()

    checksum = hashlib.sha256(data).hexdigest()
    if checksum != sha256:
        raise ValueError(f"sha256 mismatch, expected {sha256}, got {checksum}")

    return data


def extract(url: str, data: bytes) -> bytes:
    with io.BytesIO(data) as bio:
        if ".tar." in url:
            with tarfile.open(fileobj=bio) as tarf:
                for info in tarf.getmembers():
                    if info.isfile() and info.name.endswith("actionlint"):
                        return tarf.extractfile(info).read()
        elif url.endswith(".zip"):
            with zipfile.ZipFile(bio) as zipf:
                for info in zipf.infolist():
                    if info.filename.endswith(".exe"):
                        return zipf.read(info.filename)

    raise AssertionError(f"unreachable {url}")


def save_executable(data: bytes, base_dir: str):
    exe = "actionlint" if sys.platform != "win32" else "actionlint.exe"
    output_path = os.path.join(base_dir, exe)
    os.makedirs(base_dir, exist_ok=True)

    with open(output_path, "wb") as fp:
        fp.write(data)

    # Mark as executable.
    # https://stackoverflow.com/a/14105527
    mode = os.stat(output_path).st_mode
    mode |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    os.chmod(output_path, mode)
    return output_path
