import reader
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("city_1", help='Starting city')
parser.add_argument("city_2", help='Ending city')
parser.add_argument("-qas")
args = parser.parse_args()