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
environment (or `actionlint.exe` on windows).

### As a pre-commit hook

See [pre-commit] for instructions

Sample `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/Mateusz-Grzelinski/actionlint-py
  rev: v1.6.25
  hooks:
    - id: actionlint
```

or to avoid going twice to internet (might help with proxy):

```yaml
- repo: local
  hooks:
    - id: actionlint
      name: actionlint
      description: Test yaml scripts with actionlint
      #      additional_dependencies: [actionlint-py==1.6.22.2] # safer, but pre-commit autoupdate will not work
      additional_dependencies: [ actionlint-py ]
      entry: actionlint
      #      args: [-ignore "*.set-output. was depracated.*"]
      language: python
      types: [ "yaml" ]
      files: "^.github/workflows/"
```

[actionlint]: https://github.com/rhysd/actionlint

[pre-commit]: https://pre-commit.com

# Development

Development of wrapper and releasing new version: see [README-DEV.md](./README-DEV.md)

# Roadmap

- [ ] Update tag in readme in github action when releasing new version
- [ ] Upload also binary distribution, not only source distribution
- [ ] Add unit tests to build system

Won't do unless asked:

- support all platforms that actionlint supports (like freebsd)
