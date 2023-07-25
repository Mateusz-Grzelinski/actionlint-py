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
  rev: v1.6.25.5
  hooks:
    - id: actionlint
```

Because `actionlint-py` is available as source distribution, pip build system is set up to fetch binary from (public)
github. It might cause problems with corporate proxy. In case of problems try this semi-manual setup:

```yaml
- repo: local
  hooks:
    - id: actionlint
      name: actionlint
      description: Lint GitHub workflows with actionlint
      additional_dependencies: [ actionlint-py ]
      #additional_dependencies: [actionlint-py==1.6.25.5]
      # safer, but pre-commit autoupdate will not work
      # note: the versioning scheme is different: not "v1.6.25" but "1.6.25.2" (last number is build system version)
      entry: actionlint
      #args: [-ignore "*.set-output. was depracated.*"]
      language: python
      types: [ "yaml" ]
      files: "^.github/workflows/"
```

[actionlint]: https://github.com/rhysd/actionlint

[pre-commit]: https://pre-commit.com

# Development

Development of wrapper and releasing new version:
see [README-DEV.md](https://github.com/Mateusz-Grzelinski/actionlint-py/blob/main/README-DEV.md)

# Roadmap

- [ ] Update tag in readme in github action when releasing new version
- [ ] Upload also binary distribution, not only source distribution
- [ ] Add unit tests to build system

See [README-DEV.md](https://github.com/Mateusz-Grzelinski/actionlint-py/blob/main/README-DEV.md) for more TODOs.

Won't do unless asked:

- support all platforms that actionlint supports (like freebsd)
