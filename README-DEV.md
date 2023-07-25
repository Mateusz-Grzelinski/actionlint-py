# Workflows

Workflows take care of (todo update):

- checking for updates every day: [check-for-update.yml](.github/workflows/check-for-update.yml)
  and [auto_update_main.py](_custom_build/auto_update_main.py)
- tagging a git commit using only version in file: `_custom_build/VERSION_ACTIONLINT.txt`
  in [tag.yml](.github/workflows/tag.yml)
    - todo: it is not ideal that pip version and tag is different...
- making a test release using version on branch `release*`
  [build.yml](.github/workflows/build-dev.yml) and
  [release.yml](.github/workflows/upload.yml) and publishing it
  to https://test.pypi.org/project/actionlint-py/#history
    - test version is set to `python -m "_custom_build" --version` + `.devN` (development version is updated
      automatically when PR is created)
- making a public release using version _custom_build/VERSION_ACTIONLINT.txt
  [build.yml](.github/workflows/build-dev.yml) and
  [release.yml](.github/workflows/upload.yml) and publishing it
  to https://pypi.org/project/actionlint-py/
    - public version is set to `python -m "_custom_build" --version`
- after `release*` branch is merged development version is reset to 0
  [version-dev.yml](.github/workflows/version-dev-reset.yml)
- after `release*` branch is merged build system version is incremented
  [version-build-system.yml](.github/workflows/version-build-system.yml)
- todo: those workflow means I can not write protect main branch...

## Use actionlint from test mirror

```shell
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ actionlint-py==1.6.25.3.dev6
```

# Change actionlint version

All details about actionlint source (and checksums) are stored in [setup.cfg](setup.cfg).
The script [setup_auto_update.py](setup_auto_update.py) scraps the release page of actionlint and sets the checksums to
the newest release. It is not great quality script, but it works. Just run:

```shell
python auto_update_main.py
```

# Manual release

https://test.pypi.org/manage/project/actionlint-py/releases/

https://pypi.org/manage/project/actionlint-py/releases/

Install dependencies:

```shell
pip install --upgrade build twine
```

Build and check:

```shell
# python .\setup.py sdist bdist_wheel # deprecated
# python -c "from setuptools import setup; setup()" build # deprecated
python -m build
python -m twine check .\dist\*
```

If using token, create file `.pypirc`:

```
[pypi]
username = __token__
password = <PyPI token>
```

Provide file or insert creds when prompted:

```shell
python -m twine upload .\dist\* # --config-file .pypirc
```
