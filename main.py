import yaml
from geometry.simple_geometries import get_cubic_geometry
from optimization import Optimizator
from plotting_utils import plot_geometry_3d


with open('optimization/optimization_config.yml', "r") as yml_config:
    optimization_config = yaml.safe_load(yml_config)


if __name__ == '__main__':
    geometry = get_cubic_geometry(2 * 1e-3)
    optimizator = Optimizator(kind='CMA-ES')
    # result_geometry, result_value = optimizator.run(geometry, optimization_config['test'])
    res = optimizator.run(geometry, optimization_config['CMA-ES'])
    optimizator.save_results()

    # print(res)
    # for i in result_geometry.wires:
    #     print(i, result_value)
    # ax = plot_geometry_3d(result_geometry)
