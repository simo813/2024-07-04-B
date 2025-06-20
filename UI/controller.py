import flet as ft
from UI.view import View
from model.modello import Model
import networkx as nx


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self.view = view
        # the model, which implements the logic of the program and holds the data
        self.model = model

    def fillDD(self):
        listYears = self.model.passYears()
        for year in listYears:
            self.view.ddyear.options.append(ft.dropdown.Option(key=year, text=year))
        self.view.update_page()

    def fillDDStates(self):
        listStates = self.model.passStates(int(self.view.ddYearValue))
        for state in listStates:
            self.view.ddstate.options.append(ft.dropdown.Option(key=state.id, text=state.name))
        self.view.update_page()



    def handle_graph(self, e):
        self.view.txt_result1.clean()
        if self.view.ddYearValue is not None and self.view.ddStateValue is not None:
            self.model.createGraph(int(self.view.ddYearValue), self.view.ddStateValue)
            graph = self.model.graph
            listOfConnected = sorted(nx.connected_components(graph), key=len, reverse=True)
            largest_cc = max(nx.connected_components(graph), key=len)
            self.view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {graph.number_of_nodes()}\n"
                                                          f"Numero di archi: {graph.number_of_edges()}\n"
                                                          f"Il grafo ha {len(list(listOfConnected))} componenti connesse\n"
                                                          f"La componente connessa più grande è costituita da {len(largest_cc)} nodi:\n"))


            for node in list(largest_cc):
                self.view.txt_result1.controls.append(ft.Text(f"{node.__str__()}\n"))


            self.view.btn_path.disabled = False
        else:
            self.view.txt_result1.controls.append(ft.Text(f"Seleziona i valori della ricerca"))
        self.view.update_page()

    def handle_path(self, e):
        self.view.txt_result2.clean()
        optPath, optPathPoints = self.model.getOptPath()
        self.view.txt_result2.controls.append(ft.Text(f"Il punteggio del cammino ottimo è: {optPathPoints}\n"))
        for node in optPath:
            self.view.txt_result2.controls.append(ft.Text(f"{node.__str__()}\n"))
        self.view.update_page()


