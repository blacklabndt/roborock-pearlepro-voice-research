import struct
import unittest

from inspect_package import inspect


class InspectorTests(unittest.TestCase):
    def test_empty_and_short_files_are_not_patterns(self):
        for data in (b'', b'abc', bytes(1027)):
            result = inspect(data)
            self.assertIsNone(result['candidate_trailer'])
            self.assertFalse(result['decrypted'])
            self.assertFalse(result['authenticity_verified'])

    def test_marker_alone_is_insufficient(self):
        trailer = bytearray(1028)
        trailer[:4] = bytes.fromhex('01060100')
        result = inspect(bytes(4096 + 16) + trailer)
        self.assertFalse(result['candidate_trailer']['matches_studied_pattern'])

    def test_synthetic_layout_and_corrupted_length(self):
        body_size = 4096 + 16
        trailer = bytearray(1028)
        trailer[:4] = bytes.fromhex('01060100')
        for offset, value in ((956, 4096), (960, body_size), (976, 5)):
            struct.pack_into('<I', trailer, offset, value)
        result = inspect(bytes(body_size) + trailer)
        self.assertTrue(result['candidate_trailer']['matches_studied_pattern'])
        self.assertFalse(result['authenticity_verified'])
        struct.pack_into('<I', trailer, 960, body_size + 1)
        self.assertFalse(inspect(bytes(body_size) + trailer)['candidate_trailer']['matches_studied_pattern'])


if __name__ == '__main__':
    unittest.main()
