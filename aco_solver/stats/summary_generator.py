from os import listdir
from os.path import isfile, join
import re

from aco_solver.algorithm.ant_colony import get_population_fullname


def get_details(output_directory, filename):
    f = open(output_directory + filename, 'r')

    details = []
    for _ in range(4):
        read_line = f.readline()
        details.append(read_line.split(":")[1].strip())
    f.close()

    return details


def write_summary(output_directory, filename_pattern, filename_list, prefix, separator):
    output_filename = output_directory + prefix + '_summary.dat'
    f = open(output_filename, 'w')
    f.write('Name;Distance;Iteration;Time\n')

    for filename in filename_list:
        suffix = re.match(filename_pattern, filename).group(2)
        population_name = get_population_fullname(suffix)

        details = get_details(output_directory, filename)

        f.write(population_name + separator + details[0] + separator + details[2] + separator + details[3] + '\n')

    f.close()
    print 'Summary saved to file: ' + output_filename


def find_matching_files(files, prefix):
    return [f for f in files if f.startswith(prefix)]


def main():
    separator = ';'
    output_directory = 'outputs/'
    filename_pattern = r"(\w+_\d+_\d+)_(\w{2}).dat"

    files = [f for f in listdir(output_directory) \
             if isfile(join(output_directory, f)) and re.match(filename_pattern, f)]

    while files:
        basic_filename = files[0]
        m = re.match(filename_pattern, basic_filename)

        prefix = m.group(1)
        matching_files = find_matching_files(files, prefix)
        write_summary(output_directory, filename_pattern, matching_files, prefix, separator)

        files = [filename for filename in files if filename not in matching_files]


if __name__ == "__main__":
    main()