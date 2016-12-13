"""
Noise Temperature, Antenna dipping.
Jose Vines
"""

import matplotlib.pyplot as plt
import scipy as sp
from scipy import array, linspace, log, poly1d, polyfit, radians, sin
from scipy.optimize import curve_fit


"""
Se hace el fit de antenna dipping.
"""


def model_line(x, m, n):
    model = m * x + n
    return model


def noise_temp(thot, tcold, whot, wcold):
    gamma = whot / wcold
    noise_temp = (thot - gamma * tcold) / (gamma - 1)
    return noise_temp


if __name__ == '__main__':

    # HOT-COLD test.

    whot = 0.08996
    wcold = 0.057916

    amb_temp = sp.arange(20, 30, 0.5) + 273
    nitrogen_temp = sp.arange(66, 90, 1)

    info = "Ambient temp = {} C\tnitrogen temp = {} K\ttemp noise = {} K"

    possible_temps = list()
    for amb in amb_temp:
        for nit in nitrogen_temp:
            noise_t = noise_temp(amb, nit, whot, wcold)
            if noise_t >= 300. and noise_t <= 320.:
                possible_temps.append((noise_t, amb, nit))
                # print(info.format(amb - 273, nit, noise_t))

    results = max(possible_temps)
    print(info.format(results[1], results[2], results[0]))

    # Antenna Dipping.

    w_amb = 0.089842

    elevation = sp.array(
        [4.99, 5.47, 6.04, 6.76, 7.66,
         8.85, 10.48, 12.84, 16.6, 23.5]
    )

    power = w_amb - sp.array(
        [0.08863, 0.088414, 0.088371, 0.088034,
         0.087341, 0.086716, 0.08575, 0.084052, 0.08121, 0.046278]
    )

    elevation_rad = radians(elevation)
    elevation_inv = 1 / sin(elevation_rad)
    power_log = log(power)

    coefs = polyfit(elevation_inv, power_log, 1)

    line = poly1d(coefs)

    label = "$\\tau_w = {:0.4f}$".format(-coefs[0])

    plt.plot(elevation_inv, line(elevation_inv), label=label)
    plt.plot(elevation_inv, power_log, '*')
    plt.xlabel('$1/\\sin(z)$', fontsize=16)
    plt.ylabel('$\\log(\Delta W)$', fontsize=16)
    plt.title('placeholder')
    plt.legend(loc=9, fontsize=16)
