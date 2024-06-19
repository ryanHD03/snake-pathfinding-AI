import random
from settings import *

class Snake:
    def __init__(self):
        # Initialize the snake at the center of the screen
        self.x, self.y = 0, 0
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
        ''' Spawn a new apple ont he screen at a random position '''
        # Randomly spawn apple
        self.x = random.randrange(0, WIDTH, BLOCK_SIZE)
        self.y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        self.apple = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    
    def drawApple(self):
        pygame.draw.rect(SCREEN, APPLE_CLR, self.apple)

    def checkSpawn(self, snake: list):
        ''' Check if the apple collides with the snake. If so, respawn the apple. '''
        for square in snake:
            if self.apple.colliderect(square):
                self.spawn() # Respawn apple if it collides with snake