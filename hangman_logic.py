"""Game rules for Hangman, kept separate from the Pygame drawing code so they can be tested."""

import json
import random
import string

MAX_WRONG_GUESSES = 6


class HangmanRound:
    """One round: a secret word, the letters guessed so far and the wrong-guess count."""

    def __init__(self, word, category="", max_wrong=MAX_WRONG_GUESSES):
        self.word = word.upper()
        self.category = category
        self.max_wrong = max_wrong
        self.guessed = set()
        self.wrong = 0

    def guess(self, letter):
        """Guess a letter. Returns 'correct', 'wrong', 'repeat', 'invalid' or 'over'."""
        letter = letter.upper()
        if self.finished:
            return "over"
        if len(letter) != 1 or letter not in string.ascii_uppercase:
            return "invalid"
        if letter in self.guessed:
            return "repeat"
        self.guessed.add(letter)
        if letter in self.word:
            return "correct"
        self.wrong += 1
        return "wrong"

    def masked(self):
        """The word as shown to the player, e.g. 'P _ T _ O N'."""
        return " ".join(c if c in self.guessed else "_" for c in self.word)

    @property
    def won(self):
        return all(c in self.guessed for c in self.word)

    @property
    def lost(self):
        return self.wrong >= self.max_wrong

    @property
    def finished(self):
        return self.won or self.lost


def load_words(path):
    """Load {category: [WORDS]} from a JSON file, keeping only A-Z words."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    words = {}
    for category, items in data.items():
        cleaned = [w.strip().upper() for w in items
                   if w.strip() and all(c in string.ascii_letters for c in w.strip())]
        if cleaned:
            words[category] = cleaned
    if not words:
        raise ValueError(f"No usable words found in {path}")
    return words


def pick_word(words, rng=random, exclude=None):
    """Pick a random (category, word), avoiding `exclude` when another word exists."""
    choices = [(cat, w) for cat, items in words.items() for w in items]
    if exclude is not None and len(choices) > 1:
        choices = [c for c in choices if c[1] != exclude]
    return rng.choice(choices)
