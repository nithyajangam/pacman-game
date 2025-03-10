import pygame
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
BLOCK_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pac-Man AI')

# Maze layout (1 represents wall, 0 represents path)
maze_layout = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Pac-Man class
class PacMan:
    def __init__(self):
        self.x = 40
        self.y = 40
        self.size = BLOCK_SIZE
        self.color = YELLOW
        self.direction = "RIGHT"
        self.speed = BLOCK_SIZE

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size // 2)

    def move(self):
        if self.direction == "UP" and self.y > 0 and not self.is_wall(self.x, self.y - self.speed):
            self.y -= self.speed
        elif self.direction == "DOWN" and self.y < HEIGHT - self.size and not self.is_wall(self.x, self.y + self.speed):
            self.y += self.speed
        elif self.direction == "LEFT" and self.x > 0 and not self.is_wall(self.x - self.speed, self.y):
            self.x -= self.speed
        elif self.direction == "RIGHT" and self.x < WIDTH - self.size and not self.is_wall(self.x + self.speed, self.y):
            self.x += self.speed

    def is_wall(self, x, y):
        # Check if the position collides with a wall based on the maze layout
        row = y // BLOCK_SIZE
        col = x // BLOCK_SIZE
        if maze_layout[row][col] == 1:
            return True
        return False

# Ghost class
class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = BLOCK_SIZE
        self.color = RED
        self.speed = BLOCK_SIZE

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size // 2)

    def move(self, pacman_x, pacman_y):
        # Simple AI: chase Pac-Man
        if self.x < pacman_x:
            self.x += self.speed
        elif self.x > pacman_x:
            self.x -= self.speed
        if self.y < pacman_y:
            self.y += self.speed
        elif self.y > pacman_y:
            self.y -= self.speed

# Function to draw the maze
def draw_maze():
    for row in range(len(maze_layout)):
        for col in range(len(maze_layout[row])):
            if maze_layout[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Main function
def main():
    pacman = PacMan()
    ghosts = [Ghost(random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                    random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE) for _ in range(3)]

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(BLACK)
        
        draw_maze()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.direction = "UP"
                elif event.key == pygame.K_DOWN:
                    pacman.direction = "DOWN"
                elif event.key == pygame.K_LEFT:
                    pacman.direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    pacman.direction = "RIGHT"

        # Pac-Man movement
        pacman.move()

        # Ghost movement (AI)
        for ghost in ghosts:
            ghost.move(pacman.x, pacman.y)

        # Draw the Pac-Man and ghosts
        pacman.draw()
        for ghost in ghosts:
            ghost.draw()

        # Refresh the game screen
        pygame.display.update()
        clock.tick(FPS)

# Run the game
if __name__ == "__main__":
    main()
    pygame.quit()
