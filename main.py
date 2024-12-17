import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Obstacle Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

def main():
    # Player attributes
    player_width = 50
    player_height = 50
    player_x = 100
    player_y = SCREEN_HEIGHT - player_height - 10
    player_speed = 5

    # Obstacle attributes
    obstacle_width = 50
    obstacle_height = 50
    obstacle_speed = 5

    # Goal attributes
    goal_width = 50
    goal_height = 50
    goal_x = SCREEN_WIDTH - goal_width - 10
    goal_y = SCREEN_HEIGHT - goal_height - 10

    # Item attributes
    item_width = 30
    item_height = 30
    item_x = random.randint(50, SCREEN_WIDTH - item_width - 50)
    item_y = random.randint(50, SCREEN_HEIGHT - item_height - 50)
    item_collected = False

    # Initialize obstacles
    obstacles = []
    for i in range(3):
        obstacle_x = random.randint(300, SCREEN_WIDTH - 100)
        obstacle_y = random.randint(50, SCREEN_HEIGHT - 100)
        obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))

    # Player rect
    player = pygame.Rect(player_x, player_y, player_width, player_height)

    # Goal rect
    goal = pygame.Rect(goal_x, goal_y, goal_width, goal_height)

    # Item rect
    item = pygame.Rect(item_x, item_y, item_width, item_height)

    # Game loop
    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main()
                return

        if not game_over:
            # Handle player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= player_speed
            if keys[pygame.K_RIGHT] and player.right < SCREEN_WIDTH:
                player.x += player_speed
            if keys[pygame.K_UP] and player.top > 0:
                player.y -= player_speed
            if keys[pygame.K_DOWN] and player.bottom < SCREEN_HEIGHT:
                player.y += player_speed

            # Move obstacles
            for obstacle in obstacles:
                obstacle.y += obstacle_speed
                if obstacle.top > SCREEN_HEIGHT:
                    obstacle.x = random.randint(300, SCREEN_WIDTH - 100)
                    obstacle.y = random.randint(-100, -50)

            # Check for collisions
            for obstacle in obstacles:
                if player.colliderect(obstacle):
                    print("Game Over!")
                    game_over = True

            # Check if player collects the item
            if not item_collected and player.colliderect(item):
                item_collected = True
                print("Item Collected!")

            # Check if player reaches the goal
            if player.colliderect(goal):
                if item_collected:
                    print("You Win!")
                    game_over = True
                else:
                    print("You must collect the item first!")

        # Draw everything
        screen.fill(WHITE)
        if not game_over:
            pygame.draw.rect(screen, GREEN, player)
            pygame.draw.rect(screen, BLUE, goal)
            if not item_collected:
                pygame.draw.rect(screen, YELLOW, item)
            for obstacle in obstacles:
                pygame.draw.rect(screen, RED, obstacle)
        else:
            font = pygame.font.Font(None, 74)
            text = font.render("Press Enter to Replay", True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        # Update the display
        pygame.display.flip()

        # Control frame rate
        clock.tick(30)

main()
