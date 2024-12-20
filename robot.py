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
        position: tuple,
    ):
        self.number_of_sensors = number_of_sensors
        self.number_of_neurons = number_of_neurons
        self.total_global_sensor_count= total_global_sensor_count
        self.total_global_output_count = total_global_output_count
        self.position = position

        self.genome = np.random.randint(0, self.total_global_sensor_count, size=self.number_of_sensors)
        self.mask = np.random.randint(0, 4, size=(self.number_of_sensors, self.number_of_neurons)) != 3
        self.mask2 = np.random.randint(0, 3, size=(self.number_of_neurons, self.total_global_output_count)) != 2
        self.internal_weights = np.random.uniform(-1, 1, size=(self.number_of_sensors, self.number_of_neurons))
        self.internal_weights[self.mask] = 0
        self.output_weights = np.random.uniform(-1, 1, size=(self.number_of_neurons, self.total_global_output_count))
        self.output_weights[self.mask2] = 0

    @classmethod
    def clone(
        cls,
        total_global_sensor_count: int,
        total_global_output_count: int,
        number_of_sensors: int, # how many sensors is the robot restricted to 
        number_of_neurons: int, # how many neurons is the robot restricted to
        position: tuple,
        genome: np.ndarray,
        internal_weights: np.ndarray,
        output_weights: np.ndarray,
        mask: np.ndarray,
    ):
        # Create an instance without random initialization
        instance = cls(
            total_global_sensor_count,
            total_global_output_count,
            number_of_sensors,
            number_of_neurons,
            position,
        )
        # Manually set the genome and weights
        instance.genome = genome
        instance.internal_weights = internal_weights
        instance.output_weights = output_weights
        instance.mask = mask

        return instance
    
    def get_mask(self):
        return self.mask
    
    def get_internal_weights(self):
        return self.internal_weights
    
    def get_output_weights(self):
        return self.output_weights

    def set_position(self, position):
        self.position = position

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
        self.internal_weights[self.mask] = 0

        #normalization of output weights to prevent domincance
        row_norms = np.linalg.norm(self.output_weights, axis=1, keepdims=True)
        row_norms[row_norms == 0] = 1
        self.output_weights /= row_norms

        self.output_weights = np.clip(self.output_weights, -1, 1)
        self.output_weights[self.mask2] = 0

    def movment_choice(
        self,
        sensor_input_vector, # a vector in order of the sensor's in the robot's genome of the sensor outputs
    ):
        internal_state = self.internal_weights.T @ sensor_input_vector
        output_state = internal_state.T @ self.output_weights
        return np.argmax(output_state)
