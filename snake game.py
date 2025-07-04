#snake game
# Snake Game with Levels, Restart & Sounds

#importing tkinter


import tkinter as tk
import random
import pygame  # for sound effects

# Initialize pygame mixer
pygame.init()
eat_sound = pygame.mixer.Sound("eat.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")

# Game constants
GAME_WIDTH = 600
GAME_HEIGHT = 400
SNAKE_SIZE = 20

# Game variables
score = 0
level = 1
SPEED = 150  # milliseconds

# Setup window
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

# Canvas for drawing the game
canvas = tk.Canvas(window, width=GAME_WIDTH, height=GAME_HEIGHT, bg="black")
canvas.pack()

# Display score and level
score_text = canvas.create_text(50, 10, fill="white", text=f"Score: {score}", anchor="nw")
level_text = canvas.create_text(500, 10, fill="white", text=f"Level: {level}", anchor="ne")

# Snake and food setup
snake = [(100, 100), (80, 100), (60, 100)]
snake_direction = "Right"
food_position = (0, 0)
food = None

# Draw snake
def draw_snake():
    canvas.delete("snake")
    for x, y in snake:
        canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill="teal", tag="snake")

# Place food
def place_food():
    global food_position, food
    x = random.randint(0, (GAME_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    y = random.randint(0, (GAME_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    food_position = (x, y)
    canvas.delete("food")
    food = canvas.create_oval(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill="yellow", tag="food")

# Move snake
def move_snake():
    global snake, food_position, score, SPEED, level

    head_x, head_y = snake[0]

    if snake_direction == "Up":
        head_y -= SNAKE_SIZE
    elif snake_direction == "Down":
        head_y += SNAKE_SIZE
    elif snake_direction == "Left":
        head_x -= SNAKE_SIZE
    elif snake_direction == "Right":
        head_x += SNAKE_SIZE

    new_head = (head_x, head_y)

    # Collision check
    if (head_x < 0 or head_x >= GAME_WIDTH or
        head_y < 0 or head_y >= GAME_HEIGHT or
        new_head in snake):
        game_over()
        return

    snake.insert(0, new_head)

    # Check for food
    if new_head == food_position:
        eat_sound.play()
        place_food()
        score += 10

        if score % 50 == 0:
            SPEED = max(50, SPEED - 10)
            level += 1
    else:
        snake.pop()

    draw_snake()
    canvas.itemconfig(score_text, text=f"Score: {score}")
    canvas.itemconfig(level_text, text=f"Level: {level}")

    window.after(SPEED, move_snake)

# Change direction
def change_direction(event):
    global snake_direction
    new_dir = event.keysym
    opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
    if new_dir in opposites and new_dir != opposites[snake_direction]:
        snake_direction = new_dir

window.bind("<Key>", change_direction)

# Game Over
def game_over():
    gameover_sound.play()
    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 20,
                       text="GAME OVER", fill="white", font=("monospace", 30))
    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 20,
                       text="Press R to Restart", fill="white", font=("monospace", 15))
    window.bind("<r>", restart_game)

# Restart game
def restart_game(event=None):
    global snake, snake_direction, score, level, SPEED
    snake = [(100, 100), (80, 100), (60, 100)]
    snake_direction = "Right"
    score = 0
    level = 1
    SPEED = 150

    canvas.delete("all")
    draw_snake()
    place_food()

    global score_text, level_text
    score_text = canvas.create_text(50, 10, fill="white", text=f"Score: {score}", anchor="nw")
    level_text = canvas.create_text(500, 10, fill="white", text=f"Level: {level}", anchor="ne")

    window.after(SPEED, move_snake)

# Start the game
place_food()
draw_snake()
move_snake()

window.mainloop()