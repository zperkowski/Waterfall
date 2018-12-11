import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm

fig = plt.figure()
ax = Axes3D(fig)

surf = None
frames = 60
fps = 30
# Todo: Find why this total time works only with values 60 frames and 30 fps
progress_bar = None


def init():
    global progress_bar
    progress_bar = tqdm(total=frames*fps+fps)
    ax.set_zlim(np.min(Z) * 0.95, np.max(Z) * 1.05)
    return fig,


def animate(i):
    progress_bar.update(i+1)
    ax.view_init(elev=20., azim=i)
    return fig,


def save_animation(map_array, name):
    global X, Y, Z, surf
    X, Y, Z = map_array
    bottom = np.zeros(len(Z))
    width = depth = np.ones(len(Z))

    ax.bar3d(X, Y, bottom, width, depth, Z)
    plt.show()
    # Animate
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=frames, interval=20, blit=True)
    # Save
    anim.save(name, fps=fps, extra_args=['-vcodec', 'libx264'])
