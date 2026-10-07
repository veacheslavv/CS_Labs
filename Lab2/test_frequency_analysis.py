import unittest

from frequency_analysis import (ALPHABET, add_substitution, full_decrypt,
                                letter_counts, partial_decrypt, recover_key,
                                sorted_by_frequency)

# Key recovered for variant 16 (cipher letter -> plaintext letter).
KEY = dict(zip("TAHOVCJQXELSZGNUBIPWDKRYFM", "abcdefghijklmnopqrstuvwxyz"))


class TestFrequencyAnalysis(unittest.TestCase):
    def test_counts_ignore_case_and_punctuation(self):
        counts = letter_counts("Wqv, wqv! 1863")
        self.assertEqual(counts["W"], 2)
        self.assertEqual(counts["V"], 2)
        self.assertEqual(sum(counts.values()), 6)

    def test_sorted_by_frequency(self):
        order = sorted_by_frequency(letter_counts("bbb aa c"))
        self.assertEqual(order[:3], ["B", "A", "C"])

    def test_partial_decrypt_marks_guesses_in_lower_case(self):
        self.assertEqual(partial_decrypt("Wqv cxipw", {"W": "t", "V": "e"}), "tQe CXIPt")

    def test_full_decrypt_keeps_case(self):
        self.assertEqual(full_decrypt("Wqv Wvsvjituq.", KEY), "The Telegraph.")

    def test_substitution_must_be_one_to_one(self):
        mapping = {"V": "e"}
        self.assertIsNotNone(add_substitution(mapping, "W", "e"))
        self.assertIsNone(add_substitution(mapping, "W", "t"))
        self.assertIsNotNone(add_substitution(mapping, "W", "th"))

    def test_recovered_key_is_a_permutation(self):
        key = recover_key(KEY)
        self.assertEqual(sorted(key.values()), list(ALPHABET))
        self.assertEqual(key["e"], "V")
        self.assertEqual(key["t"], "W")


if __name__ == "__main__":
    unittest.main()
