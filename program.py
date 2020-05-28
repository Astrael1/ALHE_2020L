import reader
import argparse
from aco import *

parser = argparse.ArgumentParser()
parser.add_argument("city_1", help='Starting city')
parser.add_argument("city_2", help='Ending city')
#parser.add_argument("type", help='type of algorithm to use', default='qas', choices=['qas', 'das'])
#parser.add_argument("-o", dest="output_path", help="path to output file")
args = parser.parse_args()

print("Calculating path from {} to {} with algorithm ."
    .format(args.city_1, args.city_2)) #   I will store it in {}  , args.type , args.output_path

#  python3 program.py  Kempten Wuerzburg 
aco = ACO(args.city_1, args.city_2, 10, verbosity=1, max_paths=100)
solution = aco.aco_run()
for path in solution:
    print(path)