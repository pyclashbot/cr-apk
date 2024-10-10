"""Generate a manifest for an XAPK."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from src.consts import BASE_APK_NAME

if TYPE_CHECKING:
    import pathlib


DEFAULT_MANIFEST: dict[str, str | int | list[str] | list[dict[str, str]]] = {
    "xapk_version": 2,
    "package_name": "com.supercell.clashroyale",
    "name": "Clash Royale",
    "min_sdk_version": "24",
    "target_sdk_version": "34",
    "permissions": [
        "android.permission.INTERNET",
        "android.permission.ACCESS_NETWORK_STATE",
        "android.permission.WAKE_LOCK",
        "android.permission.CHANGE_WIFI_STATE",
        "android.permission.ACCESS_WIFI_STATE",
        "com.android.vending.BILLING",
        "android.permission.VIBRATE",
        "android.permission.POST_NOTIFICATIONS",
        "android.permission.READ_BASIC_PHONE_STATE",
        "android.Manifest.permission.ACCESS_NETWORK_STATE",
        "com.google.android.gms.permission.AD_ID",
        "com.google.android.c2dm.permission.RECEIVE",
        "com.google.android.finsky.permission.BIND_GET_INSTALL_REFERRER_SERVICE",
        "android.permission.ACCESS_ADSERVICES_ATTRIBUTION",
        "android.permission.ACCESS_ADSERVICES_AD_ID",
        "com.google.android.providers.gsf.permission.READ_GSERVICES",
        "android.permission.CAMERA",
        "com.supercell.clashroyale.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION",
    ],
}


def generate_manifest(version: str, apks: list[pathlib.Path], icon: str = "icon.png") -> str:
    """Generate a manifest for an XAPK."""
    base_apk = None
    for apk in apks:
        if apk.name.startswith(BASE_APK_NAME):
            base_apk = apk
            break
    if not base_apk:
        error_message = f"Base APK {BASE_APK_NAME} not found"
        raise ValueError(error_message)

    manifest = DEFAULT_MANIFEST.copy()
    manifest["version_code"] = version
    manifest["version_name"] = version

    # all apks minus the base apk
    split_configs = [apk for apk in apks if apk != base_apk]

    manifest["split_configs"] = [apk.name.replace(".apk", "") for apk in split_configs]

    # all apks and their id (just the apk witout extension)
    manifest["split_apks"] = [{"id": apk.name.replace(".apk", ""), "file": apk.name} for apk in apks]

    manifest["icon"] = icon

    return json.dumps(manifest, indent=4)
