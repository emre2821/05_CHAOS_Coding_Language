from importlib import resources
from importlib.abc import Traversable
from pathlib import Path
from typing import Optional


def resolve_packaged_script(script_path: Path) -> Optional[Traversable]:
    """
    Resolve a script path that lives inside the packaged ``chaos_corpus`` data.

    This returns an importlib.resources Traversable instead of materializing a
    temporary file on disk so it is safe when running from a zip/zipapp.
    """
    try:
        corpus_root = resources.files("chaos_corpus")
    except ModuleNotFoundError:
        return None

    relative_path = script_path
    if relative_path.parts and relative_path.parts[0] == "chaos_corpus":
        relative_path = Path(*relative_path.parts[1:])

    candidate = corpus_root.joinpath(relative_path)
    if candidate.is_file():
        return candidate
    return None
