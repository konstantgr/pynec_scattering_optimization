import yaml
import matplotlib.pyplot as plt
from geometry.simple_geometries import get_cubic_geometry, my_anapole
from optimization import Optimizator
from plotting_utils import scattering_plot


with open('optimization/optimization_config.yml', "r") as yml_config:
    optimization_config = yaml.safe_load(yml_config)


if __name__ == '__main__':
    geometry = get_cubic_geometry(2 * 1e-3)
    optimizator = Optimizator(kind='CMA-ES')
    res = optimizator.run(geometry, optimization_config['CMA-ES'])

    optimizator.plot_results(save=True)
    optimizator.save_results()
    #
    # geometry_anapole = my_anapole()
    #
    # fig, ax = plt.subplots(1)
    # scattering_plot(
    #     ax, geometry_anapole,
    #     frequency_start=200,
    #     frequency_finish=1500,
    #     step=5
    # )
    # plt.show()
