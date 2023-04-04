from .population import Population
from .member import Member
import numpy as np

class GeneticAlgorithm:
    def __init__(self, population:Population = None, 
                 evaluation_method = None,
                 crossover_probability:float = 0.6,
                 mutation_probability:float = 0.02,
                 max_generations:int = 1000,
                 fitness_tolerance:int = 900,
                 expected_value:float = None,
                 maximize:bool = False) -> None:
        
        # FIXME - Implementar verificação dos parâmetros
        self.__population:Population = population
        self.__evaluator = evaluation_method
        self.__cp:float = crossover_probability
        self.__mp:float = mutation_probability
        self.__mg:int = max_generations
        self.__ftt:int = fitness_tolerance
        self.__exv:float= expected_value
        self.__maximize:bool = maximize

        self.__fitness = None
        pass
    
    def __evaluate_population_members(self) -> None:
        for m in self.__population.get_population():
           m["Fitness"] = self.__evaluator(m["Member"].get_bitstring())

    def __evaluate_population(self) -> float:
        population_sum_fitness = 0

        population = self.__population.get_population()

        for m in population:
            population_sum_fitness += m["Fitness"]

        return population_sum_fitness/len(population)

    def __check_convergence(self) -> bool:
        for m in self.__population.get_population():
            if m["Fitness"] == self.__exv:
                return True
        return False

    def __calculate_population_degrees(self) -> None:

        fitness_sum = 0

        population = self.__population.get_population()

        for m in population:
            fitness_sum += m["Fitness"]

        # FIXME - Por algum motivo podemos ter números acima de 360????
        m_before = None
        for m in population:
            if m_before != None:
                m["RoulleteDegrees"] = (m_before["RoulleteDegrees"][-1] + 1, ((m_before["RoulleteDegrees"][-1] + 1) + np.floor((m["Fitness"] * 360)/fitness_sum).astype(int)) + 1)
            else:
                m["RoulleteDegrees"] = (0, np.floor((m["Fitness"] * 360)/fitness_sum).astype(int)+1)
            m_before = m
            

    def __roullete_selection(self) -> list:

        selected_indexes = []

        population = self.__population.get_population()

        for i in range(len(population)):
            rn = np.random.randint(low=1, high=361)
            for m in range(len(population)):
                if rn >= population[m]["RoulleteDegrees"][0] and rn <= population[m]["RoulleteDegrees"][1]: 
                    selected_indexes.append(m)
                    break

        return selected_indexes
    
    def __crossover(self, couples) -> None:
        
        population = self.__population.get_population()
        new_population_array = []

        for i in range(int(len(couples)/2)):
            if np.random.random() < self.__cp:
                cutPoint = np.random.randint(low=0, high=self.__population.get_population_bitstring_size())
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

    def __mutate(self) -> None:
        for m in self.__population.get_population():
            for i in range(len(m["Member"].get_bitstring())):
                if np.random.random() < self.__mp:
                    m["Member"].mutate_at(i)

    def start(self) -> Member:
        fitnessStrikes:int = 0 # Quantidade de gerações que não melhoraram o fitness value
        generation:int = 1

        self.__evaluate_population_members() # Avalia cada membro individualmente

        # Verifica convergencia se necessário
        converged = self.__check_convergence() if self.__exv is not None else False

        self.__fitness = self.__evaluate_population() # Define o valor médio de aptidão da população

        # Execute o algoritmo enquanto:
        # - Não atingirmos o máximo de gerações
        # - Não passarmos do limite máximo de "strikes" no nosso valor de aptidão
        # - Não convergirmos na melhor resposta
        while generation != self.__mg and fitnessStrikes != self.__ftt and not converged:
            self.__calculate_population_degrees()

            # Seleção
            couples = self.__roullete_selection()

            # Reprodução
            self.__crossover(couples)
            self.__mutate()

            # Avalia a aptidão de cada um individualmente
            self.__evaluate_population_members()

            # Checa convergência caso necessário
            converged = self.__check_convergence() if self.__exv is not None else False

            # Verifica se a aptidão média da população melhorou ou não
            temp_fitness = self.__evaluate_population()
            if self.__maximize:
                if temp_fitness > self.__fitness:
                    self.__fitness = temp_fitness
                else:
                    fitnessStrikes += 1
            else:
                if temp_fitness < self.__fitness:
                    self.__fitness = temp_fitness
                else:
                    fitnessStrikes += 1

            # Soma 1 no contador de gerações
            generation += 1
        
        # Resultados do processo
        if generation == self.__mg:
            print("Fim do processo: Máximo de gerações alcançado")
        elif fitnessStrikes == self.__ftt:
            print("Fim do processo: População parou de se tornar mais apta")
        elif converged == True:
            print("Fim do processo: Convergência alcançada!")

        population = self.__population.get_population()
        best_member = population[0]
        best_fitness = population[0]["Fitness"]

        if self.__maximize:
            for m in self.__population.get_population():
                if m["Fitness"] > best_fitness:
                    best_fitness = m["Fitness"]
                    best_member = m
        else:
            for m in self.__population.get_population():
                if m["Fitness"] < best_fitness:
                    best_fitness = m["Fitness"]
                    best_member = m

        print("Geração: {}".format(generation))
        print("Melhor Membro: {}".format(best_member))
        print("Bitstring: {}".format(best_member["Member"].get_bitstring()))

        return best_member