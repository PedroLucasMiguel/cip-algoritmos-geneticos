from GeneticAlgorithm.geneticalgorithm import GeneticAlgorithm
from GeneticAlgorithm.population import Population
from matplotlib import pyplot as plt
from math import sin, pi
import numpy as np

# Reconhecimento do 0
def evaluator(value) -> float:

    expected = np.array([
        [True, True, True],
        [True, False, True],
        [True, False, True],
        [True, True, True]
    ])

    value = value.reshape(expected.shape)

    hamming_distance = 0
    for i in range(expected.shape[0]):
        for j in range(expected.shape[1]):
            if value[i][j] != expected[i][j]:
                hamming_distance += 1

    return hamming_distance

def g(value) -> float:

    x = 1.0 if value[0] == True else 0.0

    for i in range(1, len(value)):
        if value[i]:
            x += 2**-(i+1)

    return 2**(-2 * (((x-0.1)/0.9)**2)) * (sin(5*pi*x)**6)

# TODO - Depois fazer o resto das coisas, estou com preguiça, eu não aguento mais :D

if __name__ == "__main__":
    a = GeneticAlgorithm(Population(nmembers=1024), evaluator, expected_value=0, maximize=False).start()
    img = a["Member"].get_bitstring()
    img = img.reshape((4,3))
    plt.imshow(img)
    plt.show()