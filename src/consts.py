"""Constants for the project."""

import pathlib

SCRIPT_DIRECTORY = pathlib.Path(__file__).parent
OUTPUT_DIRECTORY = SCRIPT_DIRECTORY.parent / "out"
VERSIONS_DIRECTORY = SCRIPT_DIRECTORY.parent / "versions"
ASSETS_DIRECTORY = SCRIPT_DIRECTORY.parent / "assets"

BASE_APK_NAME = "com.supercell.clashroyale"
