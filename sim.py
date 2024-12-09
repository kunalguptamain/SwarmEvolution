from world_frame import World
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

world = World(
    50,
    100,
    goal_radius=5
)

num_ticks = 140
num_epochs = 1001

grid = world.spawn_swarm()

grid_history = []

for epoch in range(num_epochs):
    for tick in range(num_ticks):
        center, radius, grid = world.tick()
        if epoch == 0 and tick == 0: print(center)
        if epoch in [0, 80, 160, 400, 800, 1000]:
            grid_history.append(grid > 0)

    if epoch in [0, 80, 160, 400, 800, 1000]:
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

