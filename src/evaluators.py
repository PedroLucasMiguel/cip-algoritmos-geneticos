from math import sin, pi
from utils import *
import numpy as np

'''
    Este arquivo contem todas as funções de aptidão requeridas pelo trabalho.

    ex1_evaluator -> Função de aptidão do exercício 1
    ex2_evaluator -> Função de aptidão do exercício 2
    ex3_evaluator -> Função de aptidão do exercício 3
'''

class InvalidBitStringSize(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def ex1_evaluator(value) -> float:

    # Validação de tamanho para a bitstring, pois
    # caso ela não tenha um tamanho EXATAMENTE igual a 12, não podemos usar essa função
    if len(value) != 12:
        raise InvalidBitStringSize("A Bitstring of size 12 is expected to be provied to this evaluator")

    # Padrão do "0"
    expected = np.array([
        [True, True, True],
        [True, False, True],
        [True, False, True],
        [True, True, True]
    ])

    # Convertendo a bitstring para o "formato" esperado do padrão
    value = value.reshape(expected.shape)

    # Calculando a distância de hamming para o valor fornecido em relação ao esperado
    hamming_distance = 0
    for i in range(expected.shape[0]):
        for j in range(expected.shape[1]):
            if value[i][j] != expected[i][j]:
                hamming_distance += 1

    return hamming_distance

def ex2_evaluator(value) -> float:

    # Vide ex1_evaluator
    if len(value) != 12:
        raise InvalidBitStringSize("A Bitstring of size 12 is expected to be provied to this evaluator")

    # Neste caso, estamos considerando uma bitstring onde:
    # 1° Bit: 0.0 ou 1.0
    # Demais bits: Representação binária da parte fracional 

    x = 1.0 if value[0] == True else 0.0

    # Decodificando a parte fracional da bitstring
    x += binary_decode_decimal(value[1:])

    return 2**(-2 * (((x-0.1)/0.9)**2)) * (sin(5*pi*x)**6)

def ex3_evaluator(value) -> float:

    # Vide ex<1,2>_evaluator
    if len(value) != 30:
        raise InvalidBitStringSize("A Bitstring of size 30 is expected to be provied to this evaluator")

    # Função interna para o cálculo da função
    def f(x:float, y:float) -> float:
        return (1-x)**2 + 100*(y-x**2)**2
    
    '''
        Neste exercício, estamos lidando com a nossa bitstring de uma forma um pouco diferente.
        Como estamos lidando com valores dentro do intervalor real [-10, 10] temos que tomar
        alguns cuidados com a nossa bitstring, principalmente quando falamos da representação
        da parte inteira dos valores de "x" e "y".

        Considerando que a representação binária do número "10" é descrita como "1010", podemos
        perceber que se não fizermos nenhum tipo de tratamento, durante o processo de crossover e
        mutação, podemos obter cromossommos que ultrapassem o limite já pré-determinado.

        Dessa forma, visando evitar uma grande quantidade de checagens e mudanças para contornar
        o problema do crossover, optei por construir a minha bitstring da seguinte forma:

        Dado uma bitstring de tamanho 30, para os valores de X e Y temos:

        - 5 bits para a parte inteira: 1° Bit representa o sinal, e os demais são a representação
                                       do número em si usando código de gray. Isso é importante pois
                                       usando código de gray, garantimos que o valor "10" será
                                       representado como "1111", assim não é necessário fazer nenhum
                                       tipo de checagem durante o nosso crossover \o/;

        - 10 bits para a parte decimal: A representação da parte decimal pode ser tratada usando
                                        através de binários "simples", já que essa parte é bem
                                        menos restrita quanto a forma que ela pode assumir após
                                        o crossover e mutação;
    '''

    x = grayscode_decoder(value[1:5]) if value[0] else -1 * grayscode_decoder(value[1:5])
    x += binary_decode_decimal(value[5: 16])
    y = grayscode_decoder(value[17:21]) if value[16] else -1 * grayscode_decoder(value[17:21])
    y += binary_decode_decimal(value[21: 30])

    return f(x, y)