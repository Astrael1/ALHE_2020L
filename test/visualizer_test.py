import sys
sys.path.insert(0, '../src')

import unittest
import aco  # type: ignore
import numpy as np
import reader as rd # type: ignore
import visualizer as vz  # type: ignore


class TestVisualizer(unittest.TestCase):
    file_path = 'test_data/aco_test_data.txt'
    start_city = 'Koblenz'
    target_city = 'Dortmund'

    def test_visualization_frames(self):
        aco_das = aco.ACO(
            self.start_city,
            self.target_city,
            ants_num =  3,
            graph=rd.getGraphFromFile(self.file_path),
            iteration_num = 3, 
            type = 'das',
            shouldVisualize=True,
            seed=1
            )
        
        _, frames = aco_das.aco_run()
        self.assertIsNotNone(frames)
        self.assertGreater(len(frames), 0)
        self.assertEqual(frames[0].iteration_nr, 0)

        visualizer = vz.Visualizer(frames, False, False)
        visualizer.generate_images()

    def test_video_generation(self):
        aco_das = aco.ACO(
            self.start_city,
            self.target_city,
            ants_num =  3,
            graph=rd.getGraphFromFile(self.file_path),
            iteration_num = 3, 
            type = 'das',
            shouldVisualize=True,
            seed=1
            )
        
        _, frames = aco_das.aco_run()
        self.assertIsNotNone(frames)
        self.assertGreater(len(frames), 0)
        self.assertEqual(frames[0].iteration_nr, 0)

        visualizer = vz.Visualizer(frames, False, True)
        visualizer.generate_video()
            
        



if __name__ == '__main__':
    unittest.main()


