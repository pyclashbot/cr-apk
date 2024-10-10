"""Build command."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.io.inputs.argument import Argument

from src.lib.apk import build_xapk, get_versions

if TYPE_CHECKING:
    from cleo.io.inputs.argument import Argument


class BuildCommand(Command):
    """Builds an APK version."""

    name = "build"
    description = "Builds an APK version"

    arguments: list[Argument] = [  # noqa: RUF012
        argument(
            "version",
            description="Version to build. If not provided, the latest version will be build.",
            optional=True,
        ),
        argument("icon", description="Icon to use for the APK", optional=True, default="icon.png"),
    ]

    def handle(self) -> None:
        """Handle the command."""
        self.line("<comment>Building APK...</comment>")
        version: str = self.argument("version")

        versions = [version.name for version in get_versions()]

        if version and version not in versions:
            error_message = f"Version {version} not found"
            raise ValueError(error_message)

        if not version:
            version = max(versions)
            logging.debug("No version provided, using latest version: %s", version)

        self.line(f"<info>Building version {version}</info>")
        build_xapk(version, self.argument("icon"))
        self.line("<info>APK built.</info>")
