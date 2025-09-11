def main():
    import sys
    sys.path.insert(0, '../src')

    import src.reader as rd # type: ignore
    import argparse
    from time import process_time 
    import src.aco as aco # type: ignore
    import os
    import src.visualizer as vz  # type: ignore

    parser = argparse.ArgumentParser()
    parser.add_argument("city_1", help='Starting city')
    parser.add_argument("city_2", help='Ending city')
    parser.add_argument("-a", "-ants", dest='ants', default=10, type=int, help='Number of ants in each iteration, default 10')
    parser.add_argument("-i","-iterations", dest='iterations', default=3, type=int, help='Number of iterations, default 3')
    parser.add_argument("-type", help='type of algorithm to use', default='qas', choices=['qas', 'das'])
    parser.add_argument("-v", dest='verbose', type=int, default=0, help='Set verbosity level 1 - only result 2 - route of particular ants')
    parser.add_argument('-t', '-time', dest='display_time' , default=False, action='store_true', help='Display time of algorithm running')
    parser.add_argument('-img', dest='visualize', default=False, action='store_true', help='Save visualization in \'results/\' directory (DO NOT REMOVE IT)')
    parser.add_argument('-vid', dest='video', default=False, action='store_true', help='Generate video in \'results/\' directory (DO NOT REMOVE IT)')
    args = parser.parse_args()

    if args.verbose:
        print("Calculating path from {} to {} with algorithm {}."
            .format(args.city_1, args.city_2, args.type))


    aco = aco.ACO(
        args.city_1, 
        args.city_2, 
        args.ants,
        rd.getGraphFromFile(os.getcwd() + "/germany50.txt"),
        iteration_num=args.iterations,
        verbosity = args.verbose, 
        shouldVisualize=args.visualize or args.video,
        type = args.type,
        qas=1,
        )

    t1_start = process_time()  
    solution, frames = aco.aco_run()
    t1_stop = process_time() 
    if(args.display_time):
        print(t1_stop - t1_start)
    if(args.verbose >=1):
        for path in solution:
            print(path)
    if(len(frames) == 0):
        print("Error: No frames to visualize")
        return
    visualizer = vz.Visualizer(frames, args.visualize, args.video)
    if args.video:
        visualizer.generate_video()
    elif args.visualize:
        visualizer.generate_images()

if __name__ == "__main__":
    main()


