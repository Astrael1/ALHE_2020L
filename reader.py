import networkx as nx
import numpy as np
import math
import matplotlib.pyplot as pl
import pandas as pd
from scipy.spatial import distance_matrix
from geopy.distance import geodesic


def getGraphFromFile(file_path):
    file = open(file_path, "r")
    graph = nx.Graph()
    content=file.read()
    # dictionary with coordinates of nodes
    coords = {}    
    cities = []
    # 
    # turninig on options to see all information in DataFrame
    #pd.set_option('display.max_rows', None)
    #pd.set_option('display.max_columns', None)

    # extract node section
    node_section = content[content.find("NODES"):content.find("LINK")]
    # extract nodes only
    node_section = node_section[node_section.find("(") + 1: node_section.rfind(")")]
    # split into single nodes
    nodes = node_section.split('\n')[1:-1]

    for node in nodes:
        # get list with name on 0 index and two coordinates
        node = node.replace('(', '').replace(')', '').split(' ')[2:-1]
        node.pop(1)
        cities.append(node[0])
        coords[node[0]] = {"x":node[1], "y": node[2]}
        graph.add_node(node[0])
    # extract link section
    link_section = content[content.find("LINKS"):content.find("DEMAND")]
    link_section = link_section[link_section.find("(") + 1: link_section.rfind(")")]
    links = link_section.split('\n')[1:-1]
    #print(links)
    for link in links:
        link = link[ link.find("(")+1: link.find(")")].split(' ')[1:-1]
 
        lon1 = float(coords[link[0]]["x"]) # lon
        lat1 = float(coords[link[0]]["y"]) # lat

        lon2 = float(coords[link[1]]["x"])
        lat2 = float(coords[link[1]]["y"])
        
        edge_real_distance = geodesic((lat1,lon1), (lat2,lon2)).kilometers
        graph.add_edge(link[0],link[1])
        graph[link[0]][link[1]]['weight'] = edge_real_distance
        graph[link[0]][link[1]]['pheromone'] = 1
        
    # 
    # distance dataframe
    df = nx.to_pandas_adjacency(graph, weight='weight', nonedge=np.inf)
    # beginnine pheromone amount for each city in dataframe
    pheromone = nx.to_pandas_adjacency(graph, weight='pheromone', nonedge=0)
  
    # 
    # beginning eta amount for each citi in dataframe
    eta = 1 /df 
    
    return graph, df , pheromone ,eta , cities

