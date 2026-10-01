import itertools
import sys
from collections.abc import Iterable
from contextlib import suppress
from logging import Logger, getLogger
from typing import Any, Protocol, TypeGuard

from pycatsearch.utils import NAME, STOICHIOMETRIC_FORMULA, STRUCTURAL_FORMULA, CatalogEntryType
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QStyle, QWidget

from ._html import a_tag, chem_html, is_good_html, p_tag, remove_html, tag, tex_to_html_entity, wrap_in_html
from ._ods import html_to_ods, ods_object_descriptor
from ._rtf import html_to_rtf

__all__ = [
    "ReleaseInfo",
    "a_tag",
    "best_name",
    "chem_html",
    "html_to_ods",
    "html_to_rtf",
    "icon",
    "latest_release",
    "ods_object_descriptor",
    "p_tag",
    "remove_html",
    "tag",
    "update_with_pip",
    "with_logger",
    "wrap_in_html",
]


def best_name(entry: CatalogEntryType, allow_html: bool = True) -> str:
    species_tag: int = entry.speciestag
    last: str = best_name.__dict__.get("last", {}).get(species_tag, {}).get(allow_html, "")
    if last:
        return last

    def _best_name() -> str:
        if isotopolog := entry.isotopolog:
            if allow_html:
                if is_good_html(str(molecule_symbol := entry.moleculesymbol)) and (
                    entry.structuralformula == isotopolog or entry.stoichiometricformula == isotopolog
                ):
                    if state_html := entry.state_html:
                        # span tags are needed when the molecule symbol is malformed
                        return f"<span>{molecule_symbol}</span>, {chem_html(tex_to_html_entity(str(state_html)))}"
                    return str(molecule_symbol)
                if state_html := entry.state_html:
                    return f"{chem_html(str(isotopolog))}, {chem_html(tex_to_html_entity(str(state_html)))}"
                return chem_html(str(isotopolog))
            if state_html := entry.state_html:
                return f"{isotopolog}, {remove_html(tex_to_html_entity(state_html))}"
            if state := entry.state:
                return f"{isotopolog}, {remove_html(tex_to_html_entity(state.strip('$')))}"
            return isotopolog

        for key in (NAME, STRUCTURAL_FORMULA, STOICHIOMETRIC_FORMULA):
            if candidate := getattr(entry, key, ""):
                return chem_html(str(candidate)) if allow_html else str(candidate)
        if trivial_name := entry.trivialname:
            return str(trivial_name)
        if species_tag:
            return str(species_tag)
        return "no name"

    res: str = _best_name()
    if not species_tag:
        return res
    if "last" not in best_name.__dict__:
        best_name.__dict__["last"] = {}
    if species_tag not in best_name.__dict__["last"]:
        best_name.__dict__["last"][species_tag] = {}
    best_name.__dict__["last"][species_tag][allow_html] = res
    return res


class ReleaseInfo:
    def __init__(self, version: str = "", pub_date: str = "") -> None:
        self.version: str = version
        self.pub_date: str = pub_date

    def __bool__(self) -> bool:
        return bool(self.version) and bool(self.pub_date)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, (str, ReleaseInfo)):
            raise TypeError("The argument must be a string or ReleaseInfo")
        if isinstance(other, str):
            other = ReleaseInfo(version=other)
        i: str
        j: str
        for i, j in itertools.zip_longest(
            self.version.replace("-", ".").split("."), other.version.replace("-", ".").split("."), fillvalue=""
        ):
            if i == j:
                continue
            if i.isdigit() and j.isdigit():
                return int(i) < int(j)
            i_digits: str = "".join(itertools.takewhile(str.isdigit, i))
            j_digits: str = "".join(itertools.takewhile(str.isdigit, j))
            if i_digits != j_digits:
                if i_digits and j_digits:
                    return int(i_digits) < int(j_digits)
                return i_digits < j_digits
            return i < j
        return False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (str, ReleaseInfo)):
            raise TypeError("The argument must be a string or ReleaseInfo")
        if isinstance(other, str):
            other = ReleaseInfo(version=other)
        return self.version == other.version


def latest_release() -> ReleaseInfo:
    import urllib.request
    import xml.dom.minidom as dom
    from http.client import HTTPResponse
    from urllib.error import URLError
    from xml.dom.minicompat import NodeList

    from .. import __original_name__

    try:
        r: HTTPResponse = urllib.request.urlopen(
            f"https://pypi.org/rss/project/{__original_name__}/releases.xml", timeout=1
        )
    except URLError:
        return ReleaseInfo()
    if r.status != 200 or not r.readable():
        return ReleaseInfo()
    rss: dom.Node | None = dom.parseString(r.read().decode(encoding="ascii")).documentElement
    if not isinstance(rss, dom.Element) or rss.tagName != "rss":
        return ReleaseInfo()
    channels: NodeList = rss.getElementsByTagName("channel")
    if not channels or channels[0].nodeType != dom.Node.ELEMENT_NODE:
        return ReleaseInfo()
    channel: dom.Element = channels[0]
    items: NodeList = channel.getElementsByTagName("item")
    if not items or items[0].nodeType != dom.Node.ELEMENT_NODE:
        return ReleaseInfo()
    item: dom.Element = items[0]
    titles: NodeList = item.getElementsByTagName("title")
    if not titles or titles[0].nodeType != dom.Node.ELEMENT_NODE:
        return ReleaseInfo()
    title: dom.Element = titles[0]
    pub_dates: NodeList = item.getElementsByTagName("pubDate")
    if not pub_dates or pub_dates[0].nodeType != dom.Node.ELEMENT_NODE:
        return ReleaseInfo()
    pub_date: dom.Element = pub_dates[0]
    title_value: dom.Node | None = title.firstChild
    pub_date_value: dom.Node | None = pub_date.firstChild
    if not isinstance(title_value, dom.Text) or not isinstance(pub_date_value, dom.Text):
        return ReleaseInfo()

    return ReleaseInfo(title_value.data, pub_date_value.data)


def update_with_pip() -> None:
    import subprocess
    import sys
    from importlib.util import find_spec

    from .. import __original_name__

    if find_spec("pip") is None:
        subprocess.Popen(
            args=[
                sys.executable,
                "-c",
                f"""import sys, subprocess as s, time; time.sleep(2); m = [sys.executable, '-m'];\
            s.run(args=[*m, 'ensurepip']);\
            s.run(args=[*m, 'pip', 'install', '-U', {__original_name__!r}]);\
            s.Popen(args=[*m, {__original_name__!r}])""",
            ]
        )
    else:
        subprocess.Popen(
            args=[
                sys.executable,
                "-c",
                f"""import sys, subprocess as s, time; time.sleep(2); m = [sys.executable, '-m'];\
            s.run(args=[*m, 'pip', 'install', '-U', {__original_name__!r}]);\
            s.Popen(args=[*m, {__original_name__!r}])""",
            ]
        )
    sys.exit(0)


if sys.version_info < (3, 10, 0):  # noqa: UP036
    import builtins

    # noinspection PyShadowingBuiltins
    def zip(*iterables: Iterable[Any], strict: bool = False) -> builtins.zip:
        """Intentionally override `builtins.zip` to ignore the `strict` parameter in Python < 3.10."""
        return builtins.zip(*iterables)  # noqa: B905

    __all__.append("zip")


# noinspection PyPackageRequirements,PyUnresolvedReferences
def icon(
    self: QWidget,
    theme_name: str,
    *qta_name: str,
    standard_pixmap: QStyle.StandardPixmap | None = None,
    **qta_specs: object,
) -> QIcon:
    if theme_name and QIcon.hasThemeIcon(theme_name):
        return QIcon.fromTheme(theme_name)

    if qta_name:
        with suppress(ImportError, Exception):
            import qtawesome as qta

            return qta.icon(*qta_name, **qta_specs)  # might raise an `Exception` if the icon is not in the font

    if standard_pixmap is not None:
        return self.style().standardIcon(standard_pixmap)

    return QIcon()


class HasLogger(Protocol):
    logger: Logger
    __call__ = ...


def has_logger(cls: type) -> TypeGuard[HasLogger]:
    return hasattr(cls, "logger")


def with_logger(cls: type) -> HasLogger:
    # noinspection PyUnresolvedReferences
    cls.logger = getLogger(cls.__name__)
    if has_logger(cls):
        return cls
    raise RuntimeError
