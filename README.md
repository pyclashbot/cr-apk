# cr-apk

Clash Royale APK Manager

## Usage

Installation:

```bash
poetry install
```

Pull APKs from device:

```bash
poetry run cr-apk pull <version> [<package>]
```

List Available APKs to build:

```bash
poetry run cr-apk list
```

Build APK:

```bash
poetry run cr-apk build [<version> [<icon>]]
```
