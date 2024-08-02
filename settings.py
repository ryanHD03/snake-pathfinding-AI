import pygame

WIDTH = 612
HEIGHT = 612
BLOCK_SIZE = 36
ROWS = WIDTH // BLOCK_SIZE
GAP_SIZE = 2

# Set up display
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

SURFACE_CLR = (0, 0, 0)
GRID_CLR = (255, 255, 255)
SNAKE_CLR = (0, 255, 0)
APPLE_CLR = (255, 0, 0)

FPS = 5
INITIAL_SNAKE_LEN = 1
SNAKE_MAX_LEN = ROWS * ROWS - INITIAL_SNAKE_LEN

GRID = [[x,y] for x in range(0, WIDTH, BLOCK_SIZE) for y in range(0, HEIGHT, BLOCK_SIZE)]