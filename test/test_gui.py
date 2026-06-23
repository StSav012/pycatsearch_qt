#!/usr/bin/env python3
from pathlib import Path
from types import ModuleType


def _third_party_modules() -> list[str]:
    import site
    import sys

    prefixes: list[str] = site.getsitepackages([sys.exec_prefix, sys.prefix])
    third_party_modules: list[str] = []
    modules: list[tuple[str, ModuleType, list[Path]]] = [
        (module_name, module, [Path(p).resolve() for p in getattr(module, "__path__", [])])
        for module_name, module in sys.modules.items()
    ]
    for module_name, module, paths in modules:
        if (
            "." not in module_name
            and module_name != "_distutils_hack"
            and paths
            and getattr(module, "__package__", "")
            # instead of `prefix in p.parents`, it should be `is_relative_to`, but it appeared only in Python 3.9
            and any(prefix in p.parents for p in paths for prefix in prefixes)
            and not any(
                another_path in p.parents
                for p in paths
                for another_module_name, _, other_paths in modules
                if another_module_name != module_name
                for another_path in other_paths
            )
        ):
            third_party_modules.append(module_name)

    return third_party_modules


def test_gui() -> None:
    third_party_modules: list[str]

    third_party_modules = _third_party_modules()
    assert third_party_modules == [], third_party_modules

    from pycatsearch_qt import main  # noqa: F401

    expected_third_party_modules: list[str] = [
        "PyQt5",
        "PyQt6",
        "PySide2",
        "PySide6",
        "aiohttp",
        "aiosignal",
        "attr",
        "frozenlist",
        "idna",
        "multidict",
        "orjson",
        "packaging",
        "qtawesome",
        "qtpy",
        "shiboken2",
        "shiboken6",
        "yarl",
    ]
    third_party_modules = _third_party_modules()
    assert third_party_modules
    assert set(third_party_modules).issubset(expected_third_party_modules), third_party_modules


if __name__ == "__main__":
    import sys
    from os import path

    sys.path = list(set(sys.path) | {path.abspath(path.join(__file__, path.pardir, path.pardir))})

    test_gui()
