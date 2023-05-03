
```shell
pip install --upgrade build twine
# python -m build --no-isolation
python .\setup.py sdist bdist_wheel
python -m twine check .\dist\*
python -m twine upload .\dist\*
```
