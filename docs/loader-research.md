# Q7 Max / Qrevo loader evidence and S5V applicability

Reviewed 2026-10-26. This review found public control-adapter code and storage observations, not the native package-loader implementation. No device commands, installation, authentication bypass, or filesystem changes were performed.

## Control adapter versus package loader

[Valetudo's Roborock voice capability](https://github.com/Hypfer/Valetudo/blob/master/backend/lib/robots/roborock/capabilities/RoborockVoicePackManagementCapability.js) queries current sound state, forwards a package-download request to the robot, and reads operation progress. It contains no package decryption, archive parsing, or manufacturer-signature verification implementation. It explicitly treats package requirements as model-dependent. Its progress mapping distinguishes downloading and error states, but does not provide a complete native validation-error taxonomy.

The public adapter therefore cannot answer which authenticity checks stock S5V firmware enforces. A transport checksum and a manufacturer's signature have different roles. A client-side checksum comment is not evidence that the firmware accepts modified signed content. Shared command names likewise do not establish cross-model package compatibility.

## Audio storage evidence

[The Q7 Max inventory entry](https://github.com/dgiese/robotinfo/blob/main/detail_roborock.vacuum.a38_0.html) identifies encrypted, signed SquashFS sound packages with Ogg audio. A [firsthand Q7 Max+ report from December 2024](https://community.home-assistant.io/t/glados-portal-voice-pack-for-roborock-xiaomi-vacuums/241101) independently describes read-only Ogg audio under `/mnt/resources` on a device already running Valetudo. A subsequent participant reports separate read-only SquashFS audio mounts; that participant's exact model is not established, so those mount names are not treated as confirmed Q7 Max or S5V paths.

This distinguishes package installation from playback: audio can be exposed through a mounted filesystem rather than loose writable files in the old S5 directory. It strengthens SquashFS/Ogg as a comparison hypothesis, not a confirmed S5V layout. These reports do not provide stock-device administrator access.

## Original Qrevo evidence is weaker

[The original Qrevo a75 inventory entry](https://github.com/dgiese/robotinfo/blob/main/detail_roborock.vacuum.a75_0.html) names codename `pearl` and encrypted/signed firmware, but leaves its sound-format field blank. Its other historical support fields should not replace current upstream compatibility documentation. The Q7 Max sound-format description must not be silently attributed to Qrevo or PearlEPro.

Our [local sample comparison](cross-model-comparison.md) establishes similar outer package structures across Q7 Max, a75 and S5V. It does not establish identical native loaders, keys, signing policy, filenames, or audio codecs.

## Result and next evidence

The practical finding is that the old S5 writable-WAV model is an inadequate default for this investigation. A complete solution needs both the S5V's package-acceptance rules and its playback/storage layout. No native Q7 Max, Qrevo or S5V loader was acquired or decompiled in this review. A legitimately obtained loader/firmware artifact with model and version provenance would allow offline examination of those questions. Public controller code alone cannot resolve them.
