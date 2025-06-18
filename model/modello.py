from database.DAO import DAO
import networkx as nx
from model.sighting import Sighting

class Model:
    def __init__(self):
        self.DAO = DAO()
        self.graph = None
        self.listStates = self.DAO.get_all_states()
        self.idMapStates = {}
        for s in self.listStates:
            identity = s.id
            self.idMapStates[identity] = s
        self.idMapsSightings = {}



    def passYears(self):
        listYears = self.DAO.getYears()
        return listYears

    def passStates(self, year):
        listIdStates = self.DAO.getStatesOfYear(year)
        listStates = []
        for id in listIdStates:
            state = self.idMapStates[id]
            listStates.append(state)
        return listStates

    def createGraph(self, year, state):
        self.graph = nx.Graph()
        listNodes = self.DAO.getNodes(year, state)
        self.graph.add_nodes_from(listNodes)
        for s in listNodes:
            identity = s.id
            self.idMapsSightings[identity] = s
        listEdges = self.DAO.getEdges(year, state)
        for p in listEdges:
            one = self.idMapsSightings[p[0]]
            two = self.idMapsSightings[p[1]]
            if one.distance_HV(two) < 100:
                self.graph.add_edge(one, two)


