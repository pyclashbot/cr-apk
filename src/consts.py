"""Constants for the project."""

import pathlib

WORKING_DIRECTORY = pathlib.Path().cwd()
OUTPUT_DIRECTORY = WORKING_DIRECTORY / "out"
VERSIONS_DIRECTORY = WORKING_DIRECTORY / "versions"

OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
VERSIONS_DIRECTORY.mkdir(parents=True, exist_ok=True)

ASSETS_DIRECTORY = WORKING_DIRECTORY / "assets"

BASE_APK_NAME = "com.supercell.clashroyale"
OUTPUT_BASE_NAME = "PYCB_CR"

DEPLOY_TARGET_DIRECTORY = "apks"
