import numpy as np
import random
class Robot:
    # will output 
    def __init__(
        self,
        total_global_sensor_count: int, # how many total types of sensors are there
        total_global_output_count: int, # how many ouputs can a robot do (forward, backwards, etc.)
        number_of_sensors: int, # how many sensors is the robot restricted to 
        number_of_neurons: int, # how many neurons is the robot restricted to
        x: int,
        y: int,
    ):
        self.number_of_sensors = number_of_sensors
        self.number_of_neurons = number_of_neurons
        self.total_global_sensor_count= total_global_sensor_count
        self.total_global_output_count = total_global_output_count
        self.position = (x, y)

        self.genome = np.random.randint(0, self.total_global_sensor_count, size=self.number_of_sensors)
        self.internal_weights = np.random.uniform(-1, 1, size=(self.number_of_sensors, self.number_of_neurons))
        self.output_weights = np.random.uniform(-1, 1, size=(self.number_of_neurons, self.total_global_output_count))

    def set_position(self, x, y):
        self.position = (x, y)

    def get_position(self):
        return self.position

    def get_genome(self):
        # returns genome of size number_of_sensors
        # position value will between inclusive 0 to total_global_sensor_count - 1
        return self.genome
    
    def mutate_genome(
        self,
        mutation_rate: float # between 0 and 1
    ):
        mutated = np.random.rand(self.number_of_sensors) < mutation_rate
        self.genome[mutated] = np.random.randint(0, self.total_global_sensor_count, size=mutated.sum())

    def mutate_weights(
        self,
        mutation_rate: float, # between 0 and 1
        change_range: float, # if it mutates, what's its learning rate
    ):
        inner_mutated = np.random.uniform(size=(self.number_of_sensors, self.number_of_neurons)) < mutation_rate
        outer_mutated = np.random.uniform(size=(self.number_of_neurons, self.total_global_output_count)) < mutation_rate

        self.internal_weights[inner_mutated] += np.random.uniform(-change_range, change_range, size=np.sum(inner_mutated))
        self.output_weights[outer_mutated] += np.random.uniform(-change_range, change_range, size=np.sum(outer_mutated))

        self.internal_weights = np.clip(self.internal_weights, -1, 1)

        #normalization of output weights to prevent domincance
        row_norms = np.linalg.norm(self.output_weights, axis=1, keepdims=True)
        row_norms[row_norms == 0] = 1
        self.output_weights /= row_norms

        self.output_weights = np.clip(self.output_weights, -1, 1)

    def movment_choice(
        self,
        sensor_input_vector, # a vector in order of the sensor's in the robot's genome of the sensor outputs
    ):
        internal_state = self.internal_weights.T @ sensor_input_vector
        output_state = internal_state.T @ self.output_weights
        return np.argmax(output_state)
    
robot = Robot(10, 5, 5, 2, 0, 0)
robot.mutate_weights(0.5, 0.2)