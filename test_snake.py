import unittest
import pygame
from snake import Snake, Apple  # Make sure the Snake and Apple classes are imported correctly
from settings import *

class TestSnakeGame(unittest.TestCase):
    
    def setUp(self):
        pygame.init()
        self.snake = Snake()
        self.apple = Apple()

    def tearDown(self):
        pygame.quit()

    def test_initial_state(self):
        # Test initial snake position
        self.assertEqual(self.snake.head.x, 0)
        self.assertEqual(self.snake.head.y, 0)
        # Test initial snake length
        self.assertEqual(len(self.snake.body), 0)

    def test_movement(self):
        # Test snake movement to the right
        self.snake.pos = [1, 0]
        self.snake.drawSnake()
        self.assertEqual(self.snake.head.x, BLOCK_SIZE)
        self.assertEqual(self.snake.head.y, 0)

        # Test snake movement left
        self.snake.pos = [-1, 0]
        self.snake.drawSnake()
        self.assertEqual(self.snake.head.x, 0)
        self.assertEqual(self.snake.head.y, 0)

        # Test snake movement downwards
        self.snake.pos = [0, -1]
        self.snake.drawSnake()
        self.assertEqual(self.snake.head.x, 0)
        self.assertEqual(self.snake.head.y, -50)

        # Test snake movement upwards
        self.snake.pos = [0, 1]
        self.snake.drawSnake()
        self.assertEqual(self.snake.head.x, 0)
        self.assertEqual(self.snake.head.y, 0)

    def test_apple_spawn(self):
        # Test apple spawning within the grid
        self.apple.spawn()
        self.assertTrue(0 <= self.apple.apple.x < WIDTH)
        self.assertTrue(0 <= self.apple.apple.y < HEIGHT)
        self.assertEqual(self.apple.apple.width, BLOCK_SIZE)
        self.assertEqual(self.apple.apple.height, BLOCK_SIZE)

    def test_eating_apple(self):
        # Place apple directly in front of the snake
        self.apple.apple.x = self.snake.head.x + BLOCK_SIZE
        self.apple.apple.y = self.snake.head.y
        self.snake.pos = [1, 0]
        self.snake.drawSnake()

        # Simulate snake eating the apple
        if self.snake.head.colliderect(self.apple.apple):
            self.snake.body.append(pygame.Rect(self.snake.head.x, self.snake.head.y, BLOCK_SIZE, BLOCK_SIZE))
            self.apple.spawn()

        self.assertEqual(len(self.snake.body), 1)
        self.assertNotEqual((self.apple.apple.x, self.apple.apple.y), (self.snake.head.x, self.snake.head.y))

    def test_collision_with_wall(self):
        # Move snake to the right until it hits the wall
        self.snake.pos = [-1, 0]
        self.snake.drawSnake()
        self.snake.pos = [-1, 0]
        self.snake.drawSnake()
        self.assertTrue(self.snake.dead)

    def test_collision_with_self(self):
        # Create a situation where the snake will collide with itself
        self.snake.body = [
            pygame.Rect(WIDTH / 2, HEIGHT / 2, BLOCK_SIZE, BLOCK_SIZE),
            pygame.Rect(WIDTH / 2 - BLOCK_SIZE, HEIGHT / 2, BLOCK_SIZE, BLOCK_SIZE),
            pygame.Rect(WIDTH / 2 - 2 * BLOCK_SIZE, HEIGHT / 2, BLOCK_SIZE, BLOCK_SIZE)
        ]
        self.snake.pos = [1, 0]
        self.snake.drawSnake()  # Move right
        self.snake.pos = [0, -1]
        self.snake.drawSnake()  # Move up
        self.snake.pos = [-1, 0]
        self.snake.drawSnake()  # Move left (collide with body)
        self.assertTrue(self.snake.dead)

if __name__ == '__main__':
    unittest.main()
