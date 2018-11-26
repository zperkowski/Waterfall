from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)


def init():
    return fig,


def animate(i):
    ax.view_init(elev=20., azim=i)
    return fig,


def save_animation(name):
    # Animate
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=360, interval=20, blit=True)
    # Save
    anim.save(name, fps=30, extra_args=['-vcodec', 'libx264'])


if __name__ == '__main__':
    save_animation('animation.mp4')
