from pathlib import Path


def read_text_file(file_path: Path) -> str:
    """
    Read text-based files and return their content as a string.

    Supported for now:
    - .txt
    - .md
    - .py
    - .js
    - .csv
    """

    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return file_path.read_text(encoding="latin-1")