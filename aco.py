import random 
import numpy as np
import pandas as pd
import reader as rd
import math
from time import process_time 

class ACO:
    def __init__(self,city1, city2 ,ants_num, t = 'das', qas = 1,iteration_num = 10,rho = 0.5, alpha = 1, beta = 1, verbosity = 0):
        self.ants_num = ants_num
        self.iteration_num = iteration_num
        #self.best_ants = ants_num # number of best ants
        self.rho = rho # pr-stwo wyparowania pheromones
        self.alpha = alpha
        self.beta = beta
        self.city1 = city1
        self.city2 = city2
        self.graph, self.distances, self.pheromones, self.eta, self.cities, self.real_distance = rd.getGraphFromFile("germany50.txt")
        self.type = t
        self.q_qas = qas
        self.verbosity = verbosity


    def aco_run(self):
        path = None
        best_paths = [([],0)]
        y = 0
        t1_start = process_time() 
        for i in range(self.iteration_num):
            paths = self.find_paths()
            paths = [path for path in paths if path[0]]
            self.update_pheromone(paths)
            #print(paths)
            path = min(paths , key = lambda x : x[1])
            print(path)
            #lists.append(path)
            if path not in best_paths:       
                best_paths.append(path)
                y = y + 1
            else:
                continue
            
            self.pheromones * (1 - self.rho)
            # print(self.pheromones)

        # not choosing duplicated best paths
        best = sorted(best_paths , key = lambda x: x[1])
        t1_stop = process_time() 
        t1 = t1_stop - t1_start
        
        if best[1:3]:
            return [(best[1:3],t1)] 
        return [(best_paths[1:], t1)]
   
    def find_paths(self):
        paths = []
        cities = [self.city1, self.city2]
        for i in range(self.ants_num):
            path = self.find_path(cities)
            paths.append((path, self.count_distance(path)[0], self.count_distance(path)[1]))
        return paths 

    def find_path(self, city):
        path = []
        #taboo = set()
        taboo = self.pheromones.copy()
        end = self.cities.index(city[1])
        start = self.cities.index(city[0])
       
        prev = self.cities[start]
      
        while True:
            nex = self.choose(self.pheromones[prev], self.eta[prev],taboo[prev])
            
            # ant could not find the way
            if nex == 7:
                path.clear()
                break

   
            if nex[1] == end:
                path.append((prev,nex[0]))
                break

            path.append((prev,nex[0]))
            taboo[prev][nex[0]] = 0
            taboo[nex[0]][prev] = 0
            prev = nex[0]
               
        
        return path

    def choose(self, pheromone , eta, taboo):
      
        ph = np.copy(taboo) 
        nominator = ph ** self.alpha * (eta ** self.beta)
        dominator = nominator.values.sum()
        prob = nominator / dominator
       
        if math.isnan(float((prob[0]))):
            return 7
        nex = np.random.choice( range(len(self.cities)) ,1, p = prob)[0]
        
        return self.cities[nex] , nex
        
    def count_distance(self, path):
        total = 0.0
        real = 0.0
        
        for city in path:
            total += self.distances[city[0]][city[1]]
            real += self.real_distance[city[0]][city[1]]
        
        return total, real

    def update_pheromone(self, paths):
        sort_paths = sorted(paths , key = lambda x: x[1])
        for path , distance, real in sort_paths:
            for city in path:
                if self.type == 'das': 
                    self.pheromones[city[0]][city[1]] += self.eta[city[0]][city[1]]
                else:
                    self.pheromones[city[0]][city[1]] += self.q_qas

    
