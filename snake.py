import pygame
import random
from settings import *

# Set up the display
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

class Snake:
    def __init__(self):
        # Initialize the snake at the center of the screen
        self.x, self.y = WIDTH/2, HEIGHT/2
        self.pos = [1, 0] # [x, y] direction, initially set to right
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [] # List to keep track of snake's body segments
        self.dead = False
    
    def drawSnake(self):
        # Check if snake has gone out of bounds
        if self.head.x not in range(0, WIDTH) or self.head.y not in range(0, HEIGHT):
            self.dead = True
            print('game over')
        # Check if snake has hit itself
        for square in self.body: 
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
                print('game over')

        self.body.append(self.head)

        # Move body segments to follow head
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y

        # Update head position based on current direction
        self.head.x += self.pos[0] * BLOCK_SIZE
        self.head.y += self.pos[1] * BLOCK_SIZE
        self.body.remove(self.head)

class Apple:
    def __init__(self):
        self.spawn()

    def spawn(self):
        # Randomly spawn apple
        self.x = random.randrange(0, WIDTH, BLOCK_SIZE)
        self.y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        self.apple = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    
    def drawApple(self):
        pygame.draw.rect(SCREEN, APPLE_CLR, self.apple)

    def checkSpawn(self, snake: list):
        for square in snake:
            if self.apple.colliderect(square):
                self.spawn() # Respawn apple if it collides with snake

def drawGrid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, GRID_CLR, rect, 1)

def main():
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('timesnewroman', BLOCK_SIZE * 2)
    score = font.render("1", True, "white")
    score_rect = score.get_rect(center = (WIDTH / 2, HEIGHT / 20)) # Position score at the top center

    drawGrid()

    snake = Snake()
    apple = Apple()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Update snake's direction upon key press
                if event.key == pygame.K_LEFT and snake.pos[0] != 1:
                    snake.pos[0] = -1
                    snake.pos[1] = 0
                elif event.key == pygame.K_RIGHT and snake.pos[0] != -1:
                    snake.pos[0] = 1
                    snake.pos[1] = 0      
                elif event.key == pygame.K_UP and snake.pos[1] != 1:
                    snake.pos[0] = 0
                    snake.pos[1] = -1
                elif event.key == pygame.K_DOWN and snake.pos[1] != -1:
                    snake.pos[0] = 0
                    snake.pos[1] = 1

        snake.drawSnake()
        SCREEN.fill(SURFACE_CLR)
        drawGrid()

        apple.checkSpawn(snake.body)
        apple.drawApple()

        score = font.render(f"{len(snake.body)}", True, GRID_CLR)

        pygame.draw.rect(SCREEN, SNAKE_CLR, snake.head)
        for square in snake.body:
            pygame.draw.rect(SCREEN, SNAKE_CLR, square)

        SCREEN.blit(score, score_rect)

        # Grow the snake
        if len(snake.body) < 1:
            if(snake.head.x == apple.x and snake.head.y == apple.y):
                snake.body.append(pygame.Rect(snake.x, snake.y, BLOCK_SIZE, BLOCK_SIZE))    
        else:
            # Differentiates apple from the snake's body
            if(snake.head.x == apple.x and snake.head.y == apple.y):
                snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
                

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

main()