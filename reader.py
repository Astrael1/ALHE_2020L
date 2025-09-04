import networkx as nx
import numpy as np
from geopy.distance import geodesic

def get_nodes(file_content):
    node_section = file_content[file_content.find("NODES"):file_content.find("LINK")]
    node_section = node_section[node_section.find("(") + 1: node_section.rfind(")")]
    return [node.strip().replace('( ', '').replace(' )', '').split(' ') 
            for node in node_section.split('\n')[1:-1]]

def get_links(file_content):
    link_section = file_content[file_content.find("LINKS"):file_content.find("DEMAND")]
    link_section = link_section[link_section.find("(") + 1: link_section.rfind(")")]
    return [link[ link.find("(")+1: link.find(")")].strip().split(' ') for link in link_section.split('\n')[1:-1]]

def edge_from_link(link, coords):
    lon1 = coords[link[0]]["x"]
    lat1 = coords[link[0]]["y"]

    lon2 = coords[link[1]]["x"]
    lat2 = coords[link[1]]["y"]
    edge_real_distance = geodesic((lat1,lon1), (lat2,lon2)).kilometers
    return (link[0], link[1], {'weight': edge_real_distance, 'pheromone': 1})


def getGraphFromFile(file_path):
    file = open(file_path, "r")
    graph = nx.Graph()
    content=file.read()
    nodes = get_nodes(content)
    cities = [ node[0] for node in nodes ]
    coords = { node[0]: {"x": float(node[1]), "y": float(node[2])} for node in nodes }

    graph.add_nodes_from(cities)
    links = get_links(content)
    edges = [edge_from_link(link, coords) for link in links]
    graph.add_edges_from(edges)
        
    # 
    # distance dataframe
    df = nx.to_pandas_adjacency(graph, weight='weight', nonedge=np.inf)
    # beginnine pheromone amount for each city in dataframe
    pheromone = nx.to_pandas_adjacency(graph, weight='pheromone', nonedge=0)
  
    # 
    # beginning eta amount for each citi in dataframe
    eta = 1 /df 
    
    return graph, df , pheromone ,eta , cities

