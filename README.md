# PyCatSearch-Qt

A Qt-based GUI for [PyCatSearch](https://github.com/stsav012/pycatsearch) [![PyPI - Version](https://img.shields.io/pypi/v/pycatsearch)](https://pypi.org/project/pycatsearch).

## Requirements

The code is developed under the most recent Python to date. Older versions of Python should be compatible
as long as [`ruff`](https://docs.astral.sh/ruff/) makes no mistakes.
Currently, it's tuned for ![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fgithub.com%2FStSav012%2Fpycatsearch_qt%2Fraw%2Frefs%2Fheads%2Fmaster%2Fpyproject.toml).

It might work under `Python 3.8` but is uninstallable there bue to changes in `setuptools`.
Still, you can get the source files and try them under `Python 3.8`.

In case of a difficulty in the development, the support might shrink, but not further than what
[![SPEC 0 — Minimum Supported Dependencies](https://img.shields.io/badge/SPEC-0-green?labelColor=%23004811&color=%235CA038)](https://scientific-python.org/specs/spec-0000/)
proclaims.

The GUI requires Python bindings for Qt (`PyQt5`, `PySide6`, `PyQt6`, or `PySide2`), picked by `QtPy`.

## Installation

The package is available from the PyPI repo [![PyPI - Version](https://img.shields.io/pypi/v/pycatsearch_qt)](https://pypi.org/project/pycatsearch_qt):

```commandline
python3 -m pip install pycatsearch-qt
```

One may provide a Qt binding beforehand manually installing
- `PySide6-Essentials` [![PyPI - `PySide6` Version](https://img.shields.io/pypi/v/PySide6-Essentials)](https://pypi.org/project/PySide6-Essentials),
- `PyQt6` [![PyPI - `PyQt6` Version](https://img.shields.io/pypi/v/PyQt6)](https://pypi.org/project/PyQt6),
- `PyQt5` [![PyPI - `PyQt5` Version](https://img.shields.io/pypi/v/PyQt5)](https://pypi.org/project/PyQt5), or
- `PySide2` [![PyPI - `PySide2` Version](https://img.shields.io/pypi/v/PySide2)](https://pypi.org/project/PySide2).

Otherwise, one of them will be installed automatically.
Currently, it is unavoidable.
