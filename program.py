import reader
import argparse
from time import process_time 
from aco import *

parser = argparse.ArgumentParser()
parser.add_argument("city_1", help='Starting city')
parser.add_argument("city_2", help='Ending city')
parser.add_argument("-a", "-ants", dest='ants', default=10, type=int, help='Number of ants in each iteration, default 10')
parser.add_argument("-i","-iterations", dest='iterations', default=3, type=int, help='Number of iterations, default 3')
parser.add_argument("-type", help='type of algorithm to use', default='qas', choices=['qas', 'das'])
parser.add_argument("-o", dest="output_path", default='', help="path to output file")
parser.add_argument("-v", dest='verbose', type=int, default=0, help='Set verbosity level 1 - only result 2 - route of particular ants')
parser.add_argument('-t', '-time', dest='display_time' , default=False, action='store_true', help='Display time of algorithm running')
parser.add_argument('-img', dest='visualize', default=False, action='store_true', help='Save visualization in \'results/\' directory (DO NOT REMOVE IT)')
args = parser.parse_args()

if args.verbose:
    print("Calculating path from {} to {} with algorithm {}. I will store it in {}"
        .format(args.city_1, args.city_2, args.type, args.output_path)) 


aco = ACO(
    args.city_1, 
    args.city_2, 
    ants_num=args.ants,
    iteration_num=args.iterations,
    verbosity = args.verbose, 
    shouldVisualize=args.visualize,
    type = args.type,
    qas=1
    )

t1_start = process_time()  
solution = aco.aco_run()
t1_stop = process_time() 
if(args.display_time):
    print(t1_stop - t1_start)
if(args.verbose >=1):
    for path in solution:
        print(path)
