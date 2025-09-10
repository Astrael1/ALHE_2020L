import networkx as nx
import matplotlib.pyplot as pl
import matplotlib.patches as mpatches
from matplotlib.widgets import TextBox


from visualization_frame import VisualizationFrame

class Visualizer:
    def __init__(self, frames: list):
        self.frames = frames
        self.layout = nx.kamada_kawai_layout(self.frames[0].graph)

    def generate_images(self):
        for frame in self.frames:
            self.visualize_frame(frame)

    def visualize_frame(self, frame: VisualizationFrame):
        graph = frame.graph
        
        # make directional graph with path to show
        edge_colors = self.getEdgeColors(graph)
        edge_width = self.getEdgeWidth(graph)
        path = frame.path
        
        # draw
        pl.figure(1, figsize=(10,10))
        nx.draw_networkx(
            graph,
            pos=self.layout, 
            with_labels=True,
            font_size=7,
            node_color='#ffaa77',
            edge_color=edge_colors,
            width=edge_width,
            node_shape='o')
        if path != None:
            self.draw_path(path)
        
        figtext = f"Iteration: {frame.iteration_nr}\nAlpha: {VisualizationFrame.alpha}, Beta: {VisualizationFrame.beta}, Rho: {VisualizationFrame.rho}\nStart: {VisualizationFrame.start_city}, Target: {VisualizationFrame.target_city}"

        if path == None:
            figtext += "\nPheromone levels after iteration."
        else:
            figtext += f"\nPath found"

        pl.figtext(0.5, 0.01, figtext, wrap=True, fontsize=12, verticalalignment='bottom', horizontalalignment='center')

        pl.savefig('results/'+str(frame.serial_number)+'.png', format='png')
        pl.close(1)

    def draw_path(self, path):
        path_graph = nx.DiGraph()
        for i in range(len(path)-1):
            path_graph.add_edge(path[i], path[i+1])
        nx.draw_networkx(
                path_graph,
                pos=self.layout, 
                nodelist=path,
                with_labels=False,
                node_color='#ff0000',
                node_shape='o')

    def getEdgeColors(self, graph):
        return [self.pheromoneToColor(edge, graph) for edge in graph.edges]
    def getEdgeWidth(self, graph):
        return [self.pheromoneToWidth(edge, graph) for edge in graph.edges]

    def pheromoneToColor(self, edge, graph):
        pheromone = graph[edge[0]][edge[1]]['pheromone']
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
    def pheromoneToWidth(self, edge, graph):
        pheromone = graph[edge[0]][edge[1]]['pheromone']
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