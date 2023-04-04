from GeneticAlgorithm.geneticalgorithm import GeneticAlgorithm
from GeneticAlgorithm.population import Population
from matplotlib import pyplot as plt
from math import sin, pi
from typing import List
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

def __binary_decode_decimal(value) -> float:
    x = 0
    for i in range(1, len(value)):
        if value[i]:
            x += 2**-(i+1)
    
    return x

def __binary_decode_integer(value) -> int:
    i2 = 0
    x = 0
    for i in value[-1::-1]:
        x += i*(2**i2)
        i2 += 1

    return x

def __grayscode_decoder(sequence:List[bool]) -> int: 
    output = []
    output.append(sequence[0])

    for i in range(1, len(sequence)):
        output.append(sequence[i] ^ output[-1])

    return __binary_decode_integer(output)


def ex3(value) -> float:

    # Estou usando uma bitstring de tamanho 30

    def f(x:float, y:float) -> float:
        return (1-x)**2 + 100*(y-x**2)**2

    x = __grayscode_decoder(value[1:5]) if value[0] else -1 * __grayscode_decoder(value[1:5])
    x += __binary_decode_decimal(value[5: 16])
    y = __grayscode_decoder(value[17:21]) if value[16] else -1 * __grayscode_decoder(value[17:21])
    y += __binary_decode_decimal(value[21: 30])

    return f(x, y)


if __name__ == "__main__":

    #grayscode_decoder([True, True, True, True])

    a = GeneticAlgorithm(Population(nmembers=1024, bitstringsize=30), ex3, maximize=False).start()
    #img = a["Member"].get_bitstring()
    #img = img.reshape((4,3))
    #plt.imshow(img)
    #plt.show()