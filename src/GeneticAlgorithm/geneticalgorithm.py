from population import Population
from member import Member
import numpy as np

class GeneticAlgorithm:
    def __init__(self, population:Population = None, 
                 evaluation_method = None,
                 crossover_probability:float = 0.6,
                 mutation_probability:float = 0.02,
                 max_generations:int = 100,
                 fitness_tolerance:int = 3) -> None:
        
        # TODO - Implement checks to avoid some dumb parameters :D
        self.__population = population
        self.__evaluator = evaluation_method
        self.__cp = crossover_probability
        self.__mp = mutation_probability
        self.__mg = max_generations
        self.__ftt = fitness_tolerance

        self.__fitness = None
        pass
    
    def __evaluate_population_members(self):
        for m in self.__population.get_population():
           m["Fitness"] = self.__evaluator(m["Member"].get_bitstring())

    def __calculate_population_degrees(self):

        fitness_sum = 0

        population = self.__population.get_population()

        for m in population:
            fitness_sum += m["Fitness"]

        # TODO - Por algum motivo podemos ter números acima de 360????
        m_before = None
        for m in population:
            if m_before != None:
                m["RoulleteDegrees"] = list(range(m_before["RoulleteDegrees"][-1] + 1, ((m_before["RoulleteDegrees"][-1] + 1) + np.floor((m["Fitness"] * 360)/fitness_sum).astype(int)) + 1))
            else:
                m["RoulleteDegrees"] = list(range(0, np.floor((m["Fitness"] * 360)/fitness_sum).astype(int)+1))
            m_before = m

    def __roullete_selection(self):

        selected_indexes = []

        population = self.__population.get_population()

        for i in range(len(population)):
            rn = np.random.randint(low=1, high=361)
            for m in range(len(population)):
                try:
                    population[m]["RoulleteDegrees"].index(rn)
                    selected_indexes.append(m)
                    break
                except ValueError:
                    continue

        return selected_indexes
    
    def __crossover(self, couples):
        
        population = self.__population.get_population()
        new_population_array = []

        for i in range(int(len(couples)/2)):
            if np.random.random() < self.__cp:
                print("Doing crossover with couple: [{}, {}]".format(couples[(i*2)], couples[(i*2)+1]))
                cutPoint = np.random.randint(low=0, high=self.__population.get_population_bitstring_size())
                print("Cut point: {}".format(cutPoint))
                children1BitString = population[i*2]["Member"].get_bitstring().copy()
                children1BitString[cutPoint:] = population[(i*2)+1]["Member"].get_bitstring()[cutPoint:]

                children2BitString = population[(i*2)+1]["Member"].get_bitstring().copy()
                children2BitString[cutPoint:] = population[i*2]["Member"].get_bitstring()[cutPoint:]
                new_population_array.append({
                    "Member": Member(predefinedBitString=children1BitString),
                    "Fitness": 0.0,
                    "RoulleteDegrees": 0,
                })
                new_population_array.append({
                    "Member": Member(predefinedBitString=children2BitString),
                    "Fitness": 0.0,
                    "RoulleteDegrees": 0,
                })

            else:
                new_population_array.append(population[i*2])
                new_population_array.append(population[(i*2)+1])

        self.__population = Population(predefined=new_population_array)


    def start(self) -> Member:

        self.__evaluate_population_members()

        # DEBUG
        self.__calculate_population_degrees()


        print("------------------------------------Population before------------------------------------")
        for m in self.__population.get_population():
            print(m["Member"].get_bitstring())
        print("------------------------------------------------------------------------")
        couples = self.__roullete_selection()
        print("Couples: {}".format(couples))
        self.__crossover(couples)
        print("------------------------------------Population after------------------------------------")
        for m in self.__population.get_population():
            print(m["Member"].get_bitstring())
        print("------------------------------------------------------------------------")


        fitnessStrikes = 0 # Quantidade de gerações que não melhoraram o fitness value
        converged = False
        generation = 1

        

        # Execute o algoritmo enquanto:
        # - Não atingirmos o máximo de gerações
        # - Não passarmos do limite máximo de "strikes" no nosso valor de aptidão
        # - Não convergirmos na melhor resposta
        #while generation != self.__mg and fitnessStrikes != self.__ftt and not converged:
        #    self.__calculate_population_degrees()
        #    pass


        return None

def evaluator(value) -> float:

    expected = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1]
    ])

    value = value.reshape(expected.shape)

    return np.mean(np.isclose(value, expected))

if __name__ == "__main__":
    GeneticAlgorithm(Population(), evaluator).start()
