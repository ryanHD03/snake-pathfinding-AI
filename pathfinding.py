from settings import *
from queue import Queue
from snake import create_duplicate_snake, deepcopy
from random import randrange

def get_neighbours(position):
    '''
    Get neighbouring positions from the current position
    
    Args:
        - position: Tuple representing the current position (x, y)
    Returns:
        - List of neighbouring positions
    '''

    neighbours = [[position[0] + BLOCK_SIZE, position[1]],
                      [position[0] - BLOCK_SIZE, position[1]],
                      [position[0], position[1] + BLOCK_SIZE],
                      [position[0], position[1] - BLOCK_SIZE]]
    
    neighbours_within_grid = []
    for pos in neighbours:
        if pos in GRID:
            neighbours_within_grid.append(pos)

    return neighbours_within_grid

def get_available_neighbours(snake, position, apple_pos):
    valid_neighbours = []
    neighbours = get_neighbours(position)
    for neighbour in neighbours:
        if is_position_available(snake, neighbour) and apple_pos != neighbour:
            valid_neighbours.append(neighbour)
    return valid_neighbours

def is_position_available(snake, position):
    if (0 <= position[0] <= ROWS or 0 <= position[1] <= ROWS) and position not in snake.body:
        return True
    return False

def distance(position1, position2):
    x1, x2 = position1[0], position2[0]
    y1, y2 = position1[1], position2[1]
    return abs(x2 - x1) + abs(y2 - y1)
    

def longest_path_to_tail(snake, apple_pos):
    neighbours = get_available_neighbours(snake, (snake.head.x, snake.head.y), apple_pos)
    path = []
    if neighbours:
        d = -9999
        for neighbour in neighbours:
            tail_pos = (snake.tail.x, snake.tail.y)
            if distance(neighbour, tail_pos) > d:
                dup_snake = create_duplicate_snake(snake)
                dup_snake.go_to(neighbour)
                dup_snake.move()
            if dup_snake.head.x == apple_pos[0] and dup_snake.head.y == apple_pos[1]:
                dup_snake.grow()
            if path_to_tail(dup_snake):
                path.append(neighbour)
                d = distance(neighbour, tail_pos)
        if path:
            return [path[-1]]
        
def find_safe_move(snake, apple_pos):
    neighbours = get_available_neighbours(snake, (snake.head.x, snake.head.y), apple_pos)
    path = []
    if neighbours:
        path.append(neighbours[randrange(len(neighbours))])
        dup_snake = create_duplicate_snake(snake)
        for move in path:
            dup_snake.go_to(move)
            dup_snake.move()
        if path_to_tail(dup_snake):
            return path
        else:
            return path_to_tail(snake)
        
def BFS(start_pos, target_pos, snake_body):
    '''
    Perform Breadth-First Search (BFS) to find the shortest path from the snake's head to the apple
    
    Args:
        - start_pos: Tuple representing the starting position (snake's head)
        - target_pos: Tuple representing the target position (apple)
        - snake_body: List representing the coordinates of the snake's body
    Returns:
        - List representing the sequence of moves to the apple as a list of tuples (coordinates)
    '''
    
    queue = Queue()
    queue.put((start_pos, [])) # Initialize queue with snake's head position and empty path

    visited = set()
    visited.add(start_pos)

    while not queue.empty():
        current_pos, path = queue.get()

        # Return path if apple is found
        if current_pos == target_pos:
            return path # Sequence of moves towards the apple
        
        # Explore neighbours
        neighbours = get_neighbours(current_pos)
        for neighbour in neighbours:
            if is_position_safe(snake_body, tuple(neighbour)) and tuple(neighbour) not in visited:
            #if tuple(neighbour) not in snake_body and tuple(neighbour) not in visited:
                direction = [neighbour[0] - current_pos[0], neighbour[1] - current_pos[1]]
                visited.add(tuple(neighbour))
                new_path = path + [tuple(direction)]
                queue.put((tuple(neighbour), new_path))
                
    return [] # If no path is found

def is_position_safe(snake_body, position):
    if position[0] < 0 or position[0] >= WIDTH or position[1] < 0 or position[1] >= HEIGHT:
        return False
    for square in snake_body:
        if position == (square.x, square.y):
            return False
    return True

def set_path(snake, apple):
    apple_pos = (apple.apple.x, apple.apple.y)
    snake_head_pos = (snake.head.x, snake.head.y)
    if snake.score == SNAKE_MAX_LEN - 1 and apple_pos in get_neighbours(snake_head_pos):
        winning_path = [apple_pos]
        return winning_path
    
    duplicate_snake = create_duplicate_snake(snake)
    dup_head_pos = (duplicate_snake.head.x, duplicate_snake.head.y)

    initial_path = BFS(dup_head_pos, apple_pos, duplicate_snake.body)
    secondary_path = []
    #print(f"Score: {snake.score}")
    if initial_path:
        for position in initial_path:
            duplicate_snake.go_to(position)
            duplicate_snake.move()
        duplicate_snake.grow()
        secondary_path = path_to_tail(duplicate_snake)
    if secondary_path:
        #print(f"Initial path: {initial_path}")
        return initial_path
    if longest_path_to_tail(snake, apple_pos) and snake.score % 2 == 0:
        #print(f"Longest Path to Tail: {longest_path_to_tail(snake, apple_pos)}")
        return longest_path_to_tail(snake, apple_pos)
    if find_safe_move(snake, apple_pos):
        #print(f"Find safe move: {find_safe_move(snake, apple_pos)}")
        return find_safe_move(snake, apple_pos)
    if path_to_tail(snake):
        #print(f"Path to tail: {path_to_tail(snake)}")
        return path_to_tail(snake)
    print("snake is in danger")

def path_to_tail(snake):
    body_len = len(snake.body)
    tail_pos = deepcopy(snake.tail)
    #print(f"Tail Position: {tail_pos}")
    if len(snake.body) > 1:
        snake.tail = snake.body.pop(-1)
    #print(tail_pos)
    head_pos = (snake.head.x, snake.head.y)
    snake_tail_pos = (tail_pos.x, tail_pos.y)
    path = BFS(head_pos, (snake_tail_pos), snake.body)

    if len(snake.body) < body_len:
        snake.body.append(snake.tail)
        snake.tail = snake.body[-1]

    return path