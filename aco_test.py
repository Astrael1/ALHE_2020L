import unittest
import aco


class TestAco(unittest.TestCase):

    def test_choose_next_city(self):
        start_city = 'Kempten'

        aco_das = aco.ACO(
            start_city,
            'Wuerzburg' ,
            ants_num =  50,
            iteration_num = 10, 
            type = 'das')
        
        taboo = aco_das.pheromones.copy()
        result = aco_das.choose_next_city(
            aco_das.pheromones[start_city],
            aco_das.eta[start_city],
            taboo[start_city],
            1
            )
        self.assertEqual(result, 'Konstanz')
        
        




if __name__ == '__main__':
    unittest.main()


