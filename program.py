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
aco = ACO(args.city_1, args.city_2, 100,'das')

#aco.aco_run()[0][1]


for best, time  in aco.aco_run() :
    for b in best:
        print(str(b[0])+" "+ str(b[1]) +" "+ str(b[2]))
    print(time)
   
#print(aco.aco_run())