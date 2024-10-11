"""Deploy command."""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

import dotenv
from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option

from src.consts import DEPLOY_TARGET_DIRECTORY, OUTPUT_BASE_NAME, OUTPUT_DIRECTORY
from src.lib.apk import get_apks
from src.lib.aws import upload_file_to_s3
from src.lib.webhook import send_webhook_message

if TYPE_CHECKING:
    from cleo.io.inputs.argument import Argument

dotenv.load_dotenv()


class DeployCommand(Command):
    """Deploys an APK version."""

    name = "deploy"
    description = "Deploys an APK version"

    arguments: list[Argument] = [  # noqa: RUF012
        argument(
            "version",
            description="Version to deploy. If not provided, the latest version will be deployed.",
            optional=True,
        ),
    ]

    options = [Option("notify", "N", description="Send webhook notification when done deploying", flag=True)]  # noqa: RUF012

    def handle(self) -> None:
        """Handle the command."""
        self.line("<comment>Deploying APK...</comment>")
        version: str = self.argument("version")

        apks: list[str] = [apk.name for apk in get_apks()]
        versions = [apk.split("_")[-1].split(".")[0] for apk in apks]

        if version and version not in versions:
            error_message = f"Version {version} not found"
            raise ValueError(error_message)

        if not version:
            version = max(versions)
            logging.debug("No version provided, using latest version: %s", version)

        self.line(f"<info>Deploying version {version}</info>")

        xapk_name = f"{OUTPUT_BASE_NAME}_{version}.xapk"
        xapk_path = OUTPUT_DIRECTORY / xapk_name

        logging.debug("Uploading XAPK: %s to S3 bucket", xapk_path)
        upload_file_to_s3(xapk_path, target_dir=DEPLOY_TARGET_DIRECTORY)
        self.line("<info>APK deployed.</info>")

        if self.option("notify"):
            self.line("<info>Notifying users...</info>")
            dist_url = os.environ.get("DIST_URL", "") + "/" + xapk_name
            send_webhook_message(f"APK version {version} has been released.", "Download here", url=dist_url)
            self.line("<info>Users notified.</info>")
