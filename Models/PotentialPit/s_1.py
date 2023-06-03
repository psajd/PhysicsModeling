import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


def find_k_plus(C, x):
    return np.tan(x) - np.sqrt(C ** 2 - x ** 2) / x


def find_k_minus(C, x):
    return 1 / np.tan(x) + np.sqrt(C ** 2 - x ** 2) / x


def get_energy(func, E, count_levels_energy, U0, C, step):
    for n in range(count_levels_energy):
        x = fsolve(func, np.array([np.pi * (n - step), min(np.pi * (n - step + 0.5), C)]), args=(C,))
        E[0, n] = x[0]
        E[1, n] = -U0 * (1 - (E[0, n] / C) ** 2)
    return E


def psi(n, L, x):
    return np.sqrt(2/L)*np.sin(n*np.pi*x/L)


def psi_2(n, L, x):
    return np.square(psi(n, L, x))


if __name__ == '__main__':
    U0 = 100
    a = 2
    L = 1

    C = np.sqrt(2 * U0) * a

    count_levels_energy_plus = int(C / np.pi + 1)
    count_levels_energy_minus = int(C / np.pi + 1 / 2)

    E_1 = np.zeros((2, count_levels_energy_plus))
    E_2 = np.zeros((2, count_levels_energy_minus))

    E_1 = get_energy(find_k_plus, E_1, count_levels_energy_plus, U0, C, 1)
    E_2 = get_energy(find_k_minus, E_2, count_levels_energy_minus, U0, C, 0.5)

    print(E_1)
    print(E_2)

    plt.plot(E_1[1, :], drawstyle='steps-pre', label='график для четных собственных чисел')
    plt.plot(E_2[1, :], drawstyle='steps-pre', label='график для нечетных собственных чисел')
    plt.title('график зависимости потенциальной энергии от энергетических уровней на которых она располагается')
    plt.legend()
    plt.xlabel('энергетический ур.(n)')
    plt.ylabel('эВ')
    plt.show()

    # Построение потенциальной ямы
    x = np.linspace(-a*1.1, a*1.1, 100)
    potential = np.piecewise(x, [np.abs(x) <= a, np.abs(x) > a], [-U0, 0])
    plt.plot(x, potential, 'r-', label='Потенциальная яма')

    for i in range(count_levels_energy_plus):
        plt.hlines(E_1[1, i], -a, a, colors='b', linestyles='dashed')

    for i in range(len(E_1[1])):
        psi_x = np.linspace(0, 1, 1000)
        psi_y = psi(i, L, psi_x)
        plt.plot((psi_x - 0.5)*4, psi_y+E_1[1, i], 'm-')

    plt.ylim([-1.1 * U0, 0.1 * U0])

    plt.legend()
    plt.ylabel('эВ')
    plt.xlabel('X')
    plt.show()
