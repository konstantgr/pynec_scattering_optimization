import ray
import numpy as np

from geometry import Wire, Geometry
import json

from plotting_utils import scattering_plot

N = 4
R_MAX = 0.025
POSSIBLE_LENGTHS = np.linspace(0.001, 0.025, 20)
WIRE_RADIUS = 0.5 * 1e-3


def get_random_length(x, y):
    tmp = max(abs(x), abs(y))
    max_length = 2 * np.sqrt(R_MAX**2 - tmp**2)
    max_index = np.argmin(np.array(
        [max_length - le for le in POSSIBLE_LENGTHS if max_length - le > 0])
    )
    len_num = np.random.randint(0, max_index + 1)

    return POSSIBLE_LENGTHS[len_num]


def get_random_wires(a, tau):
    x0, y0 = -a/2, -a/2

    wires = []
    for i in range(N):
        for j in range(N):
            x = x0 + tau * j
            y = y0 + tau * i
            length = get_random_length(x, y)
            wire = Wire(
                point1=(x, y, -length / 2),
                point2=(x, y, length / 2),
                radius=WIRE_RADIUS
            )
            wires.append(wire)

    return wires


@ray.remote
def get_random_geometry(i, save=False):
    print(f'===={i}====')
    alpha = np.random.uniform(0.5, 0.95)
    a = np.sqrt(2) * alpha * R_MAX
    tau = (a - 2 * WIRE_RADIUS) / (N - 1)
    wires = get_random_wires(a, tau)

    geometry = Geometry(wires)
    scat = scattering_plot(None, geometry)

    out = {
        "spectra": list(scat),
        "lengths": [i.length for i in geometry.wires]
    }

    return out


if __name__ == '__main__':
    ray.init(num_cpus=2)
    np.random.seed(1)

    samples_count = 100
    result_ids = []
    for i in range(samples_count):
        result_ids.append(get_random_geometry.remote(i))

    results = ray.get(result_ids)
    with open('data/optimization_results/databases/spectra_geometries_uniform_2.json', 'w') as fout:
        json.dump(results, fout)
