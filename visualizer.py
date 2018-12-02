import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)

surf = None


def init():
    ax.set_zlim(np.min(Z) * 0.95, np.max(Z) * 1.05)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    return fig,


def animate(i):
    ax.view_init(elev=20., azim=i)
    return fig,


def save_animation(map_array, name):
    global X, Y, Z, surf
    X, Y, Z = map_array
    X, Y = np.meshgrid(X, Y)
    Z = np.array([Z])
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet, linewidth=1, antialiased=True)
    # Animate
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=360, interval=20, blit=True)
    # Save
    anim.save(name, fps=30, extra_args=['-vcodec', 'libx264'])


if __name__ == '__main__':
    save_animation('animation.mp4')
