import sys
sys.path.insert(0, './src')

import numpy as np
import math
import networkx as nx

from visualization_frame import VisualizationFrame  # type: ignore

class ACO:
    def __init__(self,
    city1, 
    city2,
    ants_num,
    graph,
    type = 'das', 
    qas = 1,
    das = 1,
    iteration_num = 3,
    rho = 0.5, 
    alpha = 1, 
    beta = 1, 
    verbosity = 0,
    shouldVisualize=False,
    seed=None):
        """Ant Colony Optimization algorithm to find shortest path between city1 and city2 in given graph
        city1 - starting city
        city2 - target city
        ants_num - number of ants in each iteration
        graph - networkx graph with edges having 'weight' and 'pheromone' attributes
        type - type of algorithm to use 'das' - direct ant system, 'qas' - quality ant system
        qas - constant used in quality ant system to update pheromone
        das - constant used in direct ant system to update pheromone
        iteration_num - number of iterations to run
        rho - pheromone evaporation rate
        alpha - pheromone importance
        beta - distance importance
        verbosity - level of verbosity 0 - silent, 1 - only result, 2 - detailed
        shouldVisualize - whether to save visualization of algorithm run in 'results/' directory
        seed - random seed to use in ant decisions (for testing purposes)
        """
        self.ants_num = ants_num
        self.iteration_num = iteration_num
        self.rho = rho
        self.alpha = alpha
        self.beta = beta
        self.start_city = city1
        self.target_city = city2
        self.graph = graph
        self.type = type
        self.q_qas = qas
        self.q_das = das
        self.verbosity = verbosity
        self.max_paths = 2
        self.frame_counter = 0
        self.shouldVisualize = shouldVisualize
        self.seed = seed

        self.distances = nx.to_pandas_adjacency(self.graph, weight='weight', nonedge=np.inf)
        self.pheromones = nx.to_pandas_adjacency(self.graph, weight='pheromone', nonedge=0)
        self.eta = 1 / self.distances
        self.frames_to_visualize = []

        VisualizationFrame.set_start_and_target(self.start_city, self.target_city)
    


    def aco_run(self):
        path = None
        best_paths = []
        if self.verbosity >= 2:
            print(f"Looking for path from {self.start_city} to {self.target_city}")
        for it_number in range(self.iteration_num):
            if self.verbosity >= 2:
                print(f"Iteration {it_number} running:")
            paths = self.find_paths()
            correct_paths = [path for path in paths if path[0][-1] == self.target_city]

            if(self.shouldVisualize):
                for path in correct_paths:
                    frame = VisualizationFrame(self.graph.copy(), path[0], it_number)
                    self.frames_to_visualize.append(frame)

            self.update_pheromone(correct_paths)
            if(self.shouldVisualize):
                frame = VisualizationFrame(self.graph.copy(), None, it_number)
                self.frames_to_visualize.append(frame)

            unique_paths = [path for path in correct_paths if path not in best_paths]

            if len(unique_paths) != 0:
                path = min(unique_paths , key = lambda x : x[1])            
                best_paths.append(path)
           
            self.pheromones *= (1 - self.rho)
            
        best = sorted(best_paths , key = lambda x: x[1])
        return best[:self.max_paths], self.frames_to_visualize
   
    def find_paths(self):
        paths = []
        for i in range(self.ants_num):
            path = self.find_path()
            paths.append((path, self.count_distance(path)))
        return paths 

    def find_path(self):
        """ Steps done by single ant to find path from start to end city 
        taboo - copy of pheromones table where visited cities are marked with 0 to avoid going back
        """
        path = [ self.start_city ]
        taboo = self.pheromones.copy()
        previous_city = self.start_city
      
        while self.is_path_not_found(previous_city):
            next_city = self.choose_next_city(self.eta[previous_city],taboo[previous_city])
            if self.verbosity >= 2:
                self.report_step(next_city)
            
            if self.is_ant_stuck(next_city):
                previous_city = -1
                break

            path.append(next_city)
            if next_city != self.target_city:
                self.block_visited_edge(taboo, previous_city, next_city)

            previous_city = next_city

            if next_city == self.target_city and self.verbosity >= 2:
                print(" Found it ")     
        return path

    def block_visited_edge(self, taboo, previous_city, next_city):
        taboo[previous_city][next_city] = 0
        taboo[next_city][previous_city] = 0

    def is_ant_stuck(self, next_city):
        return next_city == -1

    def report_step(self, next_city):
        if next_city != -1:
            print(f"-going to {next_city} searching {self.target_city}")
        else:
            print("STUCK")

    def is_path_not_found(self, previous_city):
        return previous_city != self.target_city and previous_city != -1

    def choose_next_city(self, eta, taboo, seed=None):
      
        pheromone_value = np.copy(taboo) 
        nominator = pheromone_value ** self.alpha * (eta ** self.beta)
        dominator = nominator.values.sum()
        prob = nominator / dominator
       
        if math.isnan(float((prob[0]))): 
            return -1
        
        actual_seed = seed if seed != None else self.seed
        if actual_seed != None:
            np.random.seed(actual_seed)
        next_city = np.random.choice( prob.index.array, 1, p = prob)[0]
        return next_city
        
    def count_distance(self, path):
        total = 0
        for i in range(len(path)-1):
            total += self.distances[path[i]][path[i+1]]
        return total


    def update_pheromone(self, paths):
        sorted_paths = sorted(paths , key = lambda x: x[1])
        for path , _ in sorted_paths:
            for i in range(len(path)-1):
                city1 = path[i]
                city2 = path[i+1]
                if self.type == 'das':
                    self.pheromones[city1][city2] += self.q_das
                else:
                    self.pheromones[city1][city2] += self.q_qas*self.eta[city1][city2]
        self.update_graph()

    def update_graph(self):
        for edge in self.graph.edges:
            self.graph.edges[edge]['pheromone'] = self.pheromones[edge[0]][edge[1]]

    
