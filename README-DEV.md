# Change project configuration

All details about source package is stored in [setup.cfg](setup.cfg).
The script [setup_auto_update.py](setup_auto_update.py) scraps the release page of actionlint and sets the checksums to
the newest release. It is not great quality script, but it works. Just run:

```shell
python auto_update_main.py
```

Investigate changes in [setup.cfg](setup.cfg).

# Release

https://pypi.org/manage/project/actionlint-py/releases/

Install dependencies:

```shell
pip install --upgrade build twine
```

Can not remember what this does:

```shell
# python -m build --no-isolation
```

Build and check:

```shell
# python .\setup.py sdist bdist_wheel # deprecated
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
