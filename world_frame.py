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
            self.robot_array[i] = robot.Robot(TOTAL_NUM_INPUT, TOTAL_NUM_OUTPUT, RESTRICTED_NUM_INPUT, NUM_NEURONS, position[0], position[1])
        return

    def tick(self):
        self.prev_grid = self.grid
        self.grid = np.zeros(shape=(self.size, self.size))
        for robot in self.robot_array:
            new_x = 0
            new_y = 0
            match robot.movment_choice():
                case 0:
                    new_x = robot.x
                    new_y = robot.y
                case 1:
                    new_x = robot.x + 1
                    new_y = robot.y
                case 2:
                    new_x = robot.x - 1
                    new_y = robot.y
                case 3:
                    new_x = robot.x
                    new_y = robot.y + 1
                case 4:
                    new_x = robot.x
                    new_y = robot.y - 1
            if new_x > self.size:
                new_x = robot.x
            if new_y > self.size:
                new_y = robot.y
        
