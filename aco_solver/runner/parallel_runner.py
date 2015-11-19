from multiprocessing import Process, Pipe
from optparse import OptionParser
import os
import pickle
import sys

from aco_solver.algorithm import graph
from aco_solver.algorithm.results import ResultConverter
from aco_solver.utils.cities_reader import CitiesReader
from aco_solver.algorithm.ant_colony import ControlSampleColony, HighAltercentricityCondition, \
    LowAltercentricityCondition, \
    ClassicAntColony, ParametrizedColony
from aco_solver.algorithm.graph import Graph


def start_simulation(ants_count, iterations, distance_matrix, positions, rho, q, type, alpha, beta, pipe, egocentric=None, altercentric=None, goodConflict=None, badConflict=None, classic=None, name=None):
    colony = None
    if type == "ca":  # Classical Ants
        graph = Graph(distance_matrix, positions, rho, q, 0.01, alpha, beta)
        colony = ClassicAntColony(ants_count, graph, alpha, beta, iterations)
    elif type == "cs":  # Control Sample
        graph = create_graph_with_default_pheromone_value(distance_matrix, positions, rho, q, alpha, beta)
        colony = ControlSampleColony(ants_count, graph, iterations)
    elif type == "ha":  # High Altercentricity Condition
        graph = create_graph_with_default_pheromone_value(distance_matrix, positions, rho, q, alpha, beta)
        colony = HighAltercentricityCondition(ants_count, graph, iterations)
    elif type == "la":  # Low Altercentricity Condition
        graph = create_graph_with_default_pheromone_value(distance_matrix, positions, rho, q, alpha, beta)
        colony = LowAltercentricityCondition(ants_count, graph, iterations)
    elif type == "pc":  # Parametrized Colony
        graph = create_graph_with_default_pheromone_value(distance_matrix, positions, rho, q, alpha, beta)
        colony = ParametrizedColony(ants_count, graph, iterations, egocentric, altercentric, goodConflict, badConflict, classic, alpha, beta, name)

    result = colony.start_simulation()
    # to avoid problems with deep recursion while serializing large objects with pickle
    sys.setrecursionlimit(30000)
    pipe.send(pickle.dumps(result))


def create_graph_with_default_pheromone_value(cities_distances, positions, rho, q, alpha, beta):
    return Graph(cities_distances, positions, rho, q, (1.0 / graph.compute_average_distance(cities_distances)) ** 2.0, alpha, beta)


def main():
    usage = "usage: %prog [options] number_of_ants iterations dataset_name [-e egocentric_no -a altercentric_no" \
            " -gc goodconflict_no -bc badconflict_no]"

    parser = OptionParser(usage=usage)
    parser.add_option("-t", "--type", default="cs", type="string", dest="type")
    parser.add_option("-a", "--alpha", default="3.0", type="float", help="pheromone influence [default: %default]",
                      dest="alpha")
    parser.add_option("-b", "--beta", default="2.0", type="float", help="distance influence [default: %default]",
                      dest="beta")
    parser.add_option("-r", "--rho", default="0.01", type="float",
                      help="pheromone evaporation coefficient [default: %default]",
                      dest="rho")
    parser.add_option("-q", "--q", default="2.0", type="float", help="pheromone deposit factor [default: %default]",
                      dest="q")
    parser.add_option("-p", "--p", default="1", type="int", help="number of processes [default: %default]",
                      dest="p")
    parser.add_option("-w", "--egocentric", default="0.25", type="float",
                      help="percent of egocentric ants in colony [default: %default]", dest="egocentric")
    parser.add_option("-x", "--altercentric", default="0.25", type="float",
                      help="percent of altercentric ants in colony [default: %default]", dest="altercentric")
    parser.add_option("-y", "--goodConflict", default="0.25", type="float",
                      help="percent of good conflict ants in colony [default: %default]", dest="goodConflict")
    parser.add_option("-z", "--badConflict", default="0.25", type="float",
                      help="percent of bad conflict ants in colony [default: %default]", dest="badConflict")
    parser.add_option("-v", "--classic", default="0.0", type="float",
                      help="percent of classic ants in colony [default: %default]", dest="classic")
    parser.add_option("-o", "--outputdir", default="outputs/", type="string",
                      help="output directory [default: %default]", dest="outputdir")
    parser.add_option("-n", "--paremetrizedName", default="pc", type="string",
                      help="name of parametrized colony [default: %default", dest="name")

    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("incorrect number of arguments")

    ants_count = int(args[0])
    iterations = int(args[1])
    cities_filename = args[2]

    cities_reader = CitiesReader(cities_filename)
    cities_reader.read_file()
    distance_matrix = cities_reader.create_distance_matrix()
    positions = cities_reader.get_positions()

    print "File:", cities_filename, "Type:", options.type, "Ants:", ants_count, "Iterations:", iterations

    processes = []
    pipes = []
    # start concurrent processes
    for i in range(options.p):
        pipes.append(Pipe(False))
    for i in range(options.p):
        if options.type == "pc":
            processes.append(Process(target=start_simulation, args=(
                ants_count, iterations, distance_matrix, positions, options.rho, options.q, options.type, options.alpha,
                options.beta, pipes[i][1], options.egocentric, options.altercentric, options.goodConflict,
                options.badConflict, options.classic, options.name)))
        else:
            processes.append(Process(target=start_simulation, args=(
                ants_count, iterations, distance_matrix, positions, options.rho, options.q, options.type, options.alpha,
                options.beta, pipes[i][1])))
    for i in range(options.p):
        processes[i].start()

    best_result = None
    result_list = []
    for i in range(options.p):
        present_result = pickle.loads(pipes[i][0].recv())

        if best_result is None or present_result.best_path < best_result.best_path:
            best_result = present_result

        result_list.append(present_result)

    output_directory_name = options.outputdir
    if not os.path.exists(output_directory_name):
        os.makedirs(output_directory_name)

    type_name = options.type
    if (options.name != 'pc'):
      type_name = options.name
      f = open(output_directory_name + cities_filename + '_'
             + str(ants_count) + '_'
             + str(iterations) + '_'
             + type_name + '_config.dat', 'w')
      config = 'Egocentric: ' + str(options.egocentric) + '\nAltercentric: ' + str(options.altercentric) + '\nGood at conflict: ' + str(options.goodConflict) + '\nBad at conflict: ' + str(options.badConflict)
      f.write(config)
      f.close()

    for i in range(len(result_list)):
        f = open(output_directory_name + cities_filename + '_'
                 + str(ants_count) + '_'
                 + str(iterations) + '_'
                 + type_name + '_' + str(i) + '.dat', 'w')
        f.write(str(result_list[i]))
        f.close()

    f = open(output_directory_name + cities_filename + '_'
             + str(ants_count) + '_'
             + str(iterations) + '_'
             + type_name + '_best.dat', 'w')
    f.write(str(best_result))
    f.close()

    f = open(output_directory_name + cities_filename + '_'
             + str(ants_count) + '_'
             + str(iterations) + '_'
             + type_name + '_fitness.dat', 'w')
    f.write(best_result.fitness_to_string())
    f.close()

    f = open(output_directory_name + cities_filename + '_'
             + str(ants_count) + '_'
             + str(iterations) + '_'
             + type_name + '_path.dat', 'w')
    f.write(str(best_result.best_path.get_points_gnuplot()))
    f.close()

    f = open(output_directory_name + cities_filename + '_'
             + str(ants_count) + '_'
             + str(iterations) + '_'
             + type_name + '_avg.dat', 'w')
    f.write(ResultConverter(result_list).covert_to_avg_results())
    f.close()

    f = open(output_directory_name + cities_filename + '_'
             + str(ants_count) + '_'
             + str(iterations) + '_'
             + type_name + '_diversity.dat', 'w')
    f.write(ResultConverter(result_list).convert_diversity_results())
    f.close()

    f = open(output_directory_name + cities_filename + '_'
             + str(ants_count) + '_'
             + str(iterations) + '_'
             + type_name + '_attractiveness_avg_std.dat', 'w')
    f.write(ResultConverter(result_list).convert_attractiveness_avg_std_results())
    f.close()

    f = open(output_directory_name + cities_filename + '_'
             + str(ants_count) + '_'
             + str(iterations) + '_'
             + type_name + '_attractiveness_ratio.dat', 'w')
    f.write(ResultConverter(result_list).convert_attractiveness_ratio_results())
    f.close()

    f = open(output_directory_name + cities_filename + '_'
             + str(ants_count) + '_'
             + str(iterations) + '_'
             + type_name + '_population_sizes.dat', 'w')
    f.write(ResultConverter(result_list).convert_population_sizes_results())
    f.close()

    for i in range(options.p):
        processes[i].join()


if __name__ == "__main__":
    main()