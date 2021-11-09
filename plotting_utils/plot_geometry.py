import matplotlib.pyplot as plt
import numpy as np
from .primitives import plot_3d_cylinder

def plot_geometry_2d(geometry):
    pass


def plot_geometry_3d(geometry):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for wire in geometry.wires:
        plot_3d_cylinder(ax, wire.radius, wire.length,
                         elevation=wire.z_1,
                         resolution=100, color='k',
                         x_center=wire.x_1, y_center=wire.y_1)

        # ax.plot([wire.x_1, wire.x_2],
        #         [wire.y_1, wire.y_2],
        #         [wire.z_1, wire.z_2],
        #         color='k', linewidth=5)

    plt.show()
    return ax
