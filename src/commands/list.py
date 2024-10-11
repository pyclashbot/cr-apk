"""List command."""

from __future__ import annotations

from cleo.commands.command import Command

from src.lib.apk import get_apks, get_versions

CHUNK_SIZE = 5


class ListCommand(Command):
    """Lists all APK versions."""

    name = "ls"
    description = "Lists all APK versions"

    def handle(self) -> None:
        """Handle the command."""
        pulled_versions = [version.name for version in get_versions()]
        built_versions = [apk.stem.split("_")[-1] for apk in get_apks()]

        pulled_versions.sort()
        built_versions.sort()

        def print_in_chunks(lst: list[str], chunk_size: int) -> None:
            for i in range(0, len(lst), chunk_size):
                chunk = lst[i : i + chunk_size]
                chunk_str = ", ".join(chunk)
                self.line(f"<info>{chunk_str}</info>")

        self.line("<comment>Pulled versions:</comment>")
        print_in_chunks(pulled_versions, CHUNK_SIZE)
        self.line("")

        self.line("<comment>Built versions:</comment>")
        print_in_chunks(built_versions, CHUNK_SIZE)
