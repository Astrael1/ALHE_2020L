import unittest
import aco
import numpy as np
import reader as rd


class TestAco(unittest.TestCase):
    file_path = 'test_data/aco_test_data.txt'
    start_city = 'Koblenz'
    target_city = 'Dortmund'

    def test_choose_next_city(self):
        start_city = 'Koblenz'
        target_city = 'Dortmund'
        expected_next_city = 'Koeln'

        aco_das = aco.ACO(
            start_city,
            target_city,
            ants_num =  50,
            graph=rd.getGraphFromFile(self.file_path),
            iteration_num = 10, 
            type = 'das',
            seed=1
            )
        
        taboo = aco_das.pheromones.copy()
        result = aco_das.choose_next_city(
            aco_das.eta[start_city],
            taboo[start_city]
            )
        self.assertEqual(result, expected_next_city)

    def test_choose_next_city_stuck(self):
        start_city = 'Frankfurt'
        target_city = 'Dortmund'
        expected_next_city = -1

        aco_das = aco.ACO(
            start_city,
            target_city,
            ants_num =  50,
            graph=rd.getGraphFromFile(self.file_path),
            iteration_num = 10, 
            type = 'das',
            seed=1
            )
        
        taboo = aco_das.pheromones.copy()
        result = aco_das.choose_next_city(
            aco_das.eta[start_city],
            taboo[start_city]
            )
        self.assertEqual(result, expected_next_city)

    def test_find_path(self):
        expected_path = ['Koblenz', 'Koeln', 'Duesseldorf', 'Essen', 'Dortmund']

        aco_das = aco.ACO(
            self.start_city,
            self.target_city,
            ants_num =  50,
            graph=rd.getGraphFromFile(self.file_path),
            iteration_num = 10, 
            type = 'das',
            seed=1
            )
        
        actual_path = aco_das.find_path()
        self.assertEqual(actual_path[0], self.start_city)
        self.assertListEqual(actual_path, expected_path)

    def test_find_paths(self):

        expected_path = ['Koblenz', 'Koeln', 'Duesseldorf', 'Essen', 'Dortmund']
        expected_dist = np.float64(170.34476288389095)

        aco_das = aco.ACO(
            self.start_city,
            self.target_city,
            ants_num =  1,
            graph=rd.getGraphFromFile(self.file_path),
            iteration_num = 1, 
            type = 'das',
            seed=1
            )
        
        paths = aco_das.find_paths()
        self.assertEqual(len(paths), 1)
        actual_path, actual_dist = paths[0]
        self.assertEqual(actual_path, expected_path)
        self.assertEqual(actual_dist, expected_dist)



if __name__ == '__main__':
    unittest.main()


