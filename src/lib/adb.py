"""ADB related functions."""

from __future__ import annotations

import logging
import pathlib

from pymemuc import PyMemuc

from src.consts import VERSIONS_DIRECTORY
from src.lib.subprocess import run

ADB_PATH: str = (pathlib.Path(PyMemuc._get_memu_top_level()) / "adb.exe").absolute().as_posix()  # noqa: SLF001


def pull_apks(version: str, package: str, adb_path: str | None = None) -> None:
    """Pull APKs from the device."""
    if adb_path is None:
        adb_path = ADB_PATH
    logging.debug("Using ADB at: %s", adb_path)

    logging.debug("Listing packages")
    list_packages_result = run([adb_path, "shell", "pm", "list", "packages", "-f", package])

    if list_packages_result[0] != 0:
        error_message = f"Failed to list packages: {list_packages_result[2]}"
        raise ValueError(error_message)
    logging.debug("Packages listed successfully")

    # get paths to apks:
    logging.debug("Getting package paths")
    package_paths_result = run([adb_path, "shell", "pm", "path", package])

    if package_paths_result[0] != 0:
        error_message = f"Failed to get package paths: {package_paths_result[2]}"
        raise ValueError(error_message)

    package_paths = package_paths_result[1].splitlines()
    apk_paths = [path.split("package:")[1] for path in package_paths]
    logging.debug("Package paths retrieved successfully: %s", apk_paths)

    output_directory = VERSIONS_DIRECTORY / version
    output_directory.mkdir(parents=True, exist_ok=True)

    logging.debug("Pulling APKs to %s", output_directory)

    def pull_apk(target_path: pathlib.Path, apk_path: str) -> None:
        """Pull an APK from the device."""
        pull_result = run([adb_path, "pull", apk_path, target_path.absolute().as_posix()])
        logging.debug("\tPulling APK %s", apk_path)
        if pull_result[0] != 0:
            error_message = f"Failed to pull APK: {pull_result[2]}"
            raise ValueError(error_message)

    for apk_path in apk_paths:
        pull_apk(output_directory, apk_path)
    logging.debug("APKs pulled successfully")

    logging.debug("Renaming APKs")
    base_apk = output_directory / "base.apk"
    base_apk.rename(output_directory / f"{package}.apk")
    for apk in output_directory.glob("split_*.apk"):
        apk.rename(output_directory / apk.name[6:])
    logging.debug("APKs renamed successfully")
