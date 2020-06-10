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
    type = 'qas', 
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
        self.best_ants = ants_num # number of best ants
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

        # end = self.cities.index(self.city2)
        # start = self.cities.index(self.city1)
        
        # self.pheromones = self.pheromones[start].replace(1, 5)
        # self.pheromones = self.pheromones[end].replace(1,5)

        for i in range(self.iteration_num):
            if self.verbosity >= 2:
                print(f"Iteration {i} running:")
            paths = self.find_paths()
            self.update_pheromone(paths, self.best_ants)
            #print(paths)
            #ignore paths that don't finish with target city
            correct_paths = [path for path in paths if path[0][-1] == self.city2 and path not in best_paths]
            if len(correct_paths) != 0:
                path = min(correct_paths , key = lambda x : x[1])            
                best_paths.append(path)
            # jeżeli powtarza się w best weź inny w paths?
            # evaporate pheromone
            self.pheromones * (1 - self.rho)

        # choosing duplicated best paths
        best = sorted(best_paths , key = lambda x: x[1])
        # print("Best paths", best)
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

            # print(nex[0])
            # ant found the end 
            if nex == end:
                path.append(nex)
                if(self.verbosity >= 2):
                    print(" Found it ")
                break

            path.append(nex)
            taboo[prev][nex] = 0
            taboo[nex][prev] = 0
            prev = nex
               
        #path.append((prev,self.cities[0]))
        return path

    def choose(self, pheromone , eta, taboo):
      
        ph = np.copy(taboo) 
        nominator = ph ** self.alpha * (eta ** self.beta)
        dominator = nominator.values.sum()
        prob = nominator / dominator
        # print("nom : {} pheromone : {} dominator {}".format(nominator, ph, dominator))
        # print(prob)
        if math.isnan(float((prob[0]))):
            # print(" Error ") 
            return -1
        nex = np.random.choice( prob.index.array ,1, p = prob)[0]
        
        # print(nex)
        return nex
        
    def count_distance(self, path):
        total = 0
        for i in range(len(path)-1):
            total += self.distances[path[i]][path[i+1]]
        return total

    def update_pheromone(self, paths, best_ants):
        sort_paths = sorted(paths , key = lambda x: x[1])
        for path , distance in sort_paths[:best_ants]:
            for i in range(len(path)-1):
                city1 = path[i]
                city2 = path[i+1]
                if self.type == 'das':
                    self.pheromones[city1][city2] += self.eta[city[0]][city[1]]
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
        
        # draw
        pl.figure(1, figsize=(10,10))
        nx.draw_networkx(
            self.graph,
            pos=layout, 
            with_labels=True,
            font_size=7,
            node_color='#ffaa77',
            edge_color=edge_colors,
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

        # TODO colorful edges
        pl.savefig('results/'+str(self.frame_counter)+'.png', format='png')
        pl.close(1)
        self.frame_counter += 1

    def getEdgeColors(self, graph):
        return [self.pheromoneToColor(edge) for edge in graph.edges]
    def pheromoneToColor(self, edge):
        pheromone = self.graph[edge[0]][edge[1]]['pheromone']
        borders = {
            1: '#cccccc', 
            2: '#ccddcc',
            3: '#cceecc',
            4: '#ccffcc',
            5: '#ddeecc',
            6: '#eeddcc'
            }
        for key,value in borders.items():
            if(pheromone < key): return value
        return '#ff0000'

    
