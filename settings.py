import pygame

WIDTH = 800
HEIGHT = 800
BLOCK_SIZE = 50
ROWS = WIDTH // BLOCK_SIZE
GAP_SIZE = 2

# Set up display
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

SURFACE_CLR = (0, 0, 0)
GRID_CLR = (255, 255, 255)
SNAKE_CLR = (0, 255, 0)
APPLE_CLR = (255, 0, 0)

FPS = 10
INITIAL_SNAKE_LEN = 1

GRID = [[x,y] for x in range(0, WIDTH, BLOCK_SIZE) for y in range(0, HEIGHT, BLOCK_SIZE)]