# scanner.py
from pathlib import Path
from typing import Iterable, List, Union

from .config import SUPPORTED_EXTENSIONS

PathLike = Union[str, Path]
InputType = Union[PathLike, Iterable[PathLike]]


def collect_parsable_files(inputs: InputType) -> List[str]:
    """
    Collect all parsable document files from:
    - a directory
    - a file
    - or a list of directories / files

    Returns:
        List[str]: absolute paths of parsable documents
    """
    if not isinstance(inputs, (list, tuple, set)):
        inputs = [
            inputs,
        ]

    collected: List[str] = []

    for item in inputs:
        path = Path(item).expanduser().resolve()

        if not path.exists():
            continue

        if path.is_file():
            if _is_parsable_file(path):
                collected.append(str(path))
            continue

        if path.is_dir():
            for p in path.rglob("*"):
                if _is_parsable_file(p):
                    collected.append(str(p))

    return sorted(set(collected))


def _is_parsable_file(p: Path) -> bool:
    return (
        p.is_file()
        and p.suffix.lower() in SUPPORTED_EXTENSIONS
        and not p.name.startswith("~$")
    )
