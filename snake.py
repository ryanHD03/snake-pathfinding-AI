import random
from settings import *
from copy import deepcopy

def create_duplicate_snake(snake):
    dup_snake = Snake()
    dup_snake.pos = deepcopy(snake.pos)
    dup_snake.head = deepcopy(snake.head)
    dup_snake.body = deepcopy(snake.body)
    dup_snake.dead = deepcopy(snake.dead)
    dup_snake.tail = deepcopy(snake.tail)
    return dup_snake

class Snake:
    def __init__(self):
        # Initialize the snake at the center of the screen
        self.x, self.y = 0, 0
        self.pos = [1, 0] # [x, y] direction, initially set to right
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [] # List to keep track of snake's body segments
        self.dead = False
        if self.body:
            self.tail = self.body[-1]
        else:
            self.tail = self.head
        self.score = 0

    def drawSnake(self):
        pygame.draw.rect(SCREEN, SNAKE_CLR, self.head)
        for segment in self.body:
            pygame.draw.rect(SCREEN, SNAKE_CLR, segment)

    def go_to(self, position):
        if position[0] > 0 and self.pos != [-1, 0]:
            self.pos = [1, 0]
        elif position[0] < 0 and self.pos != [1, 0]:
            self.pos = [-1, 0]
        elif position[1] > 0 and self.pos != [0, 1]:
            self.pos = [0, 1]
        elif position[1] < 0 and self.pos != [0, -1]:
            self.pos = [0, -1]
    
    def move(self):
        new_head = self.head.copy()
        new_head.x += self.pos[0] * BLOCK_SIZE
        new_head.y += self.pos[1] * BLOCK_SIZE

        if self.body:
            self.body.insert(0, new_head)
            self.head = self.body[0]
        else:
            self.head = new_head

        if not self.dead and self.body:
            self.body.pop()

    def grow(self):
        self.score += 1
        new_block = pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body.insert(0, new_block)

class Apple:
    def __init__(self):
        self.spawn()

    def spawn(self):
        ''' Spawn a new apple on the screen at a random position '''
        # Randomly spawn apple
        self.x = random.randrange(0, WIDTH, BLOCK_SIZE)
        self.y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        self.apple = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    
    def drawApple(self):
        pygame.draw.rect(SCREEN, APPLE_CLR, self.apple)

    def checkSpawn(self, snake):
        ''' Check if the apple collides with the snake. If so, respawn the apple. '''
        for square in snake.body:
            if self.apple.colliderect(square):
                self.spawn() # Respawn apple if it collides with snake
                #snake.grow()