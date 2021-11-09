from PyNEC import *
import numpy as np


class Wire:
    def __init__(self, point1, point2, radius):
        self.x_1, self.y_1, self.z_1 = point1
        self.x_2, self.y_2, self.z_2 = point2
        self.radius = radius
        self.length = np.sqrt((self.x_2 - self.x_1)**2
                              + (self.y_2 - self.y_1)**2
                              + (self.z_2 - self.z_1)**2)

    def __str__(self):
        return (f'{self.x_1=}, {self.y_1=}, {self.z_1=}\n'
                + f'{self.x_2=}, {self.y_2=}, {self.z_2=}\n'
                + f'{self.length=}')


class Geometry:
    def __init__(self, wires, scale=1):
        self.wires = wires
        self.segments = 10
        self.context = self.make_context(scale)

    def make_context(self, scale=1):
        context = nec_context()
        geo = context.get_geometry()

        for idx, wire in enumerate(self.wires):
            if wire.length == 0:
                continue

            # try:
            geo.wire(idx + 1, self.segments,
                     wire.x_1, wire.y_1, wire.z_1,
                     wire.x_2, wire.y_2, wire.z_2, wire.radius, 1, 1)

            # except Exception as e:
            #     w1 = self.wires[idx-1]
            #     w2 = self.wires[idx]
            #     print(w1)
            #     print(w2)
            #     print(w1.radius)
            #     print(w1.x_1 - w2.x_1 - 2*w1.radius)
            #     print(w1.y_1 - w2.y_1 - 2*w1.radius)
            #     raise SystemExit(1)

        geo.scale(scale)
        context.geometry_complete(0)

        return context

    def to_dict(self):
        d = {}
        for idx, wire in enumerate(self.wires):
            d[f'wire{idx}'] = {'x1': wire.x_1, 'y1': wire.y_1, 'z1': wire.z_1,
                               'x2': wire.x_1, 'y2': wire.y_1, 'z2': wire.z_1,
                               'radius': wire.radius}
        return d
