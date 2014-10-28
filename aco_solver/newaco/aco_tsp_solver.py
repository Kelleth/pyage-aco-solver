from optparse import OptionParser
from aco_solver.core.cities_reader import CitiesReader
from aco_solver.newaco.aco_ant_colony import AntColony
from aco_solver.newaco.graph import Graph

if __name__ == "__main__":
    usage = "usage: %prog [options] citiesFileName"
    parser = OptionParser(usage=usage)
    parser.add_option("-a", "--ants", default="10", metavar="int", help="ant count [default: %default]", dest="ants")
    parser.add_option("-i", "--iter", default="10", metavar="int",
                      help="iterations count [default: %default]", dest="iter")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    cities_filename = args[0]
    iterations = int(options.iter)
    ants_count = int(options.ants)

    cities_reader = CitiesReader(cities_filename)
    cities_reader.read_file()
    cities_distances = cities_reader.create_distance_matrix()

    graph = Graph(cities_distances)
    colony = AntColony(graph, ants_count, iterations)
    colony.start_simulation()

