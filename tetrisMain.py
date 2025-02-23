import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
COLUMNS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[1, 1, 0], [0, 1, 1]],  # Z shape
    [[0, 1, 1], [1, 1, 0]],  # S shape
    [[1, 1, 1], [0, 1, 0]],  # T shape
    [[1, 1, 1], [1, 0, 0]],  # L shape
    [[1, 1, 1], [0, 0, 1]]   # J shape
]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x, self.y = COLUMNS // 2 - len(self.shape[0]) // 2, 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Game functions
def draw_grid(surface):
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(surface, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, WHITE, (0, y), (WIDTH, y))

def draw_tetromino(surface, tetromino):
    for row_idx, row in enumerate(tetromino.shape):
        for col_idx, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, tetromino.color, 
                                 pygame.Rect((tetromino.x + col_idx) * GRID_SIZE, 
                                             (tetromino.y + row_idx) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    tetromino = Tetromino()

    while running:
        screen.fill(BLACK)
        draw_grid(screen)
        draw_tetromino(screen, tetromino)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    main()
