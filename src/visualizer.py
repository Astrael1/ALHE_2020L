import networkx as nx
import matplotlib.pyplot as pl
import numpy as np
import imageio



from visualization_frame import VisualizationFrame

class Visualizer:
    img_width = 10
    img_height = 10
    def __init__(self, frames: list, save_images = True, save_video = False):
        self.frames = frames
        self.layout = nx.kamada_kawai_layout(self.frames[0].graph)
        self.save_images = save_images
        self.save_video = save_video


    def generate_video(self):
        fps = 1
        output_filename = './results/aco_video.mp4'
        video_frames = self.generate_images()
        imageio.mimwrite(output_filename, video_frames, fps=fps)


    def generate_images(self):
        video_frames = []
        for frame in self.frames:
            video_frames.append(self.visualize_frame(frame))
        return video_frames
            

    def visualize_frame(self, frame: VisualizationFrame):
        graph = frame.graph
        
        # make directional graph with path to show
        edge_colors = self.getEdgeColors(graph)
        edge_width = self.getEdgeWidth(graph)
        path = frame.path
        
        # draw
        fig = pl.figure(1, figsize=(self.img_width, self.img_height), dpi=100.0)
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
        
        ant_part = f", Ant: {frame.ant_nr + 1}" if frame.ant_nr != None else ""
        figtext = f"Iteration: {frame.iteration_nr}{ant_part}\nAlpha: {VisualizationFrame.alpha}, Beta: {VisualizationFrame.beta}, Rho: {VisualizationFrame.rho}\nStart: {VisualizationFrame.start_city}, Target: {VisualizationFrame.target_city}"

        if path == None:
            figtext += "\nPheromone levels after iteration."
        else:
            figtext += f"\nPath found"

        pl.figtext(0.5, 0.01, figtext, wrap=True, fontsize=12, verticalalignment='bottom', horizontalalignment='center')
        fig.canvas.draw()
        image = np.array(fig.canvas.renderer.buffer_rgba())

        if self.save_images:
            pl.savefig('results/'+str(frame.serial_number)+'.png', format='png')
        pl.close(1)
        return image

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