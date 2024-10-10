"""List command."""

from cleo.commands.command import Command

from src.lib.apk import get_versions


class ListCommand(Command):
    """Lists all APK versions."""

    name = "list"
    description = "Lists all APK versions"

    def handle(self) -> None:
        """Handle the command."""
        self.line("<comment>Available APK versions:</comment>")
        versions = get_versions()

        # print the versions in chunks of 5
        versions_list = [version.name for version in versions]
        for i in range(0, len(versions_list), 5):
            versions_chunk = versions_list[i : i + 5]
            versions_string = ", ".join(versions_chunk)
            self.line(f"<info>{versions_string}</info>")
