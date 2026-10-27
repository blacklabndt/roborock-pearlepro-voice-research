# Candidate PearlEPro package layout

Offsets are zero-based and ranges are end-exclusive. This is a working description, **not a validated decryption specification**.

For the studied Cantonese package, total length is 2,642,964 bytes:

| Region | Start | End | Length | Evidence |
| --- | ---: | ---: | ---: | --- |
| Opaque body | 0 | 2641936 | 2641936 | High entropy; candidate encrypted body |
| Trailer prefix | 2641936 (`0x285010`) | 2641940 | 4 | Observed `01 06 01 00`; semantics unknown |
| Rest of trailer | 2641940 | 2642964 | 1024 | Internal layout unresolved |

## Five-sample comparison

The following numerical relationships hold across three PearlEPro packages, one Q7 Max package and one original Qrevo package. Integers are interpreted as unsigned little-endian 32-bit values; offsets below are relative to the candidate trailer start.

| Offset | Relationship | Cantonese value |
| --- | --- | ---: |
| +956 | Body length minus 16 | 2641920 |
| +960 | Body length = total length minus 1028 | 2641936 |
| +976 | Ceiling of body length divided by 1024 | 2581 |

The value at +956 is divisible by 4,096 for all five samples. Each total file length therefore equals a multiple of 4,096 plus 16 plus 1,028. All five share the same four-byte trailer prefix.

These correlations strengthen the candidate boundary. They do not prove that the firmware uses these positions as formal fields; they could include packaging-tool state. A 16-byte difference might reflect a padding block or framing. Four-KiB alignment is consistent with an aligned filesystem image but does not identify a filesystem.

No ZIP, gzip, RIFF/WAV, Ogg, FLAC, tar `ustar`, XZ or Zstandard signatures were found in the studied Cantonese package. Its measured byte entropy is approximately 7.999927 bits/byte. Absence of these signatures and high entropy do not establish a cipher.

## Published information about related models

[Dennis Giese's device inventory](https://github.com/dgiese/robotinfo/blob/main/index.html) describes AES-256-CBC and RSA signatures for several Roborock firmware families, and describes some related sound packages as encrypted, signed SquashFS images containing Ogg audio.

[The research thesis](https://dontvacuum.me/thesis/Security_Analysis_of_the_Xiaomi_IoT_Ecosystem.pdf) describes a 256-byte RSA signature within the final 1,028 bytes and an unpacking approach also tested with sound packages. Neither source establishes every field for PearlEPro.

## Unknowns

- Exact cipher, key, IV source, framing and padding for PearlEPro.
- Signature offset, hash, RSA encoding and signed-byte range.
- Trailer-prefix semantics and which remaining fields matter to the reader.
- Plaintext container, filenames, audio codec, sample rate and channel count.

Do not assume the first sixteen bytes are an IV or that the first 256 bytes after the prefix are a signature. A decryption key, signature-verification public key and signing private key have different roles. A catalog MD5 is none of those. Structural pattern matching does not verify authenticity or establish custom-pack compatibility.
