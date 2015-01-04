from optparse import OptionParser

from aco_solver.utils.results_reader import read_file


def main():
    usage = "usage: %prog ants_count iterations citiesFileName resultsDir"

    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()
    if len(args) != 4:
        parser.error("incorrect number of arguments")

    ants_count = int(args[0])
    iterations = int(args[1])
    cities_filename = args[2]
    directory = args[3]

    prefix = cities_filename + '_' + str(ants_count) + '_' + str(iterations) + '_'
    populations_results = []
    for ant_type in ['cs', 'ac', 'gc', 'ca']:
        type_results = []
        for test_number in range(12):
            type_results.append(read_file(directory, prefix + ant_type + '_' + str(test_number) + '.dat'))

        populations_results.append(type_results)


if __name__ == "__main__":
    main()