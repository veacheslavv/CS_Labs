import unittest

from caesar_cipher import (ALPHABET, build_permuted_alphabet, caesar2_decrypt,
                           caesar2_encrypt, caesar_decrypt, caesar_encrypt,
                           normalize_text, parse_key)


class TestCaesar(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize_text("Cifrul cezar")[0], "CIFRULCEZAR")
        self.assertEqual(normalize_text("țară și ştiinţă")[0], "ȚARĂȘIȘTIINȚĂ")
        self.assertEqual(normalize_text("abc1"), (None, "1"))

    def test_keys(self):
        self.assertEqual(parse_key("3"), 3)
        self.assertEqual(parse_key("30"), 30)
        for bad in ["0", "31", "-1", "abc", "2.5", ""]:
            self.assertIsNone(parse_key(bad))

    def test_caesar_wraps_around(self):
        self.assertEqual(caesar_encrypt("Z", 1), "A")
        self.assertEqual(caesar_decrypt("A", 1), "Z")

    def test_caesar_round_trip_all_keys(self):
        m = "ȘTIINȚACALCULATOARELORĂÂÎ"
        for k in range(1, 31):
            self.assertEqual(caesar_decrypt(caesar_encrypt(m, k), k), m)

    def test_permuted_alphabet(self):
        p = build_permuted_alphabet("CRIPTOGRAFIE")
        self.assertEqual(p[:9], ["C", "R", "I", "P", "T", "O", "G", "A", "F"])
        self.assertEqual(sorted(p, key=ALPHABET.index), ALPHABET)

    def test_caesar2_round_trip(self):
        m = "ȘTIINȚACALCULATOARELOR"
        for k in range(1, 31):
            c = caesar2_encrypt(m, k, "CRIPTOGRAFIE")
            self.assertEqual(caesar2_decrypt(c, k, "CRIPTOGRAFIE"), m)


if __name__ == "__main__":
    unittest.main()
