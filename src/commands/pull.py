"""Pull command."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cleo.commands.command import Command
from cleo.helpers import argument, option

from src.consts import BASE_APK_NAME
from src.lib.adb import pull_apks

if TYPE_CHECKING:
    from cleo.io.inputs.argument import Argument
    from cleo.io.inputs.option import Option


class PullCommand(Command):
    """Pulls an installed application's APKs from the device."""

    name = "pull"
    description = "Pulls an installed application's APKs from the device"

    arguments: list[Argument] = [  # noqa: RUF012
        argument(
            "version",
            description="The version to save the pulled APKs as",
        ),
        argument(
            "package",
            description="Package name of the application to pull APKs from",
            default=BASE_APK_NAME,
            optional=True,
        ),
    ]

    options: list[Option] = [  # noqa: RUF012
        option(
            "adb",
            description="Path to the ADB executable",
            flag=False,
        ),
    ]

    def handle(self) -> None:
        """Handle the command."""
        package = self.argument("package")
        version = self.argument("version")
        adb_path = self.option("adb")
        self.line(
            f"<info>Pulling APKs for package <comment>{package}</comment>"
            f" as version <comment>{version}</comment></info>",
        )
        pull_apks(version, package, adb_path)
        self.line("<info>APKs pulled.</info>")
