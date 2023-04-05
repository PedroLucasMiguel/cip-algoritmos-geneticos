from GeneticAlgorithm.geneticalgorithm import GeneticAlgorithm
from GeneticAlgorithm.population import Population
from matplotlib import pyplot as plt
from evaluators import *

if __name__ == "__main__":

    #ex = GeneticAlgorithm(Population(nmembers=3072, bitstringsize=12), ex1_evaluator, maximize=False, expected_value=0)
    ex = GeneticAlgorithm(Population(nmembers=3072, bitstringsize=12), ex2_evaluator, maximize=True)
    #ex = GeneticAlgorithm(Population(nmembers=3072, bitstringsize=30), ex3_evaluator, maximize=False)
    r = ex.start()
    print(ex.get_fitness_history())
    #img = r["Member"].get_bitstring()
    #img = img.reshape((4,3))
    #plt.imshow(img)
    #plt.show()