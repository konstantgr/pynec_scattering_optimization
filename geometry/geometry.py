from PyNEC import *
import numpy as np


class Wire:
    def __init__(self, point1, point2, radius, conductivity=None):
        self.x_1, self.y_1, self.z_1 = point1
        self.x_2, self.y_2, self.z_2 = point2
        self.radius = radius
        self.length = np.sqrt((self.x_2 - self.x_1) ** 2
                              + (self.y_2 - self.y_1) ** 2
                              + (self.z_2 - self.z_1) ** 2)
        self.conductivity = None

    def __str__(self):
        return (f'{self.x_1=}, {self.y_1=}, {self.z_1=}\n'
                + f'{self.x_2=}, {self.y_2=}, {self.z_2=}\n'
                + f'{self.length=}')


class Geometry:
    def __init__(self, wires, scale=1):
        self.wires = wires
        self.segments = 10
        self.context = self.make_context(scale)

    def set_wire_conductivity(self, context, conductivity, wire_tag=None):
        """ The conductivity is specified in mhos/meter. Currently all segments of a wire are set. If wire_tag is
        None, all wire_tags are set (i.e., a tag of 0 is used). """
        if wire_tag is None:
            wire_tag = 0

        context.ld_card(5, wire_tag, 0, 0, conductivity, 0, 0)
        # return context

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

        geo.scale(scale)
        context.geometry_complete(0)

        # if hasattr(wire, 'conductivity') and wire.conductivity is not None:
        #     context = self.set_wire_conductivity(context, 0, 1)
        return context

    def to_dict(self):
        d = {}
        for idx, wire in enumerate(self.wires):
            d[f'wire{idx}'] = {'x1': wire.x_1, 'y1': wire.y_1, 'z1': wire.z_1,
                               'x2': wire.x_1, 'y2': wire.y_1, 'z2': wire.z_1,
                               'radius': wire.radius}
        return d
