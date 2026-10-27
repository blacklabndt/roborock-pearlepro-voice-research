# Evidence and provenance

## Official catalog and samples

The primary catalog was `https://us-app.roborock.com/app/pearlepro/voice-pkg/info`. Source URLs, versions, sample hashes and measured fields are recorded in `data/samples.json`.

US Cantonese package response observations:

- Content-Length: 2642964
- ETag: `c5471666cee5b0558f187d4b5a45e265`
- Last-Modified: `Mon, 23 Mar 2026 10:07:13 GMT`
- US catalog Last-Modified: `Tue, 16 Jun 2026 08:22:20 GMT`

The EU catalog also listed Cantonese version 2 and served identical bytes. The CN catalog listed version 4 and different bytes; it is not the studied version-2 sample. Retrieval observations are snapshots; URLs may later serve different content.

Follow-up comparison established that the Cantonese catalog hash is exactly the full-file MD5 of the Mandarin PearlEPro sample. Both the English and Mandarin files match their own catalog hashes. See [checksum study](boundary-analysis.md). This narrows the discrepancy to a likely metadata mix-up without establishing the publisher's cause or the Cantonese file's signature validity.

## Model mapping

An authenticated catalog query returned numeric product ID 179 for `roborock.vacuum.a170`, named Roborock Qrevo C, with package name `com.roborock.tanos`. No account response or identifying device information is published.

The downloaded official model-plugin ZIP has SHA-256 `4ab99db127106ce2116ab010fcafda3b740df4faea6f0f609237f7ddb059ce1b`. Its `index.android.bundle` was Hermes bytecode version 96. Offline disassembly used `hermes-dec` 0.1.8. That tool is documented at https://github.com/P1sec/hermes-dec .

Static instructions map the short-model list `a169`, `a170` to the `PearlEPro` product symbol, whose directory string is `pearlepro`. This contradicts the third-party library nickname PearlELite as a guide to this particular CDN path; it is not evidence that the entire library model definition is incorrect.

## Voice installation path

Function numbers below are specific to that exact plugin artifact and disassembler output. They are not stable API identifiers.

- Function #25998 constructs catalog-entry objects including voice ID, version, package URL, MD5 and preview URL; no encryption-key field was identified in that model.
- Function #32458 constructs an installation request from the entry and calls `setSoundPackage`.
- Exported `setSoundPackage` refers to function #5295, which forwards the caller's parameters through `Methods.SetSoundPackage`.
- The method tables map that operation to the vacuum's voice download/install command. The inspected path does not decrypt the file on the phone.
- Generic AES/CBC helper #21311 receives input bytes, key and IV as parameters. No voice-package-specific key was identified there, and no connection from the traced voice-install path to it was found.

The downloaded Android app's readable `loadSoundConfig` method selects a regional CDN, downloads the catalog JSON, caches it and reads it as text. Bounded literal searches covered three JavaScript bundles, five DEX files and ninety native-library entries. Java/native code was not fully decompiled. Obfuscation, stripped symbols and unexamined code limit any conclusion of absence.

**Inference:** the traced flow delegates package processing to the vacuum. **Not established:** that every app component lacks a decoder or that the exact device-side implementation has been identified.

## Separate audio preview

Source: `https://us-app.roborock.com/app/pearlepro/voice-pkg/wav/yueyu.wav`.

SHA-256: `6ae7ef6f39133c3a6ac85dd3118a2065cf8089e7e2103939eabaa391864afa34`.

Python's standard-library `wave` parser reported one channel, 16,000 samples/second, two bytes/sample, uncompressed PCM, 1.034 seconds. File length is 33,144 bytes. This preview was downloaded separately; no audio was extracted from the encrypted package.

## Negative results

No publicly documented decoder verified for this PearlEPro sample was found in the bounded searches performed. No decryption or signature verification succeeded. That is not proof that compatible tools do not exist.

Legacy Roborock S5 tools are not evidence of S5V compatibility. For example, https://github.com/LazyT/rrcc/blob/master/unpackager.cpp uses the older ccrypt path. Sharing a `.pkg` extension does not establish a common encoding.
