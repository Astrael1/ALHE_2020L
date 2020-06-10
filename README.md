# ALHE_2020L
usage: program.py [-h] [-a ANTS] [-i ITERATIONS] [-type {qas,das}]
                  [-o OUTPUT_PATH] [-v VERBOSE] [-t] [-img]
                  city_1 city_2

positional arguments:
  city_1                Starting city
  city_2                Ending city

optional arguments:
  -h, --help            show this help message and exit
  -a ANTS, -ants ANTS   Number of ants in each iteration, default 10
  -i ITERATIONS, -iterations ITERATIONS
                        Number of iterations, default 3
  -type {qas,das}       type of algorithm to use
  -o OUTPUT_PATH        path to output file
  -v VERBOSE            Set verbosity level 1 - only result 2 - route of
                        particular ants
  -t, -time             Display time of algorithm running
  -img                  Save visualization in 'results/' directory (DO NOT
                        REMOVE IT)
