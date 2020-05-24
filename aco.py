import random 
import numpy as np
import pandas as pd
import reader as rd
import math

class ACO:
    def __init__(self,city1, city2 ,ants_num, t = 'qas', qas = 1,iteration_num = 3,rho = 0.5, alpha = 1, beta = 1):
        self.distances = rd.getGraphFromFile("germany50.txt")[1]
        self.ants_num = ants_num
        self.iteration_num = iteration_num
        self.best_ants = ants_num # number of best ants
        self.rho = rho # pr-stwo wyparowania pheromones
        self.alpha = alpha
        self.beta = beta
        self.pheromones = rd.getGraphFromFile("germany50.txt")[2] 
        self.eta = rd.getGraphFromFile("germany50.txt")[3] # 1 / distances
        self.city1 = city1
        self.city2 = city2
        self.cities = rd.getGraphFromFile("germany50.txt")[4]
        self.type = t
        self.q_qas = qas

    def aco_run(self):
        path = None
        best_paths = []

        # end = self.cities.index(self.city2)
        # start = self.cities.index(self.city1)
        
        # self.pheromones = self.pheromones[start].replace(1, 5)
        # self.pheromones = self.pheromones[end].replace(1,5)

        for i in range(self.iteration_num):
            paths = self.find_paths()
            self.update_pheromone(paths, self.best_ants)
            #print(paths)
            path = min(paths , key = lambda x : x[1])            
            best_paths.append(path)
            # jeżeli powtarza się w best weź inny w paths?
            self.pheromones * (1 - self.rho)

        # choosing duplicated best paths
        best = sorted(best_paths , key = lambda x: x[1])
        print(best)
        return best[:2]
   
    def find_paths(self):
        paths = []
        cities = [self.city1, self.city2]
        for i in range(self.ants_num):
            path = self.find_path(cities)
            paths.append((path, self.count_distance(path)))
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
                break

            # print(nex[0])
            # ant found the end 
            if nex[1] == end:
                path.append((prev,nex[0]))
                print(" Found it ")
                break

            path.append((prev,nex[0]))
            taboo[prev][nex[0]] = 0
            taboo[nex[0]][prev] = 0
            prev = nex[0]
               
        #path.append((prev,self.cities[0]))
        return path

    def choose(self, pheromone , eta, taboo):
      
        ph = np.copy(taboo) 
        nominator = ph ** self.alpha * (eta ** self.beta)
        dominator = nominator.values.sum()
        prob = nominator / dominator
        print("nom : {} pheromone : {} dominator {}".format(nominator, ph, dominator))
        print(prob)
        if math.isnan(float((prob[0]))):
            print(" Error ") 
            return 7
        nex = np.random.choice( range(len(self.cities)) ,1, p = prob)[0]
        print(nex)
        return self.cities[nex] , nex
        
    def count_distance(self, path):
        total = 0
        for city in path:
            total += self.distances[city[0]][city[1]]
        return total

    def update_pheromone(self, paths, best_ants):
        sort_paths = sorted(paths , key = lambda x: x[1])
        for path , distance in sort_paths[:best_ants]:
            for city in path:
                if self.type == 'das': 
                    self.pheromones[city[0]][city[1]] += self.eta[city[0]][city[1]]
                else:
                    self.pheromones[city[0]][city[1]] += self.q_qas

    
