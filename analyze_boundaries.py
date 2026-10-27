"""Bounded offline checks of package framing hypotheses, without key recovery."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

from inspect_package import inspect, MAX_BYTES


def prefix_matches(data, target, header_sizes=(0, 16, 32), max_trailer=8192):
    """Check MD5 of contiguous spans with a small header and bounded trailer removed."""
    if max_trailer < 0:
        raise ValueError('max_trailer must be nonnegative')
    if len(target) != 32 or any(c not in '0123456789abcdefABCDEF' for c in target):
        raise ValueError('expected a 32-digit hexadecimal MD5')
    matches = []
    for start in header_sizes:
        if start < 0 or start > len(data):
            continue
        lower = max(start, len(data) - max_trailer)
        digest = hashlib.md5(data[start:lower])
        for end in range(lower, len(data) + 1):
            if digest.hexdigest() == target.lower():
                matches.append({'header_removed': start, 'trailer_removed': len(data) - end})
            if end < len(data):
                digest.update(data[end:end + 1])
    return matches


def body_blocks(data):
    measurement = inspect(data)
    trailer = measurement['candidate_trailer']
    if not trailer or not trailer['matches_studied_pattern']:
        raise ValueError('sample does not match the studied structural pattern')
    end = trailer['start']
    return Counter(data[i:i + 16] for i in range(0, end, 16))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packages', type=Path, nargs='+')
    parser.add_argument('--manifest', type=Path, default=Path(__file__).parent / 'data/samples.json')
    args = parser.parse_args()
    manifest = {row['inspection']['sha256']: row for row in json.loads(args.manifest.read_text(encoding='utf-8'))}
    rows, sets = [], []
    for path in args.packages:
        with path.open('rb') as handle:
            data = handle.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            parser.error('sample exceeds 128 MiB')
        sha = hashlib.sha256(data).hexdigest()
        if sha not in manifest:
            parser.error('sample SHA-256 is not in the supplied manifest')
        sample = manifest[sha]
        counts = body_blocks(data)
        target = sample.get('catalog_md5')
        rows.append({
            'sample': sample['sample'], 'sha256': sha,
            'body_block_bytes': 16, 'body_block_count': sum(counts.values()),
            'repeated_block_values': sum(count > 1 for count in counts.values()),
            'duplicate_block_occurrences': sum(count - 1 for count in counts.values()),
            'catalog_md5': target,
            'checksum_span_matches': prefix_matches(data, target) if target else None,
        })
        sets.append(set(counts))
    pairs = [{'left': rows[i]['sample'], 'right': rows[j]['sample'],
              'shared_aligned_body_blocks': len(sets[i] & sets[j])}
             for i, j in itertools.combinations(range(len(rows)), 2)]
    print(json.dumps({'scope': {'removed_header_bytes': [0, 16, 32],
                               'removed_trailer_bytes_inclusive': [0, 8192],
                               'block_alignment': 'relative to file offset zero'},
                      'samples': rows, 'pair_comparisons': pairs,
                      'limitations': [
                          'Checksums cover contiguous raw-file spans, not unknown plaintext.',
                          'No repeated blocks does not identify a cipher, mode, IV or key.',
                          'No decryption or signature verification was attempted.'
                      ]}, indent=2))


if __name__ == '__main__':
    main()
