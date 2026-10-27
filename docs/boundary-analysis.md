# Follow-up: checksum scope and block comparison

These observations concern the exact sample hashes in `data/samples.json`. Results are reproducible with `analyze_boundaries.py`; the saved output is `data/boundary-analysis.json`.

## Catalog MD5 discrepancy narrowed

| PearlEPro sample | Full-file MD5 | Catalog match? |
| --- | --- | --- |
| Cantonese, ID 1001 v2 | c5471666cee5b0558f187d4b5a45e265 | No |
| English, ID 3 v3 | b773bb3543d295f94f848ce3a1fa0651 | Yes |
| Mandarin, ID 1 v3 | 681b5d6fd06612c6da56cb7c0d508596 | Yes |

The official catalog assigns the **Mandarin full-file hash** to its Cantonese entry as well. This is a directly observed equality, not a decryption result. A catalog metadata mix-up is a plausible explanation; the publisher's reason is unknown.

For each of these three files, the analysis checked MD5 over contiguous byte spans with 0, 16 or 32 bytes removed from the beginning and every suffix length from 0 through 8,192 bytes removed from the end: 24,579 candidate spans per file. The Cantonese catalog MD5 matched none. English and Mandarin matched only the complete file within this search boundary.

This rules out the tested simple framing exclusions as an explanation of the Cantonese discrepancy. It does not rule out every checksum convention, nor does it establish that an installer ignores the incorrect catalog value. No installation was attempted.

## Repeated-block comparison

The candidate encrypted body ends 1,028 bytes before EOF. Counting 16-byte blocks aligned to file offset zero found:

- No repeated block values within any of the five studied bodies.
- No shared aligned block values across any of the ten sample pairs.

Only counts are published; no cryptographic secrets or raw trailer contents are exposed. Absence of repetitions **does not identify AES, CBC, an IV, or a key**. It also does not rule out ECB when the underlying compressed content has no repeated blocks. The result supplies no basis for reusing an IV or key across these models.

## Consequence for further decoding work

The English and Mandarin packages now provide same-model, catalog-checksum-consistent reference samples for future authorized offline decoder validation. The known body/trailer relationships remain structural evidence. No decryption, plaintext extraction or signature verification has succeeded.
