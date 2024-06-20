## Snake Game with Pathfinding

This project implements the Snake game using Python and Pygame library. The Snake moves around the screen, eating apples to grow longer. The game ends if the Snake collides with itself or with the screen's boundaries.

# Features
- Snake movement: The Snake moves around the screen based on a predefined pathfinding algorithm (BFS).
- Apple spawning: Apples spawn randomly on the screen for the Snake to eat.
- Collision detection: Detects when the Snake collides with itself or the screen's boundaries.
- Pathfinding: Implements Breadth-First Search (BFS) algorithm to find the shortest path from the Snake to the nearest Apple.

# Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/snake-game.git
2. Install dependencies:
   pip install pygame
3. Run the game:
   python main.py

# Usage
  - The snake will automatically find the shortest path to the nearest apple using the BFS algorithm.

# Tests
  - To run unit tests:
    python -m unittest test_snake.py
