from PyQt6 import uic, QtWidgets
from GeneticAlgorithm.geneticalgorithm import GeneticAlgorithm
from GeneticAlgorithm.population import Population
from matplotlib import pyplot as plt
from evaluators import *
from UI.AlertBox import AlertBox
import time

app = QtWidgets.QApplication([])
interface = uic.loadUi("UI/mainscreen.ui")

def get_data() -> dict:
    data = {}
    data["nmembers"] = interface.spin_population.value()
    data["cp"] = interface.spin_cp.value()
    data["mp"] = interface.spin_mp.value()

    if data["cp"] > data["mp"]:
        data["n_generations"] = interface.spin_gen.value()
        data["fitness_tolerance"] = interface.spin_fitness.value()
        data["maximize"] = interface.check_maximize.isChecked()
        if interface.spin_ev.isEnabled():
            data["ev"] = interface.spin_ev.value()
        else:
            data["ev"] = None

        return data
    else:
        AlertBox("Não é possível usar uma taxa de mutação maior ou igual a taxa de crossover")
        return None

def __enable_expected_value() -> None:
    if interface.check_use_ev.isChecked():
        interface.spin_ev.setEnabled(True)
    else:
        interface.spin_ev.setEnabled(False)

def __start_button_clicked() -> None:
    interface.text_output.clear()
    interface.progress_bar.setValue(int(0))
    data = get_data()
    
    if data is not None:
        if interface.radio_ex1.isChecked():
            start = time.time()
            ex = GeneticAlgorithm(
                    Population(nmembers=data["nmembers"], bitstringsize=12), 
                    evaluation_method=ex1_evaluator,
                    crossover_probability=data["cp"], 
                    mutation_probability=data["mp"],
                    max_generations=data["n_generations"],
                    fitness_tolerance=data["fitness_tolerance"],
                    maximize=data["maximize"], 
                    expected_value=data["ev"],
                    ui=interface)
            r = ex.start()
            end = time.time()
            img = r["Member"].get_bitstring()
            img = img.reshape((4,3))
            plt.imshow(img)
            plt.show()
            
        elif interface.radio_ex2.isChecked():
            start = time.time()
            ex = GeneticAlgorithm(
                    Population(nmembers=data["nmembers"], bitstringsize=12), 
                    evaluation_method=ex2_evaluator,
                    crossover_probability=data["cp"], 
                    mutation_probability=data["mp"],
                    max_generations=data["n_generations"],
                    fitness_tolerance=data["fitness_tolerance"],
                    maximize=data["maximize"], 
                    expected_value=data["ev"],
                    ui=interface)
            r = ex.start()
            end = time.time()

        else:
            start = time.time()
            ex = GeneticAlgorithm(
                    Population(nmembers=data["nmembers"], bitstringsize=30), 
                    evaluation_method=ex3_evaluator,
                    crossover_probability=data["cp"], 
                    mutation_probability=data["mp"],
                    max_generations=data["n_generations"],
                    fitness_tolerance=data["fitness_tolerance"],
                    maximize=data["maximize"], 
                    expected_value=data["ev"],
                    ui=interface)
            r = ex.start()
            end = time.time()

        interface.text_output.appendPlainText("Aptidão minima, média e máxima alcançada: {}".format(ex.get_fitness_history()))
        duration = (end - start) 
        duration *= 1000
        interface.text_output.appendPlainText("Tempo de execução (ms): {}".format(duration))   
    
def show_ui() -> None:
    interface.start_button.clicked.connect(__start_button_clicked)
    interface.check_use_ev.clicked.connect(__enable_expected_value)
    interface.show()
    app.exec()


if __name__ == "__main__":
    show_ui()
    pass