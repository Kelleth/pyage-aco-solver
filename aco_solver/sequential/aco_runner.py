from multiprocessing import Process, Queue
from optparse import OptionParser
import random
import math

from aco_solver.core.cities_reader import CitiesReader
from aco_solver.sequential.ant_colony import AntColony
from aco_solver.sequential.ants import GCAnt, BCAnt, ACAnt, ECAnt, GreedyAnt, ClassicAnt
from aco_solver.sequential.commons import Path
from aco_solver.sequential.graph import Graph


def generate_greedy_ants(total_number_of_ants, city_graph, alpha, beta):
    generated_ants = []
    for _ in range(total_number_of_ants):
        generated_ants.append(GreedyAnt(city_graph, generate_random_path(city_graph.cities), alpha, beta))
    return generated_ants


def generate_classic_ants(total_number_of_ants, city_graph, alpha, beta):
    generated_ants = []
    for _ in range(total_number_of_ants):
        generated_ants.append(ClassicAnt(city_graph, generate_random_path(city_graph.cities), alpha, beta))
    return generated_ants


# 22% egocentric, 15% altercentric, 45% flexible, 18% bad conflict handlers
def generate_control_sample(total_number_of_ants, city_graph):
    return create_sample(total_number_of_ants, 0.22, 0.15, 0.45, 0.18, city_graph)


# 3% egocentric, 46% altercentric, 23% flexible, 28% bad conflict handlers
def generate_guilt_condition_sample(total_number_of_ants, city_graph):
    return create_sample(total_number_of_ants, 0.03, 0.46, 0.23, 0.28, city_graph)


# 6% egocentric, 6% altercentric, 63% flexible, 25% bad conflict handlers
def generate_anger_condition_sample(total_number_of_ants, city_graph):
    return create_sample(total_number_of_ants, 0.06, 0.06, 0.63, 0.25, city_graph)


def create_sample(total_number_of_ants, ec_fraction, ac_fraction, bc_fraction, gc_fraction, city_graph):
    generated_ants = []

    for _ in range(int(math.ceil(total_number_of_ants * ec_fraction))):
        generated_ants.append(ECAnt(city_graph, generate_random_path(city_graph.cities)))

    for _ in range(int(math.ceil(total_number_of_ants * ac_fraction))):
        generated_ants.append(ACAnt(city_graph, generate_random_path(city_graph.cities)))

    for _ in range(int(math.ceil(total_number_of_ants * bc_fraction))):
        generated_ants.append(BCAnt(city_graph, generate_random_path(city_graph.cities)))

    for _ in range(total_number_of_ants - len(generated_ants)):
        generated_ants.append(GCAnt(city_graph, generate_random_path(city_graph.cities)))

    random.shuffle(generated_ants)
    return generated_ants


def generate_random_path(available_cities):
    shuffled_cities = list(available_cities)
    random.shuffle(shuffled_cities)

    start_city = shuffled_cities.pop(0)

    connection_list = []
    present_city = start_city

    while shuffled_cities:
        next_city = shuffled_cities.pop(0)
        connection_list.append(present_city.find_connection_to_city(next_city))

        present_city = next_city

    return Path(start_city, connection_list)


def start_simulation(ants_count, iterations, cities_distances, rho, q, type, alpha, beta, queue):
    graph = Graph(cities_distances, rho, q)

    ants = []
    if type == "cs":  # control sample
        ants = generate_control_sample(ants_count, graph)
    elif type == "gc":  # guilt condition
        ants = generate_guilt_condition_sample(ants_count, graph)
    elif type == "ac":  # anger condition
        ants = generate_anger_condition_sample(ants_count, graph)
    elif type == "ca":  # classical ants
        ants = generate_classic_ants(ants_count, graph, alpha, beta)
    elif type == "ga":  # greedy ants
        ants = generate_greedy_ants(ants_count, graph, alpha, beta)

    colony = AntColony(graph, ants, iterations)
    queue.put(colony.start_simulation())


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
    cities_distances = cities_reader.create_distance_matrix()

    print "File:", cities_filename, "Type:", options.type, "Ants:", ants_count, "Iterations:", iterations
    processes = []
    queue = Queue()
    for i in range(options.p):
        processes.append(Process(target=start_simulation, args=(
            ants_count, iterations, cities_distances, options.rho, options.q, options.type, options.alpha, options.beta,
            queue,)))
    for i in range(options.p):
        processes[i].start()
    for i in range(options.p):
        processes[i].join()
    for i in range(options.p):
        print(queue.get())
