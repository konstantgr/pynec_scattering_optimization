import numpy as np
from geometry import Wire, Geometry


def single_wire(length, wire_radius):
    wire = Wire(
        point1=(0, 0, -length / 2),
        point2=(0, 0, length / 2),
        radius=wire_radius
    )
    return Geometry([wire])


def get_circular_geometry(radius, lengths_of_wires, wire_radius=1e-3, delta_angle=0):
    number_of_wires = len(lengths_of_wires)
    angles = np.linspace(0, 2 * np.pi, number_of_wires, endpoint=False) + delta_angle

    wires = []
    for i, length in enumerate(lengths_of_wires):
        phi = angles[i]
        wire = Wire(
            point1=(radius * np.cos(phi), radius * np.sin(phi), -length / 2),
            point2=(radius * np.cos(phi), radius * np.sin(phi), length / 2),
            radius=wire_radius
        )
        wires.append(wire)

    return Geometry(wires)


def get_cubic_geometry(tau, lengths_of_wires=np.ones((3, 3)) * 1e-3, wire_radius=0.5 * 1e-3):
    """
    length_of_wires: np.array([[0., 0., 0.],
                               [0., 0., 0.],
                               [0., 0., 0.],
                               [0., 0., 0.]])
                     is a 4x3 array, left bottom corner is (0,0) point
    """

    number_of_wires_y, number_of_wires_x = lengths_of_wires.shape
    wires = []
    for i in range(number_of_wires_y):
        for j in range(number_of_wires_x):
            x = tau * j
            y = tau * i
            wire = Wire(
                point1=(x, y, -lengths_of_wires[i][j] / 2),
                point2=(x, y, lengths_of_wires[i][j] / 2),
                radius=wire_radius
            )
            wires.append(wire)

    return Geometry(wires)
