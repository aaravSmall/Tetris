import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 700  # Increased height to make space for score
GRID_SIZE = 30
COLUMNS, ROWS = WIDTH // GRID_SIZE, (HEIGHT - 100) // GRID_SIZE  # Leave 100px for score display
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (128, 128, 128)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]

# Tetromino shapes
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
    def __init__(self, grid):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x, self.y = COLUMNS // 2 - len(self.shape[0]) // 2, 0
        self.landed = False
        self.grid = grid

    def rotate(self):
        if not self.landed:
            rotated_shape = [list(row) for row in zip(*self.shape[::-1])]
            if self.y + len(rotated_shape) <= ROWS and not self.collides(self.x, self.y, rotated_shape):
                self.shape = rotated_shape

    def move(self, dx, dy):
        if not self.landed and not self.collides(self.x + dx, self.y + dy, self.shape):
            self.x += dx
            self.y += dy
    
    def hard_drop(self):
        while not self.collides(self.x, self.y + 1, self.shape):
            self.y += 1
        self.landed = True
        self.add_to_grid()
    
    def check_landing(self):
        if self.collides(self.x, self.y + 1, self.shape):
            self.landed = True
            self.add_to_grid()

    def collides(self, x, y, shape):
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    if x + col_idx < 0 or x + col_idx >= COLUMNS or y + row_idx >= ROWS:
                        return True
                    if self.grid[y + row_idx][x + col_idx]:
                        return True
        return False
    
    def add_to_grid(self):
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    self.grid[self.y + row_idx][self.x + col_idx] = self.color

def clear_rows(grid):
    full_rows = [i for i in range(ROWS) if all(grid[i])]
    points = [0, 100, 300, 500, 800]  # Points for clearing 1, 2, 3, or 4 rows
    score = 0
    for row in full_rows:
        del grid[row]
        grid.insert(0, [None for _ in range(COLUMNS)])
    score += points[len(full_rows)] if len(full_rows) < len(points) else points[-1]
    return score

def draw_grid(surface):
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(surface, WHITE, (x, 100), (x, HEIGHT))
    for y in range(100, HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, WHITE, (0, y), (WIDTH, y))

def draw_tetrominos(surface, grid, active_tetromino):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, cell, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE + 100, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, GRAY, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE + 100, GRID_SIZE, GRID_SIZE), 2)
    if active_tetromino:
        for row_idx, row in enumerate(active_tetromino.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, active_tetromino.color, 
                                     pygame.Rect((active_tetromino.x + col_idx) * GRID_SIZE, 
                                                 (active_tetromino.y + row_idx) * GRID_SIZE + 100, 
                                                 GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(surface, GRAY, 
                                     pygame.Rect((active_tetromino.x + col_idx) * GRID_SIZE, 
                                                 (active_tetromino.y + row_idx) * GRID_SIZE + 100, 
                                                 GRID_SIZE, GRID_SIZE), 2)

def draw_score(surface, score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
    tetromino = Tetromino(grid)
    fall_time = 0
    fall_speed = 30
    score = 0

    while running:
        screen.fill(BLACK)
        draw_score(screen, score)
        draw_grid(screen)
        draw_tetrominos(screen, grid, tetromino)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not tetromino.landed:
                    if event.key == pygame.K_LEFT:
                        tetromino.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        tetromino.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        tetromino.move(0, 1)
                    elif event.key == pygame.K_UP:
                        tetromino.rotate()
                    elif event.key == pygame.K_SPACE:
                        tetromino.hard_drop()
        
        fall_time += 1
        if fall_time >= fall_speed:
            if not tetromino.landed:
                tetromino.move(0, 1)
                tetromino.check_landing()
            fall_time = 0
        
        if tetromino.landed:
            score += clear_rows(grid)
            tetromino = Tetromino(grid)
        
        clock.tick(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()


fojvbowrbvik bnroivbfktrsjve

ovnwoan