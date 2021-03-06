import numpy as np
import time
import json
import matplotlib.pyplot as plt

from cmaes import CMA
from tqdm import tqdm

from geometry.simple_geometries import get_cubic_geometry
from pynec_utils import get_scattering_in_frequency_range
from plotting_utils import plot_geometry_3d, scattering_plot, plot_single_wire_scattering


class Optimizator:
    def __init__(self, kind='test', target='lengths'):
        self.optimizators_mapping = {
            'test': self.test_optimizator,
            'CMA-ES': self.cma_optimizer
        }
        self.kind = kind
        self.configs = {}
        self.best_results = {}

        self._opt = self.optimizators_mapping[kind]

        self.scat = None
        self.lengths = None
    #
    # def get_target_parameters(self, geometry, target='lengths'):
    #     return geometry
    #

    def run(self, geometry, config: dict):
        self.configs[self.kind] = config
        return self._opt(geometry, **config)

    def plot_results(self, kind=None, save=False):
        if kind is None:
            kind = self.kind

        best_geometry = self.best_results[kind]['geometry']

        fig = plt.figure(figsize=plt.figaspect(2.))
        ax = fig.add_subplot(2, 1, 2)

        scat = scattering_plot(ax, best_geometry)
        self.scat = scat

        ax = fig.add_subplot(2, 1, 1, projection='3d')
        plot_geometry_3d(ax, best_geometry)

        if save:
            s = f'{kind}__'
            for key, value in self.configs[kind].items():
                s += f'{key}_{value}__'
            filename = s.rstrip('__') + '.png'

            fig.savefig(f'data/optimization_results/images/{filename}',
                        bbox_inches='tight', dpi=150)
            print('Image saved successfully')

        plt.show()

    def save_results(self, kind=None):
        if kind is None:
            kind = self.kind

        if kind not in self.best_results.keys():
            raise Exception(f"Doesn't have results of {kind} optimizer")

        result_dict = {
            'kind': kind,
            'optimizator_config': self.configs[kind],
            'best_geometry': self.best_results[kind]['geometry'].to_dict(),
            'best_result': self.best_results[kind]['optimized_value']
        }

        s = f'{kind}__'
        for key, value in self.configs[kind].items():
            s += f'{key}_{value}__'
        filename = s.rstrip('__') + '.json'

        with open(f'data/optimization_results/configs/{filename}', 'w+') as fp:
            json.dump(result_dict, fp)
        print('Results saved successfully')

    def test_optimizator(self, geometry, value=0, iterations=1, progress_bar=True):
        rg = tqdm(range(iterations)) if progress_bar else range(iterations)
        for i in rg:
            time.sleep(0.1)

        return geometry, value

    def target_cubic(self, lengths, tau, N, fr):
        lengths = np.array(lengths).reshape(N, N)
        g = get_cubic_geometry(tau=tau, lengths_of_wires=np.array(lengths))
        forward_scattering_values = get_scattering_in_frequency_range(g, [fr])['forward']
        val = forward_scattering_values[0]

        return -val

    def cma_optimizer(
            self,
            geometry,
            tau=3 * 1e-3,
            length_limits=(0, 10*1e-3),
            iterations=200,
            seed=47,
            frequency=6400,
            sphere_radius=20 * 1e-3
    ):
        np.random.seed(seed)

        # print(length_limits, iterations, seed, frequency, sphere_radius)
        N = int(np.sqrt(len(geometry.wires)))

        if tau * (N - 1) > 2 * sphere_radius:
            raise Exception('Separation between wires (tau) too big')

        x = np.linspace(-tau * N / 2, tau * N / 2, N)
        y = np.linspace(-tau * N / 2, tau * N / 2, N)

        bounds = []
        # ??????????????, ??????????????????????, ?????? ?????? ?????????????????????? ?? ????????????
        # ???????????? ?????????????? ?????????? ??????????????????????????
        for i in range(N):
            for j in range(N):
                l = (np.sqrt(sphere_radius ** 2 - x[i] ** 2 - y[j] ** 2))
                bounds.append([length_limits[0], 2 * l])
        bounds = np.array(bounds)

        # ??????????????, ???? ??????????????????????, ?????? ?????? ?????????????????????? ?? ????????????
        # ???????????? ?????????????? ?????????? ??????????????????????????
        # bounds = np.array([[length_limits[0], length_limits[1]] for i in range(N * N)])

        lower_bounds, upper_bounds = bounds[:, 0], bounds[:, 1]
        mean = lower_bounds + (np.random.rand(N * N) * (upper_bounds - lower_bounds))
        sigma = 2 * (upper_bounds[0] - lower_bounds[0]) / 5

        optimizer = CMA(
            mean=mean,
            sigma=sigma,
            bounds=bounds,
            seed=seed,
            population_size=25
        )

        cnt = 0
        max_value = 0
        max_lengths = []

        pbar = tqdm(range(iterations))
        for generation in pbar:
            solutions = []
            for _ in range(optimizer.population_size):
                lengths = abs(optimizer.ask())
                value = self.target_cubic(
                    lengths, tau=tau,
                    N=N, fr=frequency
                )

                if abs(value) > max_value:
                    max_value = abs(value)
                    max_lengths = lengths
                    cnt += 1

                solutions.append((lengths, value))
                pbar.set_description("Processed %s generation\t max %s" % (generation, round(max_value, 5)))

            optimizer.tell(solutions)

        best_geometry = get_cubic_geometry(
            tau=tau,
            lengths_of_wires=np.array(max_lengths).reshape(N, N)
        )

        results = {
            'geometry': best_geometry,
            'optimized_value': max_value
        }
        self.best_results['CMA-ES'] = results
        self.lengths = results['geometry']

        return best_geometry, max_value
