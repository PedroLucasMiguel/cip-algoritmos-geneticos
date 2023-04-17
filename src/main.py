from PyQt6 import uic, QtWidgets, QtGui
from GeneticAlgorithm.geneticalgorithm import GeneticAlgorithm
from GeneticAlgorithm.population import Population
from matplotlib import pyplot as plt
from evaluators import *
from UI.AlertBox import AlertBox
import time
import os

app = QtWidgets.QApplication([])
interface = uic.loadUi("UI/mainscreen.ui")

# Recolhe os dados fornecidos na interface
def get_data() -> dict:
    data = {}
    data["nmembers"] = interface.spin_population.value()
    data["cp"] = interface.spin_cp.value()
    data["mp"] = interface.spin_mp.value()

    data["n_generations"] = interface.spin_gen.value()
    data["fitness_tolerance"] = interface.spin_fitness.value()
    data["maximize"] = interface.check_maximize.isChecked()

    if interface.spin_ev.isEnabled():
        data["ev"] = interface.spin_ev.value()
    else:
        data["ev"] = None

    data["n_executions"] = interface.spin_n_executions.value()

    return data

# Função responsável em habilitar (ou não) o campo de valor esperado
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
            graph_name = "Ex1_{}".format(time.time())
            ex = GeneticAlgorithm(
                    Population(nmembers=data["nmembers"], bitstringsize=12), 
                    evaluation_method=ex1_evaluator,
                    crossover_probability=data["cp"], 
                    mutation_probability=data["mp"],
                    max_generations=data["n_generations"],
                    fitness_tolerance=data["fitness_tolerance"],
                    maximize=data["maximize"], 
                    n_executions=data["n_executions"],
                    expected_value=data["ev"],
                    ui=interface,
                    graph_name=graph_name)
            r = ex.start()
            #fitness = ex1_evaluator(r["Member"].get_bitstring())
            img = r["Member"].get_bitstring()
            img = img.reshape((4,3))
            time.sleep(0.3)
            plt.imshow(img)
            plt.show()
            
        elif interface.radio_ex2.isChecked():
            graph_name = "Ex2_{}".format(time.time())
            ex = GeneticAlgorithm(
                    Population(nmembers=data["nmembers"], bitstringsize=12), 
                    evaluation_method=ex2_evaluator,
                    crossover_probability=data["cp"], 
                    mutation_probability=data["mp"],
                    max_generations=data["n_generations"],
                    fitness_tolerance=data["fitness_tolerance"],
                    maximize=data["maximize"],
                    n_executions=data["n_executions"], 
                    expected_value=data["ev"],
                    ui=interface,
                    graph_name=graph_name)
            r = ex.start()
            #fitness = ex2_evaluator(r["Member"].get_bitstring())

        else:
            graph_name = "Ex3_{}".format(time.time())
            ex = GeneticAlgorithm(
                    Population(nmembers=data["nmembers"], bitstringsize=30), 
                    evaluation_method=ex3_evaluator,
                    crossover_probability=data["cp"], 
                    mutation_probability=data["mp"],
                    max_generations=data["n_generations"],
                    fitness_tolerance=data["fitness_tolerance"],
                    maximize=data["maximize"],
                    n_executions=data["n_executions"],  
                    expected_value=data["ev"],
                    ui=interface,
                    graph_name=graph_name)
            r = ex.start()
            #fitness = ex3_evaluator(r["Member"].get_bitstring())
        
        # Apresentando os resultados finais da execução
        interface.image_label.setPixmap(QtGui.QPixmap("output/{}_final.png".format(graph_name)))
        interface.text_output.appendPlainText("\n{}Resultados finais{}".format("-"*20, "-"*20))
        interface.text_output.appendPlainText("Média de gerações: {}".format(ex.get_mean_generations()))
        fh = ex.get_fitness_history()
        interface.text_output.appendPlainText("Valor de aptidão mínimo: {} | std: {}".format(fh[0][0], fh[0][1]))
        interface.text_output.appendPlainText("Valor de aptidão médio: {} | std: {}".format(fh[1][0], fh[1][1]))
        interface.text_output.appendPlainText("Valor de aptidão máximo: {} | std: {}".format(fh[2][0], fh[2][1]))
        interface.text_output.appendPlainText("Melhor membro: {}".format(r))
        #interface.text_output.appendPlainText("Fitness: {}".format(fitness))
        interface.text_output.appendPlainText("Bitstring: {}".format(r["Member"].get_bitstring()))
        interface.text_output.appendPlainText("Tempo de execução médio (s): {}".format(ex.get_execution_time()))  
    
def show_ui() -> None:
    interface.start_button.clicked.connect(__start_button_clicked)
    interface.check_use_ev.clicked.connect(__enable_expected_value)
    interface.show()
    app.exec()

if __name__ == "__main__":
    try:
        os.mkdir("output")
    except FileExistsError:
        pass
    
    show_ui()
    pass