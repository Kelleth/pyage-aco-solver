from optparse import OptionParser

times_dirs = ["parametrized_probability", "parametrized_one_swap_6percent", "parametrized_one_swap_4percent",
              "parametrized_one_swap_2percent", "parametrized_competition_1_6period",
              "parametrized_competition_1_4period", "parametrized_competition_1_2period",
              "parametrized_from_worst_to_better_6percent", "parametrized_from_worst_to_better_4percent",
              "parametrized_from_worst_to_better_2percent", "parametrized_different_swap_6percent",
              "parametrized_different_swap_4percent", "parametrized_different_swap_2percent"]

times_names = ["probability", "one-swap-6", "one-swap-4", "one-swap-2", "competition-6", "competition-4",
               "competition-2", "worst-best-6", "worst-best-4", "worst-best-2", "different-swap-6", "different-swap-4",
               "different-swap-2"]


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

    merged_times = open(directory + '/' + cities_filename + '_' + str(ants_count) + '_' + str(
        iterations) + '_merged_times.dat', 'w')

    i = 0
    for direct in times_dirs:
        time_file = open(directory + direct + '/' + cities_filename + '_' + str(ants_count) + '_' + str(
            iterations) + '_eq_times.dat', 'r')
        time_file.readline()
        times = time_file.readline().split(";")
        merged_times.write(times_names[i] + ";" + times[0] + ";" + times[1] + "\n")
        time_file.close()
        i += 1

    merged_times.close()


if __name__ == "__main__":
    main()
