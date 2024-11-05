> Note: for `pre-commit` hooks I recommend officially supported hooks:
> See docs: https://github.com/rhysd/actionlint/blob/main/docs/usage.md#pre-commit

# actionlint-py

A python wrapper to provide a pip-installable [actionlint] binary.

Internally this package provides a convenient way to download the pre-built
actionlint binary for your particular platform.

### Installation

```bash
pip install actionlint-py
```

### Usage

After installation, the `actionlint` binary should be available in your
environment (or `actionlint.exe` on windows). Remember to add you `Scripts` folder to `PATH`.

### As a pre-commit hook

See [pre-commit] for introduction.

**I recommend using officially supported pre-commit hooks from actionlint itself**
See docs: https://github.com/rhysd/actionlint/blob/main/docs/usage.md#pre-commit

Use this repo if you can not use officially supported hooks (docker, golang, system) and you are fine with python `pip` wrapper.

Sample `.pre-commit-config.yaml` using `pip` as package manager:

```yaml
- repo: https://github.com/Mateusz-Grzelinski/actionlint-py
  rev: v1.7.4.18
  hooks:
    - id: actionlint
      additional_dependencies: [ pyflakes>=3.0.1, shellcheck-py>=0.9.0.5 ]
      # actionlint has built in support for pyflakes and shellcheck, sadly they will not be auto updated. Check https://pypi.org/project/actionlint-py/ for latest version. Alternatively:
      # args: [-shellcheck=/path/shellcheck -pyflakes=/path/pyflakes]
      # note - invalid path in arguments will fail silently
```

Because `actionlint-py` is available as source distribution, pip build system will fetch binary from (public)
github. It might cause problems with corporate proxy. In case of problems try this semi-manual setup that respects
your `pip.ini`:

```yaml
- repo: local
  hooks:
    - id: actionlint
      name: actionlint
      description: Lint GitHub workflows with actionlint
      additional_dependencies: [ actionlint-py ]
      #additional_dependencies: [actionlint-py==1.7.4.18]
      # safer, but pre-commit autoupdate will not work
      # note: the pip versioning scheme is different from actionlint binary: not "v1.7.4" but "1.7.4.18" (last number is build system version)
      entry: actionlint
      #args: [-ignore "*.set-output. was depracated.*"]
      language: python
      types: [ "yaml" ]
      files: "^.github/workflows/"
```

[actionlint]: https://github.com/rhysd/actionlint

[pre-commit]: https://pre-commit.com

## Alternative methods of running actionlint

### As pre-commit hooks

See [official docs for pre-commit integration](https://github.com/rhysd/actionlint/blob/main/docs/usage.md#pre-commit)

```yaml
- repo: https://github.com/rhysd/actionlint
  rev: v1.7.4
  hooks:
    - id: actionlint
    # - id: actionlint-docker
    # - id: actionlint-system
```

### Use as github action step

Use directly in github action, see
[official docs for github action integration](https://github.com/rhysd/actionlint/blob/main/docs/usage.md#use-actionlint-on-github-actions):

```yaml
name: Lint GitHub Actions workflows
on: [ push, pull_request ]

jobs:
  actionlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Download actionlint
        id: get_actionlint
        run: bash <(curl https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)
        shell: bash
      - name: Check workflow files
        run: ${{ steps.get_actionlint.outputs.executable }} -color
        shell: bash
```

Or using docker:

```yaml
name: Lint GitHub Actions workflows
on: [ push, pull_request ]

jobs:
  actionlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check workflow files
        uses: docker://rhysd/actionlint:latest
        with:
          args: -color
```

# Development

Development of wrapper and releasing new version:
see [README-DEV.md](https://github.com/Mateusz-Grzelinski/actionlint-py/blob/main/README-DEV.md)

# Roadmap

- [x] Add actionlint hook as docker
    - [x] support `shellcheck-py` in docker image
    - [ ] auto update docker version in `.pre-commit-hooks.yaml` when using `_custom_build/auto_update_main.py`
- [x] add `shellcheck-py` as dependency (or at least document)
- [x] Update tag in readme in github action when releasing new version
- [ ] Upload also binary distribution, not only source distribution
- [ ] Add unit tests to build system

See [README-DEV.md](https://github.com/Mateusz-Grzelinski/actionlint-py/blob/main/README-DEV.md) for more TODOs.

Won't do unless asked:

- support all platforms that actionlint supports (like freebsd)
