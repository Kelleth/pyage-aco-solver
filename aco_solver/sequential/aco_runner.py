from optparse import OptionParser

from aco_solver.core.cities_reader import CitiesReader
from aco_solver.sequential.ant_colony import AntColony
from aco_solver.sequential.graph import Graph


if __name__ == "__main__":
    usage = "usage: %prog [options] ants_count iterations citiesFileName"

    parser = OptionParser(usage=usage)
    parser.add_option("-a", "--alpha", default="3.0", type="float", help="pheromone influence [default: %default]",
                      dest="alpha")
    parser.add_option("-b", "--beta", default="2.0", type="float", help="distance influence [default: %default]",
                      dest="beta")
    parser.add_option("-r", "--rho", default="0.01", type="float",
                      help="pheromone evaporation coefficient [default: %default]",
                      dest="rho")
    parser.add_option("-q", "--q", default="2.0", type="float", help="pheromone deposit factor [default: %default]",
                      dest="q")

    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("incorrect number of arguments")

    ants_count = int(args[0])
    iterations = int(args[1])
    cities_filename = args[2]

    cities_reader = CitiesReader(cities_filename)
    cities_reader.read_file()
    cities_distances = cities_reader.create_distance_matrix()

    graph = Graph(cities_distances, options.rho, options.q)
    colony = AntColony(graph, ants_count, iterations, options.alpha, options.beta)
    # colony.start_simulation()
    print ''