#from aco import *
import unittest

import aco
from time import process_time 


class TestAco(unittest.TestCase):
    def test_def_das_qas_less(self): # rho = 0.5
        aco_das = aco.ACO(
            'Kempten',
            'Wuerzburg' ,
            ants_num =  50,
            iteration_num = 10, 
            type = 'das')
        aco_qas =aco.ACO(
            'Kempten',
            'Wuerzburg' ,
            ants_num = 50,
            iteration_num = 10,
            type='qas')
        t1_start = process_time()  
        aco_das.aco_run()
        t1_stop = process_time() 

        t1 = t1_stop - t1_start

        t2_start = process_time()  
        aco_qas.aco_run()
        t2_stop = process_time()  

        t2 = t2_stop - t2_start
        
        self.assertLessEqual(t1,t2)


    def test_rho__das_qas_less(self): # rho = 0.9
        aco_das = aco.ACO(
            'Kempten',
            'Wuerzburg' ,
            ants_num =  50,
            iteration_num = 10, 
            type = 'das',
            rho=0.9)
        aco_qas =aco.ACO(
            'Kempten',
            'Wuerzburg' ,
            ants_num = 50,
            iteration_num = 10,
            type='qas',
            rho = 0.9)
        t1_start = process_time()  
        aco_das.aco_run()
        t1_stop = process_time() 

        t1 = t1_stop - t1_start

        t2_start = process_time()  
        aco_qas.aco_run()
        t2_stop = process_time()  

        t2 = t2_stop - t2_start
        

        self.assertLessEqual(t1,t2)


    def test_no_rho__das_qas_less(self): # rho = 0.0
        aco_das = aco.ACO(
            'Kempten',
            'Wuerzburg' ,
            ants_num =  50,
            iteration_num = 10, 
            type = 'das',
            rho=0.0)
        aco_qas =aco.ACO(
            'Kempten',
            'Wuerzburg' ,
            ants_num = 50,
            iteration_num = 10,
            type='qas',
            rho = 0.0)
        t1_start = process_time()  
        aco_das.aco_run()
        t1_stop = process_time() 

        t1 = t1_stop - t1_start

        t2_start = process_time()  
        aco_qas.aco_run()
        t2_stop = process_time()  

        t2 = t2_stop - t2_start
        
        self.assertLessEqual(t1,t2) 


    def test_alpha_das_qas_less(self):   # alpha = 0.1
        aco_das = aco.ACO(
            'Kempten',
            'Wuerzburg' ,
            ants_num =  50, 
            iteration_num= 10,
            type = 'das',
            rho= 0.4,
            beta = 1,
            alpha=0.1) # rho = 0.9
        aco_qas =aco.ACO(
            'Kempten',
            'Wuerzburg' ,
            ants_num =  50,
            iteration_num = 10,
            type='qas',
            rho = 0.4,
            beta = 1,
            alpha= 0.1)
        t1_start = process_time()  
        aco_das.aco_run()
        t1_stop = process_time() 

        t1 = t1_stop - t1_start

        t2_start = process_time()  
        aco_qas.aco_run()
        t2_stop = process_time()  

        t2 = t2_stop - t2_start
        self.assertLessEqual(t1,t2)


    def test_beta_das_qas_less(self):  # beta = 0.1
        aco_das = aco.ACO(
            'Kempten',
            'Wuerzburg' ,
            ants_num = 50,
            iteration_num =10,
            type = 'das',
            rho = 0.4,
            beta = 0.1,
            alpha = 1) # rho = 0.9
        aco_qas =aco.ACO(
            'Kempten',
            'Wuerzburg' ,
            ants_num = 50,
            iteration_num = 10,
            type = 'qas',
            rho = 0.4,
            beta = 0.1,
            alpha=1)
        t1_start = process_time()  
        aco_das.aco_run()
        t1_stop = process_time() 

        t1 = t1_stop - t1_start

        t2_start = process_time()  
        aco_qas.aco_run()
        t2_stop = process_time()  

        t2 = t2_stop - t2_start
        self.assertLessEqual(t1,t2)


    def test_alpha_beta_das_qas_less(self):  # beta = 0.5 alpha = 0.5
        aco_das = aco.ACO(
            'Kempten',
            'Wuerzburg' ,
            ants_num = 50,
            iteration_num =10,
            type = 'das',
            rho = 0.4,
            beta = 0.5,
            alpha = 0.5) # rho = 0.9
        aco_qas =aco.ACO(
            'Kempten',
            'Wuerzburg' ,
            ants_num = 50,
            iteration_num = 10,
            type = 'qas',
            rho = 0.4,
            beta = 0.5,
            alpha=0.5)
        t1_start = process_time()  
        aco_das.aco_run()
        t1_stop = process_time() 

        t1 = t1_stop - t1_start

        t2_start = process_time()  
        aco_qas.aco_run()
        t2_stop = process_time()  

        t2 = t2_stop - t2_start
        self.assertLessEqual(t1,t2)


    def test_100_das_qas_less(self): # rho = 0.5
        aco_das = aco.ACO(
            'Kempten',
            'Wuerzburg' ,
            ants_num =  100,
            iteration_num = 20, 
            type = 'das',
            rho = 0)
        aco_qas =aco.ACO(
            'Kempten',
            'Wuerzburg' ,
            ants_num = 100,
            iteration_num = 20,
            type='qas',
            rho = 0)
        t1_start = process_time()  
        aco_das.aco_run()
        t1_stop = process_time() 

        t1 = t1_stop - t1_start

        t2_start = process_time()  
        aco_qas.aco_run()
        t2_stop = process_time()  

        t2 = t2_stop - t2_start
        
        self.assertLessEqual(t1,t2)



if __name__ == '__main__':
    unittest.main()


