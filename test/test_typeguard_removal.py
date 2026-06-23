import re

for new, old in [
    ("def has_logger(cls: type) -> TypeGuard[HasLogger]:", "def has_logger(cls: type) -> bool:"),
    ("from typing import Any, Protocol, TypeGuard, cast", "from typing import Any, Protocol, cast"),
    ("from typing import Any, Protocol, TypeGuard", "from typing import Any, Protocol"),
    ("from typing import TypeGuard, cast", "from typing import cast"),
    ("from typing import TypeGuard", ""),
]:
    new = re.sub(r"from typing import TypeGuard$", "", new)
    new = re.sub(r"(from typing import) TypeGuard,(.*)", r"\1\2", new)
    new = re.sub(r"(from typing import\b.*?), TypeGuard\b(.*)", r"\1\2", new)
    new = re.sub(r"TypeGuard\[\w+](?=:)", "bool", new)
    assert new == old, f"{new!r} != {old!r}"
