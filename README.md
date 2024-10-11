# cr-apk

Clash Royale APK Manager

## Usage

Installation:

```bash
poetry install
```

Pull APKs from device:

```bash
poetry run cr-apk pull <version> [<package>] [--adb=<adb executable>]
```

List pulled and built APKs:

```bash
poetry run cr-apk ls
```

Build APK:

```bash
poetry run cr-apk build [<version> [<icon>]]
```

Deploy APK:

```bash
poetry run cr-apk deploy [<version>]
```
