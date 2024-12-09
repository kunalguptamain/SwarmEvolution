class Grid:

    def __init__(
        self,
        grid,
        visibility_radius: int = 5,
    ):
        self.grid = grid
        self.prefix_sum.compute_prefix_sum() #use prefix sum function
        self.visibility_radius = visibility_radius

    def get_num_robots_forward(position: tuple):
        return None

    def compute_prefix_sum(self, grid):
        rows, cols = self.grid.shape
        prefix_sum = np.zeros_like(grid, dtype=int)
        for i in range(rows):
            for j in range(cols):
                prefix_sum[i][j] = (
                    grid[i][j]
                    + (prefix_sum[i-1][j] if i > 0 else 0)
                    + (prefix_sum[i][j-1] if j > 0 else 0)
                    - (prefix_sum[i-1][j-1] if i > 0 and j > 0 else 0)
                )
        return prefix_sum

    def compute_subarray(self, tuple1, tuple2):
        x1, y1 = tuple1
        x2, y2 = tuple2

        if (x1 - 1) < 0 and (y1-1) < 0:
            return self.prefix_sum[x2, y2]
        elif (x1 - 1) < 0:
            return self.prefix_sum[x2, y2] - self.prefix_sum[x2, y1 - 1]
        elif (y1 - 1) < 0:
            return self.prefix_sum[x2, y2] - self.prefix_sum[x1 - 1, y2]
        else:
            return self.prefix_sum[x2][y2] +
                    self.prefix_sum[x1-1] - 
                    self.prefix_sum[x1 - 1, y2] -
                    self.prefix_sum[x2, y1 - 1]

    def sense_peripheral_robots(self, position):
        data_vector = [0, 0, 0, 0]
        x_pos, y_pos = position
        
        data_vector[0] = compute_subarray((argmin(x_pos + 3, self.grid_size), argmax(y_pos - 2, 0)),
                                          (argmin(x_pos + 1, self.grid_size), argmin(y_pos + 2, self.grid_size)))
        data_vector[1] = compute_subarray((argmax(x_pos - 1, 0), argmax(y_pos - 2, 0)),
                                          (argmax(x_pos - 3, 0), argmin(y_pos + 2, self.grid_size)))
        data_vector[2] = compute_subarray((argmin(x_pos + 2, self.grid_size), argmin(y_pos + 1, self.grid_size)),
                                          (argmax(x_pos - 2, 0), argmin(y_pos + 3, self.grid_size)))
        data_vector[3] = compute_subarray((argmin(x_pos + 2, self.grid_size), argmax(y_pos - 3, 0)),
                                          (argmax(x_pos - 3, 0), argmax(y_pos - 1, 0)))

        return data_vector

