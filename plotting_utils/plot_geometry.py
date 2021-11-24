import matplotlib.pyplot as plt
import numpy as np
from .primitives import plot_3d_cylinder


def plot_geometry_2d(geometry):
    pass


def plot_geometry_3d(ax, geometry):

    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.xaxis._axinfo['grid']['color'] = (1, 1, 1, 0)
    ax.yaxis._axinfo['grid']['color'] = (1, 1, 1, 0)
    ax.zaxis._axinfo['grid']['color'] = (1, 1, 1, 0)

    title = 'Scheme of geometry'
    ax.set_title(title, fontsize=16)

    for wire in geometry.wires:
        plot_3d_cylinder(ax, wire.radius, wire.length,
                         elevation=wire.z_1,
                         resolution=100, color='grey',
                         x_center=wire.x_1, y_center=wire.y_1)

        # ax.plot([wire.x_1, wire.x_2],
        #         [wire.y_1, wire.y_2],
        #         [wire.z_1, wire.z_2],
        #         color='k', linewidth=5)

    plt.show()
    return ax
