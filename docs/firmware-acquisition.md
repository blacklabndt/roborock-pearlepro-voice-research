# S5V firmware acquisition check

Checked 2026-10-26 using an existing owner-authenticated session. No update was triggered and no robot settings were changed.

The read-only firmware-information operation implemented by python-roborock 7.13.0 requests the official device-specific OTA metadata endpoint. The response contained exactly these result keys: `currentVersion`, `desc`, `forceUpdate`, `releaseTime`, `updatable`, `version`.

- Installed/current version: `02.16.64`
- Offered version: `02.16.64`
- Updatable: false
- Forced update: false
- Download links in the response: none

This establishes that the account's normal firmware-information response did not provide a downloadable package at the time checked. It does not prove that Roborock has no package elsewhere, nor that a different firmware rollout would return identical metadata.

No supported export operation for the installed filesystem/firmware was identified in the inspected local library or public documentation search. No firmware image was acquired. An official OTA package, if independently obtained, must not be described as a full device backup: it may omit device-specific data or contain encrypted or differential content.

Reference: [python-roborock firmware-information API documentation](https://python-roborock.github.io/python-roborock/roborock/web_api.html). The library documents querying firmware information separately from the state-changing operation that starts an update; only the information query was used here.

## Passive app-log follow-up

A repeated owner-authenticated metadata check on the same day again returned current/offered version `02.16.64`, `updatable=false`, and no download URL. Two bounded Android logcat captures restricted to the Roborock app process contained no HTTP(S) URLs or firmware/OTA keyword matches. The captures were sparse (six and two lines), so this is not evidence that the app never logs download information.

Opening Firmware Updates through ADB taps could not be verified: screenshots remained on Settings, and Android UI automation returned a null root node. Manual navigation was requested. Consequently, these captures must not be described as a verified app update-check trace or interception of a firmware download. No installation was initiated, no encrypted traffic was decrypted, and no firmware package was acquired. Raw logs, screenshots, and account/device identifiers are excluded from this repository.
