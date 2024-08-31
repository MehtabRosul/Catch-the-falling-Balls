import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
DARK_BLUE = (0, 102, 204)
DARK_GREEN = (0, 153, 76)
DARK_RED = (204, 0, 0)
LIGHT_GRAY = (211, 211, 211)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Objects Game")

# Basket setup
basket_width = 100
basket_height = 20
basket_speed = 10

# Falling object setup
object_size = 20
object_speed = 7

# Initial score
score = 0

# Font setup
font = pygame.font.Font(None, 36)

# High score file setup
high_score_file = "high_score.txt"

def load_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, 'r') as file:
            return int(file.read())
    return 0

def save_high_score(high_score):
    with open(high_score_file, 'w') as file:
        file.write(str(high_score))

# Load the high score
high_score = load_high_score()

# Generate a random position for a new falling object
def random_object_position():
    return random.randint(0, SCREEN_WIDTH - object_size), 0

# Main game function
def main():
    global score, high_score
    clock = pygame.time.Clock()
    running = True

    # Basket initial position
    basket_x = (SCREEN_WIDTH - basket_width) // 2
    basket_y = SCREEN_HEIGHT - basket_height - 10

    # List to store falling objects
    objects = [random_object_position()]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - basket_width:
            basket_x += basket_speed

        # Update falling objects
        new_objects = []
        for obj_x, obj_y in objects:
            obj_y += object_speed
            if obj_y > SCREEN_HEIGHT:
                continue  # Object missed
            if basket_y < obj_y + object_size and basket_x < obj_x < basket_x + basket_width:
                score += 1
            else:
                new_objects.append((obj_x, obj_y))
        objects = new_objects

        # Add a new object occasionally
        if random.randint(1, 20) == 1:
            objects.append(random_object_position())

        # Clear screen and fill with gradient background
        screen.fill(LIGHT_GRAY)
        for i in range(0, SCREEN_HEIGHT, 2):
            pygame.draw.line(screen, (230, 230, 230 - i // 3), (0, i), (SCREEN_WIDTH, i))

        # Draw basket
        pygame.draw.rect(screen, DARK_BLUE, (basket_x, basket_y, basket_width, basket_height))

        # Draw objects
        for obj_x, obj_y in objects:
            pygame.draw.ellipse(screen, DARK_RED, (obj_x, obj_y, object_size, object_size))

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw high score
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (SCREEN_WIDTH - 200, 10))

        # Update screen
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
