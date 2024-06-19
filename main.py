import pygame
from snake import Apple, Snake
from pathfinding import BFS
from settings import *

def drawGrid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, GRID_CLR, rect, 1)

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def update_snake_direction(snake, path):
    ''' Extract moves from the path and update snake's direction '''
    if path:
        next_x, next_y = path[0], path[1]
        if next_x > 0 and snake.pos != [-1, 0]:
            snake.pos = [1, 0]
        elif next_x < 0 and snake.pos != [1, 0]:
            snake.pos = [-1, 0]
        elif next_y > 0 and snake.pos != [0, 1]:
            snake.pos = [0, 1]
        elif next_y < 0 and snake.pos != [0, -1]:
            snake.pos = [0, -1]
            
        # Remove the current move pair from the path
        path = path[2:]
    return path


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
        running = handle_events()

        path = BFS(snake, apple, snake.pos)
        path = update_snake_direction(snake, path)
        
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

if __name__ == "__main__":
    main()