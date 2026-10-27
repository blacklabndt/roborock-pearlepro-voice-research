"""Read-only package measurements; no decryption or authenticity claims."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import struct

MAX_BYTES = 128 * 1024 * 1024
SIGNATURES = {
    'zip': b'PK\x03\x04', 'gzip': b'\x1f\x8b\x08', 'riff': b'RIFF',
    'ogg': b'OggS', 'flac': b'fLaC', 'tar_ustar': b'ustar',
    'xz': b'\xfd7zXZ\x00', 'zstd': b'\x28\xb5\x2f\xfd',
    'squashfs_le': b'hsqs',
}


def inspect(data):
    size = len(data)
    counts = Counter(data)
    entropy = -sum((n / size) * math.log2(n / size) for n in counts.values()) if size else 0
    result = {
        'bytes': size,
        'sha256': hashlib.sha256(data).hexdigest(),
        'md5': hashlib.md5(data).hexdigest(),
        'entropy_bits_per_byte': round(entropy, 6),
        'signature_first_offsets': {name: data.find(sig) for name, sig in SIGNATURES.items()},
        'candidate_trailer': None,
        'decrypted': False,
        'authenticity_verified': False,
    }
    if size >= 1028:
        start = size - 1028
        trailer = data[start:]
        a, b, c = (struct.unpack_from('<I', trailer, offset)[0] for offset in (956, 960, 976))
        checks = {
            'marker_matches': trailer[:4] == bytes.fromhex('01060100'),
            'field956_equals_body_minus16': a == start - 16,
            'field960_equals_body': b == start,
            'field956_is_4096_aligned': a % 4096 == 0,
            'field976_equals_ceil_body_div1024': c == (start + 1023) // 1024,
        }
        result['candidate_trailer'] = {
            'start': start, 'length': 1028, 'prefix_hex': trailer[:4].hex(),
            'u32le_at_956': a, 'u32le_at_960': b, 'u32le_at_976': c,
            'checks': checks,
            'matches_studied_pattern': start >= 16 and all(checks.values()),
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output and args.output.resolve() == args.package.resolve():
        parser.error('output must not overwrite the input package')
    with args.package.open('rb') as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        parser.error('input exceeds the 128 MiB inspection limit')
    output = json.dumps(inspect(data), indent=2) + '\n'
    if args.output:
        with args.output.open('x', encoding='utf-8') as handle:
            handle.write(output)
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
