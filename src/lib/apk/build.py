"""Build an XAPK."""

from __future__ import annotations

import logging
import pathlib
import zipfile

from src.consts import ASSETS_DIRECTORY, OUTPUT_BASE_NAME, OUTPUT_DIRECTORY
from src.lib.apk.manifest import generate_manifest
from src.lib.apk.versions import get_versions


def build_xapk(version: str, icon: str = "icon.png") -> None:
    """Build an XAPK."""
    versions = get_versions()

    version_dir = None
    for version_dir in versions:
        if version_dir.name == version:
            break
    if not version_dir:
        error_message = f"Version {version} not found"
        logging.error(error_message)
        raise ValueError(error_message)

    apks = [apk for apk in version_dir.iterdir() if apk.suffix == ".apk"]
    logging.debug("APKs found: %s", apks)
    manifest = generate_manifest(version, apks, icon)
    logging.debug("Manifest generated: %s", manifest)

    # zip up the apks and manifest to create the xapk in OUTPUT_DIRECTORY
    xapk_name = f"{OUTPUT_BASE_NAME}_{version}.xapk"
    xapk_path = pathlib.Path(OUTPUT_DIRECTORY) / xapk_name

    with zipfile.ZipFile(xapk_path, "w") as xapk:
        for apk in apks:
            xapk.write(apk, apk.name)
            logging.debug("APK added to XAPK: %s", apk)
        xapk.writestr("manifest.json", manifest)
        logging.debug("Manifest added to XAPK: %s", manifest)
        for asset in pathlib.Path(ASSETS_DIRECTORY).iterdir():
            xapk.write(asset, asset.name)
            logging.debug("Asset added to XAPK: %s", asset)

    logging.debug("XAPK built: %s", xapk_path)


def get_apks() -> list[pathlib.Path]:
    """Get all build APK paths."""
    return list(pathlib.Path(OUTPUT_DIRECTORY).iterdir())
