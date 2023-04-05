from typing import List

'''
    Este arquivo contem funções que são utilizadas pelas funções de aptidão
'''

# Decodificação de binários decimmais
def binary_decode_decimal(value) -> float:
    x = 0
    for i in range(1, len(value)):
        if value[i]:
            x += 2**-(i+1)
    
    return x

# Decodificação de binário inteiros
def binary_decode_integer(value) -> int:
    i2 = 0
    x = 0
    for i in value[-1::-1]:
        x += i*(2**i2)
        i2 += 1

    return x

# Decodificação de código de gray
def grayscode_decoder(sequence:List[bool]) -> int: 
    output = []
    output.append(sequence[0])

    for i in range(1, len(sequence)):
        output.append(sequence[i] ^ output[-1])

    return binary_decode_integer(output)