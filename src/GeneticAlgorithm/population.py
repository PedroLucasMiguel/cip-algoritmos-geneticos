from .member import Member

class Population:
    def __init__(self, nmembers:int = 8, bitstringsize:int = 12, predefined = None) -> None:
        
        if predefined is None:

            self.__population = []
            self.__populationBitstringSize = bitstringsize

            for i in range(nmembers):
                self.__population.append({
                                        "Member": Member(self.__populationBitstringSize),
                                        "Fitness": 0.0,
                                        "RoulleteDegrees": 0,
                                        })

        else:
            self.__population = predefined
            self.__populationBitstringSize = len(predefined)

        pass
    
    def get_population(self):
        return self.__population
    
    def get_population_bitstring_size(self) -> int:
        return self.__populationBitstringSize