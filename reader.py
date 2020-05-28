import networkx as nx
import numpy as np
import math
import matplotlib.pyplot as pl
import pandas as pd
from scipy.spatial import distance_matrix

def getGraphFromFile(file_path):
    file = open(file_path, "r")
    graph = nx.Graph()
    content=file.read()
    # dictionary with coordinates of nodes
    coords = {}    
    cities = []
    # 
    # turninig on options to see all information in DataFrame
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)

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

    for link in links:
        link = link[ link.find("(")+1: link.find(")")].split(' ')[1:-1]
        # print(coords[link[0]]["x"])
        x1 = float(coords[link[0]]["x"])
        y1 = float(coords[link[0]]["y"])
        x2 = float(coords[link[1]]["x"])
        y2 = float(coords[link[1]]["y"])
        dx = x2 - x1
        dy = y2 - y1
        edge_length = math.sqrt( dx ** 2 + dy ** 2 )
        graph.add_edge(link[0],link[1])
        graph[link[0]][link[1]]['weight'] = edge_length
        graph[link[0]][link[1]]['pheromone'] = 1
        # graph.add_weighted_edges_from([(link[0], link[1], edge_length)])
    # 
    # distance dataframe
    df = nx.to_pandas_adjacency(graph, weight='weight', nonedge=np.inf)
    
    
    # beginnine pheromone amount for each city in dataframe
    pheromone = nx.to_pandas_adjacency(graph, weight='pheromone', nonedge=0)
    #
    # or all matrix with ones
    # pheromone = pd.DataFrame( 1 , index = cities , columns = cities)
    # 
    # beginning eta amount for each citi in dataframe
    eta = 1 /df 
    
    return graph, df , pheromone ,eta , cities


# getGraphFromFile("germany50.txt")
# print(getGraphFromFile("germany50.txt")[1])


# ----------------------drawing graph (for future use)------------------------------
# graph, df, pheromone, eta, cities = getGraphFromFile('germany50.txt')
# nx.draw_kamada_kawai(graph, nodelist=cities, with_labels=True)
# pl.draw()
# pl.savefig('graph.png')
# pl.show()
