import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hangman_logic import HangmanRound, load_words, pick_word  # noqa: E402

WORDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.json")


class RoundTests(unittest.TestCase):
    def test_masked_word(self):
        r = HangmanRound("python")
        self.assertEqual(r.masked(), "_ _ _ _ _ _")
        r.guess("p")
        r.guess("O")
        self.assertEqual(r.masked(), "P _ _ _ O _")

    def test_correct_wrong_repeat_invalid(self):
        r = HangmanRound("java")
        self.assertEqual(r.guess("a"), "correct")
        self.assertEqual(r.guess("A"), "repeat")
        self.assertEqual(r.guess("z"), "wrong")
        self.assertEqual(r.guess("1"), "invalid")
        self.assertEqual(r.guess("ab"), "invalid")
        self.assertEqual(r.wrong, 1)

    def test_win(self):
        r = HangmanRound("java")
        for letter in "JAV":
            r.guess(letter)
        self.assertTrue(r.won)
        self.assertTrue(r.finished)
        self.assertEqual(r.guess("x"), "over")

    def test_lose_after_six_wrong_guesses(self):
        r = HangmanRound("java")
        for letter in "BCDEFG":
            r.guess(letter)
        self.assertTrue(r.lost)
        self.assertFalse(r.won)
        self.assertEqual(r.guess("J"), "over")


class WordListTests(unittest.TestCase):
    def test_words_file_is_valid(self):
        words = load_words(WORDS_FILE)
        self.assertGreaterEqual(len(words), 3)
        total = sum(len(items) for items in words.values())
        self.assertGreaterEqual(total, 50)
        for items in words.values():
            for word in items:
                self.assertTrue(word.isalpha() and word.isupper(), word)

    def test_pick_word_avoids_previous_word(self):
        words = {"A": ["ONE", "TWO"]}
        rng = random.Random(0)
        for _ in range(20):
            self.assertEqual(pick_word(words, rng, exclude="ONE"), ("A", "TWO"))

    def test_pick_word_with_single_word(self):
        self.assertEqual(pick_word({"A": ["ONE"]}, exclude="ONE"), ("A", "ONE"))


if __name__ == "__main__":
    unittest.main()
