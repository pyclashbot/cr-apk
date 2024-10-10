"""Module to handle APK versions available to build."""

from __future__ import annotations

import pathlib
from typing import Generator

from src.consts import VERSIONS_DIRECTORY


def get_versions() -> Generator[pathlib.Path, None, None]:
    """Get all APK versions available to build."""
    return pathlib.Path(VERSIONS_DIRECTORY).iterdir()
