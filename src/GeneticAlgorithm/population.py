from .member import Member
from typing import List

'''
    Este arquivo contem o código relacionado a criação de uma população
'''

class Population:
    def __init__(self, nmembers:int = 8, bitstringsize:int = 12, predefined:List[Member] = None) -> None:
        
        # Caso a população não tenha sido "construida" préviamente a instanciação, gere uma nova
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
    
    # Retorna a população
    def get_population(self) -> List[Member]:
        return self.__population
    
    # Retorna o tamanho da bitstring da população
    def get_population_bitstring_size(self) -> int:
        return self.__populationBitstringSize