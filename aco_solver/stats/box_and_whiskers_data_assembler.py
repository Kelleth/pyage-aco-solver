from optparse import OptionParser

#list of populations' names to be merged
populations = ['a', 'eq']

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

    merged_global = open(directory + '/' + dataset_name + '_100_100_avg_box_and_whiskers_global_merged.dat', 'w')
    merged_global.write('number;name;avg;min;first_quartile;third_quartile;max\n')
    merged_last_iter = open(directory + '/' + dataset_name + '_100_100_avg_box_and_whiskers_last_iter_merged.dat', 'w')
    merged_last_iter.write('number;name;avg;min;first_quartile;third_quartile;max\n')

    for i in xrange(len(populations)):
        population = populations[i]
        prefix = cities_filename + '_' + str(ants_count) + '_' + str(iterations) + '_' + population

        f_global = open(directory + prefix + '_avg_box_and_whiskers_global.dat', 'r')
        f_global.next()
        for line in f_global:
            merged_global.write(str(i) + ';' + population + ';' + line)
        f_global.close()

        f_last_iter = open(directory + prefix + '_avg_box_and_whiskers_last_iter.dat', 'r')
        f_last_iter.next()
        for line in f_last_iter:
            merged_last_iter.write(str(i) + ';' + population + ';' + line)

        f_last_iter.close()

    merged_global.close()
    merged_last_iter.close()

if __name__ == "__main__":
    main()