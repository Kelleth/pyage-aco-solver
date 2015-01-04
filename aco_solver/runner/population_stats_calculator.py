from optparse import OptionParser
import os
import re

import numpy

from aco_solver.utils.results_reader import read_file


separator = ';'
ant_populations = ['cs', 'ac', 'gc', 'ca']


def list_files_with_data(prefix, population_abbreviation, output_directory):
    pattern = prefix + population_abbreviation + '_(\d+).dat'

    files = [f for f in os.listdir(output_directory) \
             if os.path.isfile(os.path.join(output_directory, f)) and re.match(pattern, f)]

    return files


def find_best_result(result_map, iteration):
    best_distance = None

    for _, fitness_list in result_map.iteritems():
        if len(fitness_list) <= iteration:
            continue
        if best_distance is None or fitness_list[iteration] < best_distance:
            best_distance = fitness_list[iteration]

    return best_distance


def compute_average_fitness_for_population(results, iterations):
    avg_fitness = []
    stdev_fitness = []

    for iteration in range(iterations):
        fitness = [find_best_result(result.fitness.map, iteration) for result in results]

        if fitness:
            avg_fitness.append(numpy.average(fitness))
            stdev_fitness.append(numpy.std(fitness))

    return avg_fitness, stdev_fitness


def generate_fitness_output(population_results, iterations, f):
    temporary_array = []
    for population_name in ant_populations:
        temporary_array.append(population_name + '_avg')
        temporary_array.append(population_name + '_stdev')
    fitness_header = 'iteration' + separator + separator.join(temporary_array) + '\n'

    f.write(fitness_header)

    populations_fitness = []
    for _, value in population_results.iteritems():
        avg_fitness, stdev_fitness = compute_average_fitness_for_population(value, iterations)
        populations_fitness.append((avg_fitness, stdev_fitness,))

    for iteration in range(iterations):
        f.write(str(iteration + 1))
        for avg_fitness, stdev_fitness in populations_fitness:
            str_avg_fitness = ''
            str_stdev_fitness = ''

            if len(avg_fitness) > iteration and len(stdev_fitness) > iteration:
                str_avg_fitness = str(avg_fitness[iteration])
                str_stdev_fitness = str(stdev_fitness[iteration])

            f.write(separator + str_avg_fitness + separator + str_stdev_fitness)
        f.write('\n')


def main():
    usage = "usage: %prog citiesFileName antsCount iterations resultsDir"

    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()
    if len(args) != 4:
        parser.error("incorrect number of arguments")

    cities_filename = args[0]
    ants_count = int(args[1])
    iterations = int(args[2])
    directory = args[3]

    prefix = cities_filename + '_' + str(ants_count) + '_' + str(iterations) + '_'
    populations_results = dict()
    for ant_type in ant_populations:
        type_results = []
        for filename in list_files_with_data(prefix, ant_type, directory):
            type_results.append(read_file(directory, filename))

        populations_results[ant_type] = type_results

    f = open(directory + '/' + prefix + 'fitness_avg.dat', 'w')
    generate_fitness_output(populations_results, iterations, f)
    f.close()


if __name__ == "__main__":
    main()