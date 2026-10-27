import hashlib
import unittest

from analyze_boundaries import prefix_matches


class BoundaryTests(unittest.TestCase):
    def test_detects_exact_documented_span(self):
        data = b'H' * 16 + b'example payload' + b'T' * 12
        target = hashlib.md5(b'example payload').hexdigest()
        self.assertEqual(prefix_matches(data, target, max_trailer=12),
                         [{'header_removed': 16, 'trailer_removed': 12}])

    def test_trailer_search_is_bounded(self):
        data = b'payload' + b'T' * 13
        target = hashlib.md5(b'payload').hexdigest()
        self.assertEqual(prefix_matches(data, target, max_trailer=12), [])

    def test_invalid_digest_is_rejected(self):
        with self.assertRaises(ValueError):
            prefix_matches(b'data', 'not-a-checksum')


if __name__ == '__main__':
    unittest.main()
