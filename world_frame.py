import numpy as np
import robot
import random

TOTAL_NUM_INPUT = 10
TOTAL_NUM_OUTPUT = 5
RESTRICTED_NUM_INPUT = 5
NUM_NEURONS = 2

class World:
    def __init__(self, grid_size, num_robots):
        self.grid_size = grid_size
        self.grid = np.zeros(shape=(grid_size, grid_size))
        self.prev_grid = np.zeros(shape=(grid_size, grid_size))
        self.robot_array = [None] * num_robots

    def spawn_swarm(self):
        grid_positions = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)]
        for i in range(len(self.robot_array)):
            position = grid_positions.pop(random.randrange(1, len(grid_positions)))
            self.grid[position[0]][position[1]] = i
            self.robot_array[i] = robot.Robot()
        return

    def tick(self):
        self.prev_grid = self.grid
        self.grid = np.zeros(shape=(self.size, self.size))
        for robot in self.robot_array:
            