import aco_solver.algorithm.results as results

separator = ';'


def read_file(directory, filename):
    name = directory + "/" + filename
    print(name)
    f = open(directory + '/' + filename, 'r')
    details = []
    lines = f.readlines()

    fitness = results.Fitness()
    for read_line in lines[:4]:
        details.append(read_line.split(":")[1].strip())
    headers = lines[4].strip().split(separator)
    for read_line in lines[5:]:
        distances = read_line.strip().split(separator)
        for i in range(1, 6):
            distance = distances[i]
            if distance:
                fitness.update_fitness_stats(headers[i], float(distance))
        fitness.increase_iteration()
    # fixme arguments passed to constructor have wrong types
    result = results.Result(fitness, float(details[3]), details[1], details[2], 100)
    result.best_distance = float(details[0])  # workaround to store best distance value
    f.close()
    return result
