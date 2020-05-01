import networkx as nx
import math

def getGraphFromFile(file_path):
    file = open(file_path, "r")
    graph = nx.Graph()
    content=file.read()
    # dictionary with coordinates of nodes
    coords = {}

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
        graph.add_weighted_edges_from([(link[0], link[1], edge_length)])
    return graph

# getGraphFromFile("germany50.txt")
print(getGraphFromFile("germany50.txt"))

