import unittest
import reader as rd
import pandas as pd
import networkx as nx



class TestReader(unittest.TestCase):
    file_path = 'test_data/test_data.txt'

    def test_getNodes(self):
        expected_nodes = [['Aachen', '6.04', '50.76'], ['Dortmund', '7.45', '51.51'], ['Duesseldorf', '6.77', '51.25'], ['Essen', '7.02', '51.46'], ['Koblenz', '7.52', '50.40'], ['Koeln', '6.87', '50.94'], ['Wesel', '6.37', '51.39']]
        file = open(self.file_path, "r")
        content=file.read()
        nodes = rd.get_nodes(content)
        self.assertListEqual(nodes, expected_nodes)

    def test_getLinks(self):
        expectedLinks = [['Duesseldorf', 'Essen'], ['Dortmund', 'Essen'], ['Wesel', 'Essen'], ['Koeln', 'Duesseldorf'], ['Aachen', 'Koeln'], ['Koblenz', 'Koeln']];
        file = open(self.file_path, "r")
        content=file.read()
        links = rd.get_links(content)
        self.assertListEqual(links, expectedLinks)
        

    def test_reading_file(self):

        distance_expected_data = [
            [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 61.786093, 0.000000],
            [0.000000, 0.000000, 0.000000, 30.382778, 0.000000, 0.000000, 0.000000],
            [0.000000, 0.000000, 0.000000, 29.140037, 0.000000, 35.191831, 0.000000],
            [0.000000, 30.382778, 29.140037, 0.000000, 0.000000, 0.000000, 45.876092],
            [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 75.630117, 0.000000],
            [61.786093, 0.000000, 35.191831, 0.000000, 75.630117, 0.000000, 0.000000],
            [0.000000, 0.000000, 0.000000, 45.876092, 0.000000, 0.000000, 0.000000]
        ]

        pheromone_expected_data = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
        ]

        expected_cities = ['Aachen', 'Dortmund', 'Duesseldorf', 'Essen', 'Koblenz', 'Koeln', 'Wesel']
        distance_df_expected = pd.DataFrame(distance_expected_data, index=expected_cities, columns=expected_cities)
        pheromone_df_expected = pd.DataFrame(pheromone_expected_data, index=expected_cities, columns=expected_cities)
        graph, _, _, _, cities = rd.getGraphFromFile("test_data/test_data.txt")

        self.assertListEqual(cities, expected_cities)
        distance_df_actual = nx.to_pandas_adjacency(graph, nonedge=0, dtype=float)
        pheromone_df_actual = nx.to_pandas_adjacency(graph, weight='pheromone', nonedge=0, dtype=float)
        self.assertEqual(round(distance_df_expected).equals(round(distance_df_actual)), True)
        self.assertEqual(round(pheromone_df_expected).equals(round(pheromone_df_actual)), True)
        self.assertListEqual(distance_df_actual.columns.to_list(), expected_cities)



if __name__ == '__main__':
    unittest.main()


