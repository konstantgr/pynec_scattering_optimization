import numpy as np
import copy
from geometry import Geometry


def plane_wave(context, frequency):
    """ Excitation of plane wave on current frequency.
        This function calculate scattering when rp_card called.
    """
    # number_of_angles = 4
    # delta_angles = 360 / number_of_angles
    context.fr_card(0, 1,  frequency, 0)
    context.ex_card(1, 1, 1, 0, 0,
                    90, 90,
                    0,
                    0, 0, 0)

    # THE LONGEST PART OF PROGRAM
    # Use this if you need forward and backward scattering
    # context.rp_card(calc_mode=0, n_theta=1, n_phi=2,
    #                 output_format=1, normalization=0, D=0, A=0,
    #                 theta0=90, delta_theta=0, phi0=90, delta_phi=180,
    #                 radial_distance=0, gain_norm=0)

    # Use this if you need only forward scattering
    context.rp_card(calc_mode=0, n_theta=1, n_phi=1,
                    output_format=1, normalization=0, D=0, A=0,
                    theta0=90, delta_theta=0, phi0=270, delta_phi=0,
                    radial_distance=0, gain_norm=0)
    context.xq_card(0)  # Execute simulation
    return context


def get_scattering_in_frequency_range(geometry, frequency_range: range) -> dict:
    """ Get scattering (forward and backward in general) of wires geometry
        Wires is the array of Wire objects, frequency_range is the range,
        in which scattering will be calculated.
    """

    c_const = 299792458
    scattering_array = []
    wires = geometry.wires

    for frequency in frequency_range:
        lmbda = c_const / (frequency * 1e6)
        g = Geometry(wires)
        g.context = plane_wave(g.context, frequency)
        rp = g.context.get_radiation_pattern(0)
        scattering_db = rp.get_gain()[0][:]

        scattering = (10.0**(scattering_db / 10.0)) * lmbda**2
        scattering_array.append(scattering)

    scattering_array = np.array(scattering_array).T
    scattering_dict = {'forward': scattering_array[0]}
    return scattering_dict
