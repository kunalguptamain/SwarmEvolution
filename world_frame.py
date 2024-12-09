import numpy as np
from robot import Robot
import random
from typing import List
from grid import Grid

TOTAL_NUM_INPUT = 10
TOTAL_NUM_OUTPUT = 5
RESTRICTED_NUM_INPUT = 9
NUM_NEURONS = 12

class World:
    def __init__(self, grid_size, num_robots, goal_radius = 12):
        self.num_robots = num_robots
        self.grid_size = grid_size
        self.grid = np.zeros(shape=(grid_size, grid_size), dtype=np.int16)
        self.prev_prefix_grid = np.zeros(shape=(grid_size, grid_size), dtype=np.int16)
        self.robot_array: List[Robot] = [None] * (num_robots + 1) # no robot in the first index
        self.goal_radius = goal_radius 
        self.goal_center = (random.randrange(self.goal_radius, self.grid_size - self.goal_radius),
                            random.randrange(self.goal_radius, self.grid_size - self.goal_radius))
        self.tick_count = 0
        

    def spawn_swarm(self):
        grid_positions = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)]
        for i in range(1, len(self.robot_array)):
            position = grid_positions.pop(random.randrange(1, len(grid_positions)))
            self.grid[position[0]][position[1]] = i
            self.robot_array[i] = Robot(TOTAL_NUM_INPUT, TOTAL_NUM_OUTPUT, RESTRICTED_NUM_INPUT, NUM_NEURONS, position)
        return self.grid

    def get_new_position(self, robot_movement_choice: int, current_position: tuple):
        x_change = [0, 1, -1, 0, 0]
        y_change = [0, 0, 0, 1, -1]

        new_x = current_position[0] + x_change[robot_movement_choice]
        new_y = current_position[1] + y_change[robot_movement_choice]
    
        if new_x >= self.grid_size or new_x < 0:
            new_x = current_position[0]
        if new_y >= self.grid_size or new_y < 0:
            new_y = current_position[1]

        return (new_x, new_y)

    def tick(self):
        self.tick_count += 1
        sensor_grid = Grid(self.grid, self.prev_prefix_grid, self.grid_size)
        self.grid = np.zeros(shape=(self.grid_size, self.grid_size), dtype=np.int16)
        for id in range(1, len(self.robot_array)):
            if self.robot_array[id] is None: continue

            robot: Robot = self.robot_array[id]

            sensor_vector = sensor_grid.sense_peripheral_robots(robot.get_position())

            sensor_vector.append(1 if robot.position[0] > (self.goal_center[0] + self.goal_radius) or \
                                robot.position[0] < (self.goal_center[0] - self.goal_radius) or \
                                robot.position[1] > (self.goal_center[1] + self.goal_radius) or  \
                                robot.position[1] < (self.goal_center[1] - self.goal_radius) else 0)

            new_position = self.get_new_position(robot.movment_choice(sensor_vector), robot.get_position()) #TODO: insert movement choice

            # if self.grid[new_position[0], new_position[1]] != 0:
            #     #self.robot_array[id] = None
            #     self.robot_array[self.grid[new_position[0], new_position[1]]] = None
            #     self.grid[new_position[0], new_position[1]] = 0
            #      # TODO: Change if we only want one to die

            self.grid[new_position[0], new_position[1]] = id
            robot.set_position(new_position)
        self.prev_prefix_grid = sensor_grid.prefix_sum

        return self.goal_center, self.goal_radius, self.grid

    def epoch_end(self):
        self.tick_count = 0
        condensed_robot_array = [robot for robot in self.robot_array if robot]

        #select the population
        # self.goal_center = (random.randrange(self.goal_radius, self.grid_size - self.goal_radius),
        #                random.randrange(self.goal_radius, self.grid_size - self.goal_radius))
        
        num_out_of_bounds = 0
        for id in range(len(condensed_robot_array)):
            robot = condensed_robot_array[id]
            if  robot.position[0] > (self.goal_center[0] + self.goal_radius) or \
                robot.position[0] < (self.goal_center[0] - self.goal_radius) or \
                robot.position[1] > (self.goal_center[1] + self.goal_radius) or  \
                robot.position[1] < (self.goal_center[1] - self.goal_radius):
                condensed_robot_array[id] = None
                num_out_of_bounds += 1


        condensed_robot_array = [robot for robot in condensed_robot_array if robot]
        alive_robots = len(condensed_robot_array)

        i = 0
        #build up the population
        while len(condensed_robot_array) < self.num_robots:
            robot: Robot = condensed_robot_array[i]
            cloned_genome = robot.get_genome()
            cloned_internal_weights = robot.get_internal_weights()
            cloned_output_weights = robot.get_output_weights()
            mask = robot.get_mask()
            condensed_robot_array.append(robot.clone(TOTAL_NUM_INPUT, TOTAL_NUM_OUTPUT, 
                                                     RESTRICTED_NUM_INPUT, NUM_NEURONS, 
                                                     (0,0), cloned_genome, cloned_internal_weights,
                                                     cloned_output_weights, mask))
            i = i + 1
        self.robot_array = condensed_robot_array

        #mutate
        for peng in self.robot_array:
            peng.mutate_genome(0.01) #TODO: global mutation
            peng.mutate_weights(0.5, 0.02) 

        #assign new positions
        grid_positions = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)]
        for i in range(1, len(self.robot_array)):
            position = grid_positions.pop(random.randrange(1, len(grid_positions)))
            self.grid[position[0]][position[1]] = i
            self.robot_array[i].position = (position)
    
        return {
            "alive_robots": alive_robots,
            "num_out_of_bounds": num_out_of_bounds
        }