import numpy as np
from matplotlib import pyplot as plt

class Member:
    def __init__(self, bitstringsize:int = 12, predefinedBitString = None) -> None:
        
        if predefinedBitString is None:
            self.__bitstring = np.random.randint(low=0, high=2, size=bitstringsize, dtype=bool)
        else:
            self.__bitstring = predefinedBitString

        pass

    def get_bitstring(self):
        return self.__bitstring
    
    def mutate_at(self, index:int):
        self.__bitstring[index] = not self.__bitstring[index]