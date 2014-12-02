from multiprocessing import Process, Queue
from optparse import OptionParser

from aco_solver.algorithm import graph
from aco_solver.utils.cities_reader import CitiesReader
from aco_solver.algorithm.ant_colony import ControlSampleColony, GuiltConditionColony, AngerConditionColony, \
    ClassicAntColony
from aco_solver.algorithm.graph import Graph


def start_simulation(ants_count, iterations, distance_matrix, rho, q, type, alpha, beta, queue):
    colony = None

    if type == "cs":  # control sample
        graph = create_graph_with_default_pheromone_value(distance_matrix, rho, q)
        colony = ControlSampleColony(ants_count, graph, iterations)
    elif type == "gc":  # guilt condition
        graph = create_graph_with_default_pheromone_value(distance_matrix, rho, q)
        colony = GuiltConditionColony(ants_count, graph, iterations)
    elif type == "ac":  # anger condition
        graph = create_graph_with_default_pheromone_value(distance_matrix, rho, q)
        colony = AngerConditionColony(ants_count, graph, iterations)
    elif type == "ca":  # classical ants
        graph = Graph(distance_matrix, rho, q, 0.01)
        colony = ClassicAntColony(ants_count, graph, alpha, beta, iterations)

    queue.put(colony.start_simulation())


def create_graph_with_default_pheromone_value(cities_distances, rho, q):
    return Graph(cities_distances, rho, q, (1.0 / graph.compute_average_distance(cities_distances)) ** 2.0)


if __name__ == "__main__":
    usage = "usage: %prog [options] ants_count iterations citiesFileName"

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

    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("incorrect number of arguments")

    ants_count = int(args[0])
    iterations = int(args[1])
    cities_filename = args[2]

    cities_reader = CitiesReader(cities_filename)
    cities_reader.read_file()
    distance_matrix = cities_reader.create_distance_matrix()

    print "File:", cities_filename, "Type:", options.type, "Ants:", ants_count, "Iterations:", iterations

    processes = []
    queue = Queue()
    for i in range(options.p):
        processes.append(Process(target=start_simulation, args=(
            ants_count, iterations, distance_matrix, options.rho, options.q, options.type, options.alpha, options.beta,
            queue,)))
    for i in range(options.p):
        processes[i].start()
    for i in range(options.p):
        processes[i].join()

    best_result = None
    output_string = None

    while not queue.empty():
        (new_output, new_result) = queue.get()

        if best_result is None or new_result < best_result:
            best_result = new_result
            output_string = new_output

    print output_string
