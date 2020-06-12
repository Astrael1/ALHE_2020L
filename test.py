#from aco import *
#import unittest
from time import process_time 
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic
from aco import *


class TestAco(unittest.TestCase):
    def test_def_das_qas(self):
        aco_das = ACO('Kempten','Wuerzburg' , 10, 'das')
        aco_qas =ACO('Kempten','Wuerzburg' , 10, t = 'qas')
        aco_das.run()
        aco_qas.run()
        self.assertGreaterEqual(a,b)





