import random 
import numpy as np
import pandas as pd
import reader as rd
import math
import matplotlib.pyplot as pl
import networkx as nx

class ACO:
    def __init__(self,
    city1, 
    city2,
    ants_num, 
    type = 'das', 
    qas = 1,
    iteration_num = 3,
    rho = 0.5, 
    alpha = 1, 
    beta = 1, 
    verbosity = 0, 
    max_paths=2,
    shouldVisualize=False):
        self.ants_num = ants_num
        self.iteration_num = iteration_num
        #self.best_ants = ants_num # number of best ants
        self.rho = rho # pr-stwo wyparowania pheromones
        self.alpha = alpha
        self.beta = beta
        self.city1 = city1
        self.city2 = city2
        self.graph, self.distances, self.pheromones, self.eta, self.cities = rd.getGraphFromFile("germany50.txt")
        self.type = type
        self.q_qas = qas
        self.verbosity = verbosity
        self.max_paths = max_paths
        self.frame_counter = 0
        self.shouldVisualize = shouldVisualize


    def aco_run(self):
        path = None
        best_paths = []
        if self.verbosity >= 2:
            print(f"Looking for path from {self.city1} to {self.city2}")
        for i in range(self.iteration_num):
            if self.verbosity >= 2:
                print(f"Iteration {i} running:")
            paths = self.find_paths()
            correct_paths = [path for path in paths if path[0][-1] == self.city2]

            self.update_pheromone(correct_paths, self.best_ants)
            if(self.shouldVisualize):
                self.visualize(None)

            unique_paths = [path for path in correct_paths if path not in best_paths]

            if len(unique_paths) != 0:
                path = min(unique_paths , key = lambda x : x[1])            
                best_paths.append(path)
            # jeżeli powtarza się w best weź inny w paths?
            # evaporate pheromone
            self.pheromones * (1 - self.rho)
            # print(self.pheromones)

        # not choosing duplicated best paths
        best = sorted(best_paths , key = lambda x: x[1])
        return best[:self.max_paths]
   
    def find_paths(self):
        paths = []
        cities = [self.city1, self.city2]
        for i in range(self.ants_num):
            path = self.find_path(cities)
        paths.append((path, self.count_distance(path)))
            if self.shouldVisualize:
                self.visualize(path)
        return paths 

    def find_path(self, city):
        path = [ city[0] ]
        #taboo = set()
        taboo = self.pheromones.copy()
        end = city[1]

        prev = city[0]
      
        while True:
            nex = self.choose(self.pheromones[prev], self.eta[prev],taboo[prev])
            if self.verbosity >= 2:
                if nex != -1:
                    print(f"-going to {nex} searching {end}")
                else:
                    print("FINISHED")
            # ant could not find the way
            if nex == -1:
                break
            if nex == end:
                path.append(nex)
                if(self.verbosity >= 2):
                    print(" Found it ")
                break
            path.append(nex)
            taboo[prev][nex] = 0
            taboo[nex][prev] = 0
            prev = nex          
        return path

    def choose(self, pheromone , eta, taboo):
      
        ph = np.copy(taboo) 
        nominator = ph ** self.alpha * (eta ** self.beta)
        dominator = nominator.values.sum()
        prob = nominator / dominator
       
        if math.isnan(float((prob[0]))):
          # print(" Error ") 
            return -1
        nex = np.random.choice( prob.index.array ,1, p = prob)[0]
        return nex
        
    def count_distance(self, path):
        total = 0
        for i in range(len(path)-1):
            total += self.distances[path[i]][path[i+1]]
        return total


    def update_pheromone(self, paths):
        sort_paths = sorted(paths , key = lambda x: x[1])
        for path , distance in sort_paths[:best_ants]:
            for i in range(len(path)-1):
                city1 = path[i]
                city2 = path[i+1]
                if self.type == 'das':
                    delta = self.eta[city1][city2]
                    self.pheromones[city1][city2] += delta
                else:
                    self.pheromones[city1][city2] += self.q_qas
        self.update_graph()

    def update_graph(self):
        for edge in self.graph.edges:
            self.graph.edges[edge]['pheromone'] = self.pheromones[edge[0]][edge[1]]

    def visualize(self, path=None):
        layout = nx.kamada_kawai_layout(self.graph)
        
        # make directional graph with path to show
        
        edge_colors = self.getEdgeColors(self.graph)
        edge_width = self.getEdgeWidth(self.graph)
        
        # draw
        pl.figure(1, figsize=(10,10))
        nx.draw_networkx(
            self.graph,
            pos=layout, 
            with_labels=True,
            font_size=7,
            node_color='#ffaa77',
            edge_color=edge_colors,
            width=edge_width,
            node_shape='o')
        if path != None:
            path_graph = nx.DiGraph()
            for i in range(len(path)-1):
                path_graph.add_edge(path[i], path[i+1])
            nx.draw_networkx(
                path_graph,
                pos=layout, 
                nodelist=path,
                with_labels=False,
                node_color='#ff0000',
                node_shape='o')

        pl.savefig('results/'+str(self.frame_counter)+'.png', format='png')
        pl.close(1)
        self.frame_counter += 1

    def getEdgeColors(self, graph):
        return [self.pheromoneToColor(edge) for edge in graph.edges]
    def getEdgeWidth(self, graph):
        return [self.pheromoneToWidth(edge) for edge in graph.edges]

    def pheromoneToColor(self, edge):
        pheromone = self.graph[edge[0]][edge[1]]['pheromone']
        borders = {
            1: '#cccccc', 
            2: '#77ca6e',
            3: '#979b55',
            4: '#ba6637',
            5: '#cf4826',
            6: '#e52815'
            }
        for key,value in borders.items():
            if(pheromone < key): 
                return value
        return '#ff0000'
    def pheromoneToWidth(self, edge):
        pheromone = self.graph[edge[0]][edge[1]]['pheromone']
        borders = {
            1: 1.0, 
            2: 2.0,
            3: 3.0,
            4: 4.0,
            5: 5.0,
            6: 6.0
            }
        for key,value in borders.items():
            if(pheromone < key): 
                return value
        return 7.0

    
