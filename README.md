# cr-apk

Clash Royale APK Manager

## Installation

```bash
pipx install cr-apk
```

## Usage

List available commands:

```bash
crapk list
# Available commands:
#   build   Builds an APK version
#   deploy  Deploys an APK version
#   help    Displays help for a command.
#   list    Lists commands.
#   ls      Lists all APK versions
#   pull    Pulls an installed application's APKs from the device
```

### Example

```bash
crapk pull 80256022 # target version
# Pulling APKs for package com.supercell.clashroyale as version 80256022
# APKs pulled.
crapk build
# Building APK...
# Building version 80256022
# APK built.
crapk ls
# Pulled versions:
# 80256022
#
# Built versions:
# 80256022
crapk deploy
# Deploying APK...
# Deploying version 80256022
# APK deployed.
```
