#from aco import *
import unittest

import aco
from time import process_time 


class TestAco(unittest.TestCase):
    def test_def_das_qas(self):
        aco_das = aco.ACO('Kempten','Wuerzburg' , 10,3, 'das')
        aco_qas =aco.ACO('Kempten','Wuerzburg' , 10,3,'qas')
        t1_start = process_time()  
        aco_das.aco_run()
        t1_stop = process_time() 

        t1 = t1_stop - t1_start

        t2_start = process_time()  
        aco_qas.aco_run()
        t2_stop = process_time()  

        t2 = t2_stop - t2_start
        self.assertGreaterEqual(t2,t1)



if __name__ == '__main__':
    unittest.main()


