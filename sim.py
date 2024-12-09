from world_frame import World
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

world = World(
    40,
    200,
    goal_radius=5
)

num_ticks = 50
num_epochs = 3000

grid = world.spawn_swarm()

grid_history = []

for epoch in range(num_epochs):
    for tick in range(num_ticks):
        center, radius, grid = world.tick()
        print(center)
        grid_history.append(grid > 0)

    if epoch in [1, 80, 160, 200]:
        fig, ax = plt.subplots()
        cax = ax.matshow(grid_history[0], cmap="gray")
        plt.colorbar(cax)

        def update(frame):
            cax.set_array(grid_history[frame])
            ax.set_title(f"Tick: {frame + 1}")
            return cax,

        ani = FuncAnimation(
            fig, update, frames=len(grid_history), interval=40, blit=False
        )

        plt.show()

    grid_history = []
    metrics = world.epoch_end()
    print(metrics["num_out_of_bounds"])

