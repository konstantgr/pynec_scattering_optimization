import numpy as np

from pynec_utils.scattering import get_scattering_in_frequency_range
from geometry import Wire, Geometry


def get_single_channel_limit(frequency, scattering):
    # MHz -> Hz -> lam in m^2
    lam = 299_792_458 / (frequency * 1e6)
    single_channel = lam ** 2 * 3 / (2 * np.pi)
    print(single_channel.max())
    scattering /= single_channel

    return frequency, scattering


def scattering_plot(
        ax,
        geometry,
        frequency_start=2000,
        frequency_finish=12000,
        step=20):

    num_points = 100
    step = (frequency_finish - frequency_start) // num_points
    frequency_range = range(frequency_start,
                            frequency_finish + step,
                            step)

    scattering = get_scattering_in_frequency_range(geometry, frequency_range)['forward']

    # if sgl:
    #     frequency_range, scattering = get_single_channel_limit(np.array(frequency_range), scattering)

    if ax:
        title = 'Scattering'
        ax.set_title(title, fontsize=16)
        ax.set_xlabel('Frequency (MHz)', fontsize=16)
        ax.set_ylabel('Scattering', fontsize=16)
        ax.axvline(frequency_range[np.argmax(scattering)], color='grey', alpha=0.5)
        ax.plot(frequency_range, scattering, label='PyNEC')

    return scattering


def plot_single_wire_scattering(ax, length):
    wire = Wire(
        point1=(0, 0, -length / 2),
        point2=(0, 0, length / 2),
        radius=0.5 * 1e-3
    )

    g = Geometry([wire])
    scattering_plot(ax, g)

