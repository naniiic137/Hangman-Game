import pip

try:
    import pygame
except:
    pip.main(['install','pygame'])



import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 900, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hangman Game")

# Set up fonts
font = pygame.font.SysFont('comicsans', 60)
small_font = pygame.font.SysFont('comicsans', 40)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Load and resize images
images = []
for i in range(7):
    image = pygame.image.load(f"./images/hangman{i}.png")
    resized_image = pygame.transform.scale(image, (200, 200))  # Resize the image to fit the screen
    images.append(resized_image)

# Game variables
words = ["python", "java", "swift", "javascript"]
chosen_word = random.choice(words).upper()
guessed_letters = []
incorrect_guesses = 0
max_incorrect_guesses = 6

# Set up letter buttons
radius = 24
gap = 15
letters = []
startx = round((width - (radius * 2 + gap) * 13) / 2)
starty = 400
A = 65

for i in range(26):
    x = startx + gap * 2 + ((radius * 2 + gap) * (i % 13))
    y = starty + ((i // 13) * (gap + radius * 2))
    letters.append([x, y, chr(A + i), True])

# Function to draw the game window
def draw():
    win.fill(white)
    
    # Draw title
    text = font.render("Hangman Game", 1, black)
    win.blit(text, (width / 2 - text.get_width() / 2, 20))
    
    # Draw word
    display_word = ""
    for letter in chosen_word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = font.render(display_word, 1, black)
    win.blit(text, (400, 200))
    
    # Draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, black, (x, y), radius, 3)
            text = small_font.render(ltr, 1, black)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
    
    # Draw hangman image
    win.blit(images[incorrect_guesses], (150, 100))
    pygame.display.update()

# Function to check if the player has won
def check_win():
    for letter in chosen_word:
        if letter not in guessed_letters:
            return False
    return True

# Main game loop
run = True
print(chosen_word)
while run:
    draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                    if dis < radius:
                        letter[3] = False
                        guessed_letters.append(ltr)
                        if ltr in chosen_word:
                            print(f"Correct guess: {ltr}")
                        else:
                            incorrect_guesses += 1
                            print(f"Incorrect guess: {ltr}. Total incorrect guesses: {incorrect_guesses}")
    
    if check_win():
        print("You won!")
        run = False
    
    if incorrect_guesses == max_incorrect_guesses:
        print(f"You lost! The word was {chosen_word}.")
        run = False

pygame.quit()
