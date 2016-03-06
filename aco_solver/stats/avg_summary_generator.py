from optparse import OptionParser
import os
import re

import numpy

from aco_solver.algorithm import ant_colony
from aco_solver.utils.results_reader import read_file


separator = ';'
ant_populations = ['cs', 'ca', 'ha', 'la']

# backup of stats and fitness values from first column in avg result
# used to calculate common quartiles, average, min and max values
stats_values = []
fitness_values = []

def generate_header_items():
    header = []

    for population_abbrev in ant_populations:
        full_name = ant_colony.get_population_fullname(population_abbrev)
        header.append(full_name)
        header.append(full_name + " stdev")
        header.append(full_name + " min")
        header.append(full_name + " first_quartile")
        header.append(full_name + " third_quartile")
        header.append(full_name + " median")
        header.append(full_name + " max")
    return header


def list_files_with_data(prefix, name, output_directory):
    pattern = prefix + name + '_(\d+).dat'

    files = [f for f in os.listdir(output_directory) \
             if os.path.isfile(os.path.join(output_directory, f)) and re.match(pattern, f)]

    return files


def find_best_result(result_map, iteration):
    best_distance = None

    for _, fitness_list in result_map.iteritems():
        if len(fitness_list) <= iteration:
            continue
        if best_distance is None or fitness_list[iteration] > best_distance:
            best_distance = fitness_list[iteration]

    return best_distance


def generate_population_box_and_whiskers_values(fitnesses, f_box_and_whiskers_global):
    f_box_and_whiskers_global.write('avg;min;first_quartile;third_quartile;median;max\n')

    if fitnesses is None or not fitnesses:
        empty = ''
        f_box_and_whiskers_global.write(empty + separator + empty + separator + empty +
                                        separator + empty + separator + empty + '\n')
    else:
        avg_fitness = str(numpy.average(fitnesses))
        min_fitness = str(numpy.amin(fitnesses))
        first_quartile_fitness = str(numpy.percentile(fitnesses, 25))
        third_quartile_fitness = str(numpy.percentile(fitnesses, 75))
        max_fitness = str(numpy.amax(fitnesses))
        median_fitness = str(numpy.median(fitnesses))

        f_box_and_whiskers_global.write(avg_fitness + separator + min_fitness + separator + first_quartile_fitness +
                                        separator + third_quartile_fitness + separator + median_fitness + separator + max_fitness + '\n')


def generate_population_box_and_whiskers_last_iter_values(avg_fitness_last, min_fitness_last,
                                                          first_quartile_fitness_last, third_quartile_fitness_last,
                                                          max_fitness_last, median_fitness_last, f_box_and_whiskers_last_iter):

    f_box_and_whiskers_last_iter.write('avg;min;first_quartile;third_quartile;median;max\n')
    avg_fitness = str(avg_fitness_last)
    min_fitness = str(min_fitness_last)
    first_quartile_fitness = str(first_quartile_fitness_last)
    third_quartile_fitness = str(third_quartile_fitness_last)
    max_fitness = str(max_fitness_last)
    median_fitness = str(median_fitness_last)

    f_box_and_whiskers_last_iter.write(avg_fitness + separator + min_fitness + separator + first_quartile_fitness +
                                       separator + third_quartile_fitness + separator + median_fitness + separator + max_fitness + '\n')


def compute_average_fitness_for_population(results, iterations, f_box_and_whiskers_global, f_box_and_whiskers_last_iter):
    avg_fitness = []
    stdev_fitness = []
    min_fitness = []
    first_quartile_fitness = []
    third_quartile_fitness = []
    max_fitness = []
    median_fitness = []

    for iteration in range(iterations):
        fitness = [find_best_result(result.fitness.map, iteration) for result in results]

        if fitness:
            avg_fitness.append(numpy.average(fitness))
            stdev_fitness.append(numpy.std(fitness))
            min_fitness.append(numpy.amin(fitness))
            first_quartile_fitness.append(numpy.percentile(fitness, 25))
            third_quartile_fitness.append(numpy.percentile(fitness, 75))
            max_fitness.append(numpy.amax(fitness))
            median_fitness.append(numpy.median(fitness))

    generate_population_box_and_whiskers_values(avg_fitness, f_box_and_whiskers_global)

    if len(avg_fitness) == 0 or len(min_fitness) == 0 or len(first_quartile_fitness) == 0 or len(third_quartile_fitness) == 0 or len(max_fitness) == 0:
        empty = ''
        generate_population_box_and_whiskers_last_iter_values(empty, empty, empty, empty, empty, empty, f_box_and_whiskers_last_iter)
    else:
        avg_fitness_last = avg_fitness[-1]
        min_fitness_last = min_fitness[-1]
        first_quartile_fitness_last = first_quartile_fitness[-1]
        third_quartile_fitness_last = third_quartile_fitness[-1]
        max_fitness_last = max_fitness[-1]
        median_fitness_last = median_fitness[-1]

        generate_population_box_and_whiskers_last_iter_values(avg_fitness_last, min_fitness_last,
                                                              first_quartile_fitness_last, third_quartile_fitness_last, median_fitness_last,
                                                              max_fitness_last, f_box_and_whiskers_last_iter)

    return avg_fitness, stdev_fitness, min_fitness, first_quartile_fitness, third_quartile_fitness, median_fitness, max_fitness

# TODO: refactor this code
def generate_fitness_output(population_results, iterations, f, f_box_and_whiskers_global, f_box_and_whiskers_last_iter):
    fitness_header = 'Iteration' + separator + separator.join(generate_header_items()) + '\n'

    f.write(fitness_header)

    populations_fitness = []
    for _, value in population_results.iteritems():
        avg_fitness, stdev_fitness, min_fitness, first_quartile_fitness, third_quartile_fitness, median_fitness, max_fitness\
            = compute_average_fitness_for_population(value, iterations, f_box_and_whiskers_global, f_box_and_whiskers_last_iter)
        populations_fitness.append((avg_fitness, stdev_fitness, min_fitness, first_quartile_fitness,
                                    third_quartile_fitness, median_fitness, max_fitness))

    for iteration in range(iterations):
        f.write(str(iteration + 1))
        for avg_fitness, stdev_fitness, min_fitness, first_quartile_fitness, third_quartile_fitness, median_fitness, max_fitness\
                in populations_fitness:
            str_avg_fitness = ''
            str_stdev_fitness = ''
            str_min_fitness = ''
            str_first_quartile_fitness = ''
            str_third_quartile_fitness = ''
            str_median_fitness = ''
            str_max_fitness = ''

            if len(avg_fitness) > iteration and len(stdev_fitness) > iteration and len(min_fitness) > iteration \
                    and len(first_quartile_fitness) > iteration and len(third_quartile_fitness) > iteration \
                    and len(median_fitness) > iteration and len(max_fitness) > iteration:
                str_avg_fitness = str(avg_fitness[iteration])
                str_stdev_fitness = str(stdev_fitness[iteration])
                str_min_fitness = str(min_fitness[iteration])
                str_first_quartile_fitness = str(first_quartile_fitness[iteration])
                str_third_quartile_fitness = str(third_quartile_fitness[iteration])
                str_median_fitness = str(median_fitness[iteration])
                str_max_fitness = str(max_fitness[iteration])

            f.write(separator + str_avg_fitness + separator + str_stdev_fitness + separator + str_min_fitness +
                    separator + str_first_quartile_fitness + separator + str_third_quartile_fitness +
                    separator + str_median_fitness + separator + str_max_fitness)
        f.write('\n')


def compute_average_distance_for_population(results):
    distance_list = [result.best_distance for result in results]
    return compute_average_values(distance_list)


def compute_average_time_for_population(results):
    time_list = [result.computation_time for result in results]
    return compute_average_values(time_list)


def generate_stats_output(population_results, f):
    stats_header = 'Stat' + separator + separator.join(generate_header_items()) + '\n'
    f.write(stats_header)

    f.write('Best distance')
    for _, value in population_results.iteritems():
        avg_distance, stdev_distance, min_distance, first_quartile_distance, third_quartile_distance, median_distance, max_distance\
            = compute_average_distance_for_population(value)
        f.write(average_values_to_output_format(avg_distance, stdev_distance, min_distance, first_quartile_distance,
                                                third_quartile_distance, median_distance, max_distance))
    f.write('\n')

    f.write('Computation time')
    for _, value in population_results.iteritems():
        avg_time, stdev_time, min_time, first_quartile_time, third_quartile_time, median_time, max_time\
            = compute_average_time_for_population(value)
        f.write(average_values_to_output_format(avg_time, stdev_time, min_time, first_quartile_time,
                                                third_quartile_time, median_time, max_time))
    f.write('\n')


# TODO: check whether quartiles are computed correctly
def compute_average_values(values_list):
    if values_list:
        return numpy.average(values_list), numpy.std(values_list), numpy.amin(values_list), \
            numpy.percentile(values_list, 25), numpy.percentile(values_list, 75), numpy.median(values_list), numpy.amax(values_list)
    else:
        return None, None, None, None, None, None, None

# TODO: reformat this code
def average_values_to_output_format(avg, stdev, min, first_quartile, third_quartile, median, max):
    if avg is None or stdev is None or min is None or first_quartile is None or third_quartile is None or median is None or max is None:
        return separator + separator + separator + separator + separator + separator
    else:
        return separator + str(avg) + separator + str(stdev) + separator + str(min) + separator + \
            str(first_quartile) + separator + str(third_quartile) + separator + str(median) + separator + str(max)


def main():
    usage = "Usage: %prog number_of_ants iterations dataset_name output_directory"

    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()
    if len(args) < 4 or len(args) > 5:
        parser.error("Incorrect number of arguments")

    ants_count = int(args[0])
    iterations = int(args[1])
    cities_filename = args[2]
    directory = args[3]
    if len(args) == 5:
        name = args[4]
    else:
        name = None

    prefix = cities_filename + '_' + str(ants_count) + '_' + str(iterations) + '_'
    populations_results = dict()
    for ant_type in ant_populations:
        type_results = []

        if ant_type != 'pc' or name is None:
            name = ant_type

        for filename in list_files_with_data(prefix, name, directory):
            type_results.append(read_file(directory, filename, name))

        populations_results[ant_type] = type_results

    f = open(directory + '/' + prefix + name + '_avg_summary.dat', 'w')
    generate_stats_output(populations_results, f)
    f.write('\n')
    f_box_and_whiskers_global = open(directory + '/' + prefix + name + '_avg_box_and_whiskers_global.dat', 'w')
    f_box_and_whiskers_last_iter = open(directory + '/' + prefix + name + '_avg_box_and_whiskers_last_iter.dat', 'w')

    generate_fitness_output(populations_results, iterations, f, f_box_and_whiskers_global, f_box_and_whiskers_last_iter)

    f.close()
    f_box_and_whiskers_global.close()
    f_box_and_whiskers_last_iter.close()


if __name__ == "__main__":
    main()