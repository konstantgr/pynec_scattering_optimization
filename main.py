import yaml
import ray
import numpy as np
from geometry.simple_geometries import get_cubic_geometry, my_anapole
from optimization import Optimizator


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
    return config


if __name__ == '__main__':
    ray.init(num_cpus=optimization_config['num_cpu'])

    seeds = [10, 20]
    iters = [10]

    result_ids = []
    for seed in seeds:
        optimization_config['CMA-ES']['seed'] = seed
        result_ids.append(optimize_geometries.remote(optimization_config, True))

    # for it in iters:
    #     optimization_config['CMA-ES']['iterations'] = it
    #     result_ids.append(optimize_geometries.remote(optimization_config))

    results = ray.get(result_ids)
    print(results)
