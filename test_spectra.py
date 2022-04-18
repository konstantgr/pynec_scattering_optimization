import yaml
import ray
import numpy as np

from geometry import Wire, Geometry
from geometry.simple_geometries import get_cubic_geometry
from plotting_utils import scattering_plot
import matplotlib.pyplot as plt

res = np.array([0.2042, 0.4325, 0.2566, 0.2458, 0.5413, 0.4439, 0.6731, 0.4245, 0.5735]).reshape(3,3)
# res = np.array([[0.53011358, 0.66164297, 0.6993323 ],
#        [0.36413446, 0.41079286, 0.7448017 ],
#        [0.51111501, 0.43506238, 0.5869838 ]])

# res = np.array(res).reshape(3, 3)

wires = []
for i in range(3):
    for j in range(3):
        x = 0.005 * j
        y = 0.005 * i
        wire = Wire(
            point1=(x, y, -res[i][j] / 2 * 0.05),
            point2=(x, y, res[i][j] / 2 * 0.05),
            radius=0.5 * 1e-3
        )
        wires.append(wire)

g = Geometry(wires)

if __name__ == '__main__':

    fig, ax = plt.subplots()
    scat = scattering_plot(ax, g)
    print(list(scat))
    fig.show()
