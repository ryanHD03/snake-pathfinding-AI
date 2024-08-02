import pygame
from snake import Apple, Snake
from pathfinding import set_path, is_position_safe
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

def update(snake, apple):
    apple.drawApple()
    path = set_path(snake, apple)
    if path:
        snake.go_to(path[0])
    snake.move()

    pygame.draw.rect(SCREEN, SNAKE_CLR, snake.head)

    for square in snake.body[1:]:
        if snake.head.x == square.x and snake.head.y == square.y:
            snake.dead = True
        if snake.head.x <= -1 or snake.head.x >= WIDTH or snake.head.y <= -1 or snake.head.y >= HEIGHT:
            snake.dead = True
    if snake.dead:
        #main()
        pygame.time.wait(30000)

    if len(snake.body) < 1:
        # If snake's body is empty, add a new block after the head
        new_block = pygame.Rect(snake.head.x, snake.head.y, BLOCK_SIZE, BLOCK_SIZE)
        snake.body.append(new_block)
    else:
        # Draw and update all body segments
        for square in snake.body:
            pygame.draw.rect(SCREEN, SNAKE_CLR, square)

    apple_pos = (apple.apple.x, apple.apple.y)
    if snake.head.x == apple_pos[0] and snake.head.y == apple_pos[1]:
        apple.spawn()  # Respawn apple
        while not is_position_safe(snake.body, (apple.apple.x, apple.apple.y)):
            apple.spawn()
        # Add a new block after the current head position
        snake.grow()
        
def main():
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('timesnewroman', BLOCK_SIZE * 2)
    score = font.render("1", True, "white")
    score_rect = score.get_rect(center = (WIDTH / 2, HEIGHT / 20)) # Position score at the top center

    drawGrid()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        running = handle_events()
        SCREEN.fill(SURFACE_CLR)
        drawGrid()

        update(snake, apple)
                
        clock.tick(FPS)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()