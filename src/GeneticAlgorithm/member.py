import numpy as np
from typing import List

class Member:
    def __init__(self, bitstringsize:int = 12, predefinedBitString:List[bool] = None) -> None:
        
        if predefinedBitString is None:
            self.__bitstring:List[bool] = np.random.randint(low=0, high=2, size=bitstringsize, dtype=bool)
        else:
            self.__bitstring:List[bool]  = predefinedBitString

        pass

    def get_bitstring(self) -> List[bool] :
        return self.__bitstring
    
    def mutate_at(self, index:int) -> None:
        self.__bitstring[index] = not self.__bitstring[index]