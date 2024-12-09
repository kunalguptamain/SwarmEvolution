class Grid:
    def __init__(self, grid, prev_prefix_sum, grid_size, visibility_radius=6):
        self.grid = [i > 0 for i in grid]
        self.grid_size = grid_size
        self.prefix_sum = self.compute_prefix_sum(grid)
        self.prefix_sum_difference = self.prefix_sum - prev_prefix_sum
        self.visibility_radius = visibility_radius

    def compute_prefix_sum(self, grid):
        return grid.cumsum(axis=0).cumsum(axis=1)

    def compute_area_sum(self, prefix_array, tuple1, tuple2):
        x1, y1 = tuple1
        x2, y2 = tuple2
        total = prefix_array[x2, y2]
        if x1 > 0:
            total -= prefix_array[x1 - 1, y2]
        if y1 > 0:
            total -= prefix_array[x2, y1 - 1]
        if x1 > 0 and y1 > 0:
            total += prefix_array[x1 - 1, y1 - 1]
        return total

    def sense_peripheral_robots(self, position):
        x_pos, y_pos = position
        grid_size = self.grid_size - 1
        offset1 = self.visibility_radius
        offset2 = self.visibility_radius - 1

        quadrants = [
            ((min(x_pos + offset1, grid_size), max(y_pos - offset2, 0)),
             (min(x_pos + 1, grid_size), min(y_pos + offset2, grid_size))),
            ((max(x_pos - 1, 0), max(y_pos - offset2, 0)),
             (max(x_pos - offset1, 0), min(y_pos + offset2, grid_size))),
            ((min(x_pos + offset2, grid_size), min(y_pos + 1, grid_size)),
             (max(x_pos - offset2, 0), min(y_pos + offset1, grid_size))),
            ((min(x_pos + offset2, grid_size), max(y_pos - offset1, 0)),
             (max(x_pos - offset1, 0), max(y_pos - 1, 0))),
        ]

        return [
            self.compute_area_sum(self.prefix_sum, *q) for q in quadrants
        ] + [
            self.compute_area_sum(self.prefix_sum_difference, *q) for q in quadrants
        ]
