# Hangman Game

A graphical implementation of the classic Hangman word guessing game using Python and Pygame.

## Description

This project is a simple interactive game where players attempt to guess a hidden word by selecting letters. The game features a graphical interface with an on-screen keyboard and visual representation of the hangman figure that updates with every incorrect guess.

## Features

- **Graphical Interface**: Clean windowed application using Pygame.
- **Mouse Interaction**: Clickable letter buttons for user input.
- **Visual Progression**: Displays the hangman drawing progressively as incorrect guesses are made.
- **Win/Loss Detection**: Automatically detects when the player has won or lost the game.

## Prerequisites

Before running the game, ensure you have the following installed:

- **Python 3.x**: [Download Python](https://www.python.org/downloads/)
- **Pygame**: The game relies on the Pygame library for graphics and event handling.

## Installation

1. **Clone the repository** (or download the source files):
   ```bash
   git clone https://github.com/your-username/hangman-game.git
   cd hangman-game
   ```

2. **Install Dependencies**:
   The game script attempts to install `pygame` automatically if missing, but it is recommended to install it manually to ensure compatibility:
   ```bash
   pip install pygame
   ```

3. **Verify Assets**:
   Ensure a folder named `images` exists in the project directory containing the image assets:
   - `hangman0.png` through `hangman6.png`

## How to Play

1. **Run the Game**:
   Execute the main script from your terminal or IDE:
   ```bash
   python main.py
   ```

2. **Gameplay**:
   - A window will open showing the game board.
   - Use your mouse to click on the letters at the bottom of the screen.
   - If the letter is in the hidden word, it will appear in the correct position(s).
   - If the letter is not in the word, a part of the hangman will be drawn.

3. **Objective**:
   - **Win**: Reveal the entire word before the hangman is fully drawn.
   - **Lose**: The game ends if you make 6 incorrect guesses.

## Configuration

**Word List**: The current word list is hardcoded in `main.py`. You can modify the `words` list in the code to add your own words:
```python
words = ["python", "java", "swift", "javascript"]
```

## Project Structure

- `main.py`: The main entry point and logic for the game.
- `images/`: Directory containing the 7 hangman state images.