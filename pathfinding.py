from settings import *
from queue import Queue

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
        
def BFS(snake, apple, current_direction):
    '''
    Perform Breadth-First Search (BFS) to find the shortest path from the snake's head to the apple
    
    Args:
        - snake: Snake object
        - apple: Apple object
        - current direction: Tuple representing current direction of the snake (x, y)
    Returns:
        - List representing the sequence of moves to the apple'''
    
    queue = Queue()
    head_pos = (snake.head.x, snake.head.y)
    apple_pos = (apple.apple.x, apple.apple.y)
    queue.put((head_pos, [])) # Initialize queue with snake's head position and empty path

    visited = set()
    visited.add(head_pos)

    while not queue.empty():
        current_pos, path = queue.get()

        # Return path if apple is found
        if current_pos == apple_pos:
            return path # Sequence of moves towards the apple
        
        # Explore neighbours
        neighbours = get_neighbours(current_pos)
        for neighbour in neighbours:
            if neighbour not in snake.body:
                direction = [neighbour[0] - current_pos[0], neighbour[1] - current_pos[1]]
                if direction != [-current_direction[0], -current_direction[1]]:
                    if tuple(neighbour) not in visited:
                        visited.add(tuple(neighbour))
                        new_path = path + direction
                        queue.put((tuple(neighbour), new_path))
    return [] # If no path is found