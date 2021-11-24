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


def my_anapole():
    tau = 30.9359 * 1e-3
    length0 = 2 * 94.2002 * 1e-3
    length1 = 2 * 27.8908 * 1e-3
    length2 = 2 * 69.451 * 1e-3
    length3 = 2 * 69.451 * 1e-3
    length4 = 2 * 17.7475 * 1e-3

    point_0 = (0, 0, length0)
    point_1 = (0, tau, length1)
    point_2 = (tau, 0, length2)
    point_3 = (-tau, 0, length3)
    point_4 = (0, -tau, length4)
    points = [point_0, point_1, point_2, point_3, point_4]

    wires = []
    i = 0
    for x, y, length in points:
        wire = Wire(
                point1=(x, y, -length / 2),
                point2=(x, y, length / 2),
                radius=1e-3
            )
        if i == 0:
            wire.conductivity = 1e2

        wires.append(wire)
        i += 1

    return Geometry(wires)
