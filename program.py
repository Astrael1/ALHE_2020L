import reader
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("city_1", help='Starting city')
parser.add_argument("city_2", help='Ending city')
parser.add_argument("type", help='type of algorithm to use', default='qas', choices=['qas', 'das'])
parser.add_argument("-o", dest="output_path", help="path to output file")
args = parser.parse_args()

print("Calculating path from {} to {} with algorithm {}. I will store it in {}"
    .format(args.city_1, args.city_2, args.type, args.output_path))