# Roborock PearlEPro / S5V voice-package research

Offline format research for the official Cantonese voice package associated with **Roborock Qrevo S5V, model `roborock.vacuum.a170`**. The authenticated product catalog called the same model **Roborock Qrevo C**. The investigated device reported firmware **02.16.64**.

**Status: structural inspection only. No successful decryption, extracted audio, verified signing scheme, or custom-pack installation.** This repository is not a decoder or an installer.

## Findings

- The official product catalog identifies `a170` as numeric product **179**. The account's opaque product identifier is a different identifier and was rejected by the older plugin endpoint.
- Static inspection of the official model plugin maps `a169`/`a170` to **PearlEPro**, whose catalog directory is **`pearlepro`**. A third-party library's PearlELite nickname initially led to incorrect URL guesses.
- The [official US catalog](https://us-app.roborock.com/app/pearlepro/voice-pkg/info) listed Cantonese (`粤语版`), **voice ID 1001, version 2**. Its [package URL](https://us-app.roborock.com/app/pearlepro/voice-pkg/package/yueyu.pkg) returned 2,642,964 bytes.
- Five official samples share a candidate 1,028-byte trailer and reproducible length relationships. Three samples are from PearlEPro; the other two are Q7 Max and original Qrevo. See [layout notes](docs/layout.md) and [measurements](data/samples.json).
- The traced app/plugin path passes catalog metadata to the vacuum's voice download/install command. No voice-package decoder or key was identified in the inspected app paths. This was not a complete native-code audit.
- The separate official Cantonese preview is mono, 16 kHz, 16-bit PCM WAV, lasting 1.034 seconds. **This does not establish the codec inside the encrypted package.**

## Integrity caveat

The downloaded Cantonese file's MD5 is `c5471666cee5b0558f187d4b5a45e265`, while the catalog lists `681b5d6fd06612c6da56cb7c0d508596`. A US re-download with a cache-busting query produced identical bytes and matched the CDN ETag. The EU copy also returned identical bytes with the same catalog discrepancy.

**Follow-up finding:** the MD5 listed for Cantonese exactly matches the complete **Mandarin** package (`prc.pkg`). Both Mandarin and English match their own catalog MD5 values over the complete files. This supports a catalog metadata mix-up; it does not prove why the wrong value was published or verify the Cantonese signature. See [boundary and checksum analysis](docs/boundary-analysis.md).

SHA-256 of the studied file:

```text
36d728688f08ea7d4d99116c0c00606546b7613b3c17c3cd4ecd5d5a76dbf87c
```

The file is content served by the official URL, but **catalog checksum verification failed**. No modified or downloaded package was installed during this investigation.

## Reproduce offline inspection

Requires Python 3.10+ and only the standard library. Obtain your own samples from the official URLs recorded in `data/samples.json`; upstream content may change. Compare SHA-256 before comparing results.

```console
python inspect_package.py /path/to/yueyu.pkg --output inspection.json
```

For the bounded checksum-span and repeated-block study, use known samples from the manifest:

```console
python analyze_boundaries.py /path/to/yueyu.pkg /path/to/en.pkg /path/to/prc.pkg
python -m unittest discover -v
```

The script reads a local file and reports hashes, selected file signatures, entropy and candidate trailer relationships. It does not contact a vacuum or cloud service, decrypt, extract archives, or change its input. A matching pattern is not cryptographic verification.

## Help wanted

Please open an issue with reproducible, non-sensitive evidence addressing:

1. A published PearlEPro format specification or compatible offline decoder.
2. The meaning of the trailer fields and whether they are consumed by the device or merely packaging-tool artifacts.
3. Documented IV/framing and padding conventions for this package family.
4. The signature's exact location, encoding, digest and covered byte range.
5. An explanation of the catalog MD5 discrepancy.
6. Audio codec and filesystem metadata from a legitimately obtained plaintext sample, including its provenance.

State the model, voice ID/version, source URL, sample SHA-256, tool/version and whether your result is observed or inferred. Do not post account tokens, verification codes, private logs, device identifiers or protected keys. See [contributing](CONTRIBUTING.md).

## Evidence and limitations

See [provenance and app inspection](docs/evidence.md). Binary packages, proprietary APKs/plugins, disassemblies, account helpers, credentials and private device logs are not redistributed here. Public CDN links are supplied for independent reproduction. The repository contains original summaries and limited format measurements, not manufacturer source code.

Research notes were prepared with AI assistance and checked against the recorded local measurements. Cryptographic interpretations remain hypotheses until independently validated. This project is not affiliated with Roborock.

Original code and notes in this repository are under the [MIT license](LICENSE). That license does not cover linked third-party artifacts.
