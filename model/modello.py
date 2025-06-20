import copy

from database.DAO import DAO
import networkx as nx
from model.sighting import Sighting

class Model:
    def __init__(self):
        self.optPathPoints = None
        self.optPath = None
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



    def getOptPath(self):
        self.optPath = []
        self.optPathPoints = 0
        graph = self.graph

        for node in graph.nodes:
            self.recursion(
                source=node,
                partial=[node],
                partialPoints=0
            )
            print("\nENTRATO\n")
        print(self.optPath)
        print(self.optPathPoints)
        print("\nFINE\n")

        return self.optPath, self.optPathPoints

    def recursion(self, source, partial, partialPoints):
        graph = self.graph

        if partialPoints > self.optPathPoints:
            print("\n---------------------------------")
            print(partialPoints)
            self.optPathPoints = partialPoints
            self.optPath = copy.deepcopy(partial)


        for successor in graph.neighbors(source):
            if self.isAdmissible(successor, partial):
                print("successore ammissibile")
                if successor.duration > source.duration:
                    print("successore ha valore di duration maggiore di source")
                    if  successor.datetime.month ==  source.datetime.month:
                        partial.append(successor)
                        self.recursion(successor, partial, partialPoints + 200)
                        print("NUOVA RICORSIONE\n")
                        partial.pop()

                    else:
                        partial.append(successor)
                        self.recursion(successor, partial, partialPoints + 100)
                        print("NUOVA RICORSIONE\n")
                        partial.pop()

    def isAdmissible(self, successor, partial):
        if successor not in partial:
            count = 0
            for element in partial:
                if element.datetime.month == successor.datetime.month:
                    count += 1
                    if count > 3:
                        return False
                    else:
                        return True
        else:
            return False




