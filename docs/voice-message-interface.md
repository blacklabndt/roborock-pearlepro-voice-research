# Voice-message playback: a separate compatibility lead

Investigation date: 2026-10-26. Status: static evidence only; no playback request sent and no S5V support confirmed.

## Finding

**Live UI follow-up, 2026-10-26:** inspected the selected S5V's normal Android app screens over owner-authorized wireless ADB. Robot Voice showed volume, official language choices and a single Cantonese entry under Custom Tones, marked Current. No upload, recording or per-event assignment control was visible. More Options showed DND, charging, button-light, child-lock and offline-map settings, with no audio controls. Remote Control showed directional controls, Spot Clean and Back to Dock, with no microphone/send-recording control. The main device screen likewise exposed no recording control. This is a negative result for these inspected screens and configuration, not proof that every firmware or region lacks the feature. No playback, movement, installation or settings-change control was activated. Private screenshots are not published.

The previously acquired official model plugin contains a phone-recording-to-robot playback flow. This is distinct from downloading a system voice package and from rrmultivoice's filesystem replacement approach.

The installed python-roborock 7.13.0 command enumeration includes `PLAY_AUDIO = "play_audio"`. A search of the installed Python package found the declaration but no dedicated implementation establishing its payload or supported models. The [upstream command enumeration](https://github.com/Python-roborock/python-roborock/blob/main/roborock/roborock_typing.py) is a reference, not a device capability guarantee.

## Reproducible static evidence

Artifact: official model-plugin ZIP SHA-256 `4ab99db127106ce2116ab010fcafda3b740df4faea6f0f609237f7ddb059ce1b`. Function identifiers below refer to its Hermes v96 bundle disassembled with hermes-dec 0.1.8, as described in [the evidence notes](evidence.md). These identifiers are not stable across plugin versions.

| Location | Observation | Limit |
| --- | --- | --- |
| Function 5389 | Exposed as `playAudio`; forwards the `play_audio` method and caller data to the shared request helper | Does not establish device-side implementation |
| Functions 29521 and 29576 | `robotPlayAudio` generator bodies retrieve phone recordings through `getRecordData`, prepare protected audio data and call `playAudio` | No claim about accepted codec, duration or S5V support |
| Surrounding recording UI | References `RRRecorder`, recording permissions, `send_voice_record` and `long_press_to_send_voice` | Indicates a voice-message feature, not replacement of built-in prompts |
| Function 5085 | `isRecordSupported` checks presence of the native `RRRecorder` module and a numeric API-level threshold | This is an app-side capability check, not proof of robot support |
| Function 5710 | `isRecordAllowed` checks platform/API constraints, a defined numeric `robotNewFeatures` value, then tests mask 1024 (bit 10) | The current S5V value has not been established; other surrounding UI conditions also apply |

The recording functions use a public-key-based protected transport. That observation does not link the transport to PearlEPro package encryption, supply a package decryption key or establish a way to modify signed packages. No secrets were extracted.

The separate `isNativeSupportPlayAudio` helper is also used by sound-package preview UI. Its name alone must not be treated as a device capability flag for arbitrary audio.

## What this changes

If the S5V officially exposes the recording feature, it could offer a way to play user-created speech on the vacuum without modifying its filesystem. That is a conditional possibility, not an established solution. A shared plugin can contain functionality for other models.

Even successful voice-message playback would not demonstrate automatic replacement of cleaning, docking or error announcements. Event integration, timing, codec limits and coexistence with normal prompts would remain separate questions.

## Next verification

### Can this replace cleaning and error announcements?

A follow-up bounded search of the shared plugin's explicit voice/audio/sound identifiers and the traced playback functions did not identify a registration API mapping user recordings to cleaning or error events. This is not a complete firmware audit and does not prove such an interface cannot exist.

The observed message playback path accepts recording data for an immediate playback request. No event-binding or persistent prompt replacement was identified in that path. Voice-service switches and sound-volume controls are not evidence of per-event audio substitution.

Three distinct approaches must therefore remain separate:

| Approach | Can replace the original event announcement? | S5V status |
| --- | --- | --- |
| Compatible system voice pack | In principle, if the device accepts a pack containing the relevant prompts | No custom-pack acceptance or construction demonstrated |
| On-device sound-file replacement, as used by rrmultivoice | In principle, where the firmware opens compatible writable files for those events | Administrative access, paths and playback behavior unverified |
| External event automation plus voice-message playback | Can potentially add a message; does not itself replace the original | S5V playback support unverified; event coverage, latency and volume interaction untested |

Muting normal announcements is not an established workaround: it could also mute message playback, suppress useful fault reports or produce timing gaps while volume is changed. No per-channel mute separation has been established. A replacement error message should preserve the original fault meaning and recovery advice.

There is currently no verified way in this investigation to replace the S5V's cleaning/error announcements. Demonstrating a normal voice-message feature would be useful, but would not resolve the persistent replacement requirement.

### Independent review and follow-up

Claude Code reviewed these research summaries on 2026-10-26 without device access or independent artifact inspection. Its useful additional distinction: a successful manual recording through the app would not establish a supported programmatic playback interface for automation. Neither automatic event playback nor persistent announcement replacement has been demonstrated.

Further inspection of the existing disassembly found assignments from a response's `new_feature_info` field to `robotNewFeatures`. This narrows the field provenance; it does not establish the S5V's current value. The saved Android log had no numeric value for either field. The cloud `newFeatureSet` field must not be substituted based on its similar name.

The review also emphasized that rrmultivoice rotates a filename after detecting it open. Under normal open-file semantics, a player retaining that descriptor reads the previous inode. To replace the first occurrence of an event, the desired recording must already be in place before the player opens it. Actual S5V playback behavior remains unknown.

The review is advisory. Absence of a demonstrated interface is not proof that no interface exists, and the current evidence does not justify claiming S5V modification is impossible.

1. Inspect the normal app controls for the selected S5V for a send-recording feature. Do not force-enable hidden controls.
2. If accessible through an existing authenticated read-only status response, inspect only the relevant capability value and establish its mapping to `robotNewFeatures`. Do not assume a similarly named cloud field has identical semantics.
3. If the normal app exposes the feature, use a short original recording through that supported UI to verify actual speaker playback. Record model, firmware and outcome without publishing account or device identifiers.
4. If the feature is absent or unsupported, keep this as a negative/unresolved compatibility result; do not infer that sending speculative RPC payloads will enable it.

The connected Android device was not available to ADB during this follow-up, so no current UI verification was possible. No vacuum settings, firmware, sound files or voice packs were changed.

## Public-source compatibility check

Live follow-up on 2026-10-26: Mindsolo's [voice-pack builder](https://vacuum.mindsolo.net/en/create/voicepack) listed 540 selectable models. Filtering by `a170` returned 0 of 540, and replacing the search with `S5V` also returned no models. The general model catalog likewise returned no result for `a170`. Its [creation guide](https://vacuum.mindsolo.net/en/info/create-voicepack) documents MP3/WAV/OGG uploads for supported models, but that general upload capability is not evidence of S5V support. No recording was uploaded and no alternate model was selected to build an incompatible package.

- The [rrmultivoice issue listing](https://github.com/erkexzcx/rrmultivoice/issues?q=is%3Aissue) returned no issues in an all-states API query during this check. This supplies no additional S5V compatibility evidence.
- The [Valetudo supported-robots list](https://valetudo.cloud/pages/general/supported-robots/) does not list Qrevo S5V/a170 and explicitly describes its list as exhaustive.
- [Home Assistant's Roborock integration](https://www.home-assistant.io/integrations/roborock) documents control and monitoring of Qrevo-series devices. Its documented functionality does not establish arbitrary-audio upload or an administrative filesystem interface. Integration support is not rrmultivoice installation support.
