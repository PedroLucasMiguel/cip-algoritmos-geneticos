from .member import Member
from typing import List

class Population:
    def __init__(self, nmembers:int = 8, bitstringsize:int = 12, predefined:List[Member] = None) -> None:
        
        if predefined is None:

            self.__population:List[Member] = []
            self.__populationBitstringSize:int = bitstringsize

            for i in range(nmembers):
                self.__population.append({
                                        "Member": Member(self.__populationBitstringSize),
                                        "Fitness": 0.0,
                                        "RoulleteDegrees": 0,
                                        })

        else:
            self.__population:List[Member] = predefined
            self.__populationBitstringSize:int = len(predefined)

        pass
    
    def get_population(self) -> List[Member]:
        return self.__population
    
    def get_population_bitstring_size(self) -> int:
        return self.__populationBitstringSize