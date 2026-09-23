"""Hangman with Pygame: guess the word letter by letter before the drawing is complete.

Controls: click a letter or type it on the keyboard.
After a round: R = play again, Esc = quit.
"""

import math
import random
from pathlib import Path

import pygame

from hangman_logic import MAX_WRONG_GUESSES, HangmanRound, load_words, pick_word

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"
WORDS_FILE = BASE_DIR / "words.json"

WIDTH, HEIGHT = 900, 600
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (120, 120, 120)
GREEN = (30, 140, 60)
RED = (190, 40, 40)

BUTTON_RADIUS = 24
BUTTON_GAP = 15
BUTTONS_TOP = 400


class HangmanGame:
    def __init__(self, words, rng=random):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Hangman Game")
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont("comicsans", 60)
        self.word_font = pygame.font.SysFont("comicsans", 60)
        self.letter_font = pygame.font.SysFont("comicsans", 40)
        self.info_font = pygame.font.SysFont("comicsans", 26)

        self.images = [
            pygame.transform.scale(pygame.image.load(str(IMAGES_DIR / f"hangman{i}.png")), (200, 200))
            for i in range(MAX_WRONG_GUESSES + 1)
        ]

        self.words = words
        self.rng = rng
        self.wins = 0
        self.losses = 0
        self.round = None
        self.buttons = []
        self.new_round()

    # --- game state -------------------------------------------------------

    def new_round(self):
        previous = self.round.word if self.round else None
        category, word = pick_word(self.words, self.rng, exclude=previous)
        self.round = HangmanRound(word, category)
        self.buttons = self._make_buttons()

    def _make_buttons(self):
        """26 round letter buttons in two rows: [x, y, letter, visible]."""
        startx = round((WIDTH - (BUTTON_RADIUS * 2 + BUTTON_GAP) * 13) / 2)
        buttons = []
        for i in range(26):
            x = startx + BUTTON_GAP * 2 + (BUTTON_RADIUS * 2 + BUTTON_GAP) * (i % 13)
            y = BUTTONS_TOP + (i // 13) * (BUTTON_GAP + BUTTON_RADIUS * 2)
            buttons.append([x, y, chr(ord("A") + i), True])
        return buttons

    def guess(self, letter):
        """Apply a guess from the mouse or keyboard and update the score when a round ends."""
        result = self.round.guess(letter)
        if result in ("correct", "wrong"):
            for button in self.buttons:
                if button[2] == letter.upper():
                    button[3] = False
            if self.round.won:
                self.wins += 1
            elif self.round.lost:
                self.losses += 1
        return result

    def handle_event(self, event):
        """Process one event. Returns False when the game should close."""
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if self.round.finished:
                if event.key == pygame.K_r:
                    self.new_round()
            elif event.unicode and event.unicode.isalpha():
                self.guess(event.unicode)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.round.finished:
            mx, my = event.pos
            for x, y, letter, visible in self.buttons:
                if visible and math.hypot(x - mx, y - my) < BUTTON_RADIUS:
                    self.guess(letter)
                    break
        return True

    # --- drawing ------------------------------------------------------------

    def _blit_centered(self, surface, y):
        self.win.blit(surface, (WIDTH / 2 - surface.get_width() / 2, y))

    def draw(self):
        self.win.fill(WHITE)
        self._blit_centered(self.title_font.render("Hangman Game", True, BLACK), 10)

        score = self.info_font.render(f"Wins: {self.wins}   Losses: {self.losses}", True, BLACK)
        self.win.blit(score, (400, 300))

        category = self.info_font.render(f"Category: {self.round.category}", True, GREY)
        self.win.blit(category, (400, 130))

        # Show the full word once the round is over.
        text = " ".join(self.round.word) if self.round.finished else self.round.masked()
        word_surface = self.word_font.render(text, True, BLACK)
        if word_surface.get_width() > WIDTH - 420:          # long words: smaller font
            word_surface = self.letter_font.render(text, True, BLACK)
        self.win.blit(word_surface, (400, 200))

        for x, y, letter, visible in self.buttons:
            if visible:
                pygame.draw.circle(self.win, BLACK, (x, y), BUTTON_RADIUS, 3)
                label = self.letter_font.render(letter, True, BLACK)
                self.win.blit(label, (x - label.get_width() / 2, y - label.get_height() / 2))

        self.win.blit(self.images[min(self.round.wrong, MAX_WRONG_GUESSES)], (150, 100))

        if self.round.finished:
            self._draw_end_screen()
        else:
            hint = self.info_font.render("Click a letter or type it on your keyboard", True, GREY)
            self._blit_centered(hint, 535)

        pygame.display.update()

    def _draw_end_screen(self):
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((255, 255, 255, 200))
        self.win.blit(veil, (0, 0))

        box = pygame.Rect(0, 0, 560, 250)
        box.center = (WIDTH // 2, HEIGHT // 2)
        pygame.draw.rect(self.win, WHITE, box)
        pygame.draw.rect(self.win, BLACK, box, 3)

        won = self.round.won
        headline = self.title_font.render("You won!" if won else "You lost!", True, GREEN if won else RED)
        self._blit_centered(headline, box.top + 10)
        word = self.info_font.render(f"The word was {self.round.word} ({self.round.category})", True, BLACK)
        self._blit_centered(word, box.top + 95)
        score = self.info_font.render(f"Wins: {self.wins}   Losses: {self.losses}", True, BLACK)
        self._blit_centered(score, box.top + 140)
        keys = self.info_font.render("Press R to play again  /  Esc to quit", True, GREY)
        self._blit_centered(keys, box.top + 190)

    # --- main loop ----------------------------------------------------------

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if not self.handle_event(event):
                    running = False
                    break
            if running:
                self.draw()
        pygame.quit()


def main():
    HangmanGame(load_words(WORDS_FILE)).run()


if __name__ == "__main__":
    main()
