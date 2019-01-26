import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm

from utils import filter_only_water

fig = plt.figure()
ax = Axes3D(fig)

surf = None
gl_water = None
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
    global gl_water

    if len(gl_water) > i:
        water = gl_water[i]
    else:
        water = gl_water[len(gl_water) - 1]

    water = filter_only_water(water)
    wx, wy, w_bottom, wz = water
    w_width = w_depth = np.array(0.01*len(Z))
    ax.bar3d(wx, wy, w_bottom, w_width, w_depth, wz, color='b', zorder=1)

    ax.view_init(elev=20., azim=i)
    return fig,


def save_animation(map_array, l_water, name):
    global X, Y, Z, surf, gl_water
    gl_water = l_water
    X, Y, Z = map_array
    bottom = np.zeros(len(Z))
    # Todo: Find proper values
    width = depth = np.array(0.01*len(Z))
    ax.bar3d(X, Y, bottom, width, depth, Z, color='r', zorder=0)

    s_water = gl_water[0][:]
    s_water = filter_only_water(s_water)    # Show where is water
    wx, wy, w_bottom, wz = s_water
    w_width = w_depth = np.array(0.01*len(Z))

    ax.bar3d(wx, wy, w_bottom, w_width, w_depth, wz, color='b', zorder=1)

    plt.show()
    # Animate
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=frames, interval=20, blit=True)
    # Save
    anim.save(name, fps=fps, extra_args=['-vcodec', 'libx264'])
