# Administration-interface search

Checked 2026-10-26 for Qrevo S5V / `roborock.vacuum.a170`, firmware `02.16.64`.

## Observations

- Authenticated normal LAN control queries work, as recorded in [the voice-interface investigation](voice-message-interface.md).
- Requests to the device's HTTP and HTTPS root pages on standard ports 80 and 443 were refused. No login page or certificate was returned. This rules out a web page on those ports at that moment, not every possible interface.
- The inspected app menus do not expose filesystem browsing, recording upload or firmware export.
- The normal OTA metadata query returned version information but no package URL; see [firmware acquisition](firmware-acquisition.md).

## Independent documentation review

Claude Code independently searched public vendor and integration documentation, without device connections or private artifact access. It did not identify a documented S5V administration portal or firmware-export interface. This is a bounded negative search result, not proof that service-only tools or other interfaces do not exist.

The review contained Q-series/Qrevo conflation and uncertainty about Matter that should not be used as evidence: the owner's app visibly offered a Matter-network option. That option does not establish filesystem or firmware-export access. The older command reference used by the review is incomplete and is not an exhaustive description of the installed library or firmware.

## Closely matching public report

[Local Roborock Server issue 52](https://github.com/Python-roborock/local_roborock_server/issues/52) reports successful onboarding for the exact model `a170` and firmware `02.16.64`. It supports local control compatibility. It does not report a device-hosted administration portal, arbitrary file access or firmware export.

The [project README](https://github.com/Python-roborock/local_roborock_server) describes a self-hosted replacement backend and local control/maps. A web interface hosted on another computer must not be mistaken for an administrative interface on the vacuum. No network reconfiguration was performed during this investigation.

## Current conclusion

No verified portal for the requested file/firmware access has been found. Repeating ordinary control queries or finding another control dashboard does not resolve this gap. Useful new evidence would be an S5V-specific documented service/export procedure or an official downloadable image; no such artifact was obtained in this check. No credentials, private screenshots or device addresses are published.

## Expanded public-source search

A further search on the same date covered the exact model identifier, S5V, PearlEPro, service software, SSH references and Qrevo web interfaces. It did not identify an S5V-specific device-hosted administration portal. Search absence is not proof of absence, and no hidden endpoints were probed.

The [Local Roborock Server installation guide](https://github.com/Python-roborock/local_roborock_server/blob/main/docs/installation.md) explicitly places `/admin` on the separately deployed server and describes its administrator credentials separately from cloud and protocol credentials. Thus, search hits referring to that admin page do not establish a portal on the robot. [LocalRock](https://github.com/DonSidro/LocalRock) likewise describes itself as a client of that separately hosted backend. Neither source establishes S5V filesystem access or recording replacement.

The subsequently verified app firmware screen and app logs also report no offered update or firmware package link; see the manual-navigation follow-up in [firmware acquisition](firmware-acquisition.md).
