"""Constants for the project."""

import pathlib

SCRIPT_DIRECTORY = pathlib.Path(__file__).parent
OUTPUT_DIRECTORY = SCRIPT_DIRECTORY.parent / "out"
VERSIONS_DIRECTORY = SCRIPT_DIRECTORY.parent / "versions"

OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
VERSIONS_DIRECTORY.mkdir(parents=True, exist_ok=True)

ASSETS_DIRECTORY = SCRIPT_DIRECTORY.parent / "assets"

BASE_APK_NAME = "com.supercell.clashroyale"
OUTPUT_BASE_NAME = "PYCB_CR"

DEPLOY_TARGET_DIRECTORY = "apks"
