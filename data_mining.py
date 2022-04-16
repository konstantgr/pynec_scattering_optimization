import yaml
import ray
import numpy as np
from geometry.simple_geometries import get_cubic_geometry, my_anapole
from optimization import Optimizator
import json


with open('optimization/optimization_config.yml', "r") as yml_config:
    optimization_config = yaml.safe_load(yml_config)


@ray.remote
def optimize_geometries(config, save=False):
    geometry = get_cubic_geometry(2 * 1e-3, np.ones((4, 4)) * 1e-3)
    optimizator = Optimizator(kind='CMA-ES')
    res = optimizator.run(geometry, config['CMA-ES'])

    optimizator.plot_results(save=save)
    if save:
        optimizator.save_results()

    out = {
        "spectra": list(optimizator.scat),
        "lengths": [i.length for i in optimizator.lengths.wires]
    }

    return out


if __name__ == '__main__':
    ray.init(num_cpus=optimization_config['num_cpu'])
    np.random.seed(1)

    resonance_frequencies = np.random.randint(5000, 6000, 10)
    result_ids = []
    for freq in resonance_frequencies:
        optimization_config['CMA-ES']['frequency'] = int(freq)
        result_ids.append(optimize_geometries.remote(optimization_config, False))

    results = ray.get(result_ids)
    with open('data/optimization_results/databases/spectra_geometries.json', 'w') as fout:
        json.dump(results, fout)
