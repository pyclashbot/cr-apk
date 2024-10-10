"""Webhook module."""

from __future__ import annotations

import os

import dotenv
import requests

dotenv.load_dotenv()

TIMEOUT = 10
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/...")


def send_webhook_message(title: str, description: str | None = None, url: str | None = None) -> None:
    """Send a webhook message to Discord.

    Args:
        title (str): The title of the message.
        description (str | None): The description of the message.
        url (str | None): The URL to include in the message.

    """
    payload = {
        "embeds": [
            {
                "title": title,
                "description": description,
                "url": url,
            },
        ],
    }

    response = requests.post(WEBHOOK_URL, json=payload, timeout=TIMEOUT)

    response.raise_for_status()
