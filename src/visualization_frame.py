import networkx as nx

class VisualizationFrame:
    """A class to represent a frame in the visualization of a pathfinding algorithm. 
    Frame number, start city, target city are kept in class variables."""
    serial_number = 0
    start_city: str
    target_city: str
    path: list

    def __init__(self, graph: nx.Graph, path, iteration_nr: int):
        self.serial_number = VisualizationFrame.serial_number
        VisualizationFrame.serial_number += 1

        self.graph = graph
        self.path = path
        self.iteration_nr = iteration_nr


    @classmethod
    def set_start_and_target(cls, start_city: str, target_city: str):
        cls.start_city = start_city
        cls.target_city = target_city