# Cross-model voice package comparison

Checked 2026-10-26. These are offline measurements of previously acquired samples, not compatibility tests. The existing read-only inspector generated [the full measurements and hashes](sample-comparison.json).

| Sample | Bytes | Matches all candidate trailer relationships |
| --- | ---: | --- |
| S5 Cantonese | 7,101,253 | No |
| Q7 Max Cantonese | 1,467,412 | Yes |
| Original Qrevo a75 Cantonese | 1,704,980 | Yes |
| S5V Cantonese v2 | 2,642,964 | Yes |
| S5V English | 2,991,124 | Yes |
| S5V Mandarin | 2,872,340 | Yes |

The relationships are defined in [layout.md](layout.md): a candidate 1,028-byte trailer, its marker, and three length/alignment relationships. No tested archive/audio signature was found in any sample. This remeasurement confirms earlier observations; it does not constitute a new decode.

REA's format detector rejected the S5V sample as an unsupported binary format. The existing Python measurement tool was used instead. That rejection does not establish corruption or encryption.

## Which model is a useful reference?

[Dennis Giese's inventory](https://github.com/dgiese/robotinfo/blob/main/index.html) specifically describes Q7 Max sound packages as encrypted, signed SquashFS with Ogg audio. The local Q7 Max sample matches the candidate outer structure of S5V. This makes Q7 Max a better container-comparison reference than the original S5. It does not establish shared keys, a shared installer, interchangeable packages, or an Ogg codec on S5V.

The [rrmultivoice implementation](https://github.com/erkexzcx/rrmultivoice) operates on existing audio files after root/SSH access exists. Its author's S5 setup therefore answers a different question from stock S5V package acceptance. It is not a route to obtaining administrator access.

## Remaining evidence needed

Two questions must be answered separately: how the S5V package decodes, and whether stock firmware permits owner-created packages. Decoding alone would not supply a manufacturer's signing capability. A legitimately obtained S5V loader/firmware image or a documented custom-package publishing interface would be useful evidence. Neither has been acquired here.

No package was modified or installed. No security checks were bypassed. Package binaries, private app logs, and account/device identifiers are not included.
