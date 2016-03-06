class Graph(object):
    def __init__(self, instance, pheromone_evaporation, pheromone_deposit, init_pheromone_value,
                 attractiveness_alpha, attractiveness_beta):
        #TODO: remove unused objects/lists
        self.constraints = instance.constraints
        self.constraint_count = len(instance.constraints)

        items = []
        for i in range(instance.item_count):
            item_constraints = [x[i] for x in instance.constraint_item_matrix]

            heuristic = instance.item_profits[i] / sum([float(item_constraints[x]) / float(self.constraints[x]) for x in range(self.constraint_count) ])

            items.append(Item(item_constraints, init_pheromone_value, instance.item_profits[i], i, heuristic))

        self.items = items
        self.item_count = instance.item_count

        self.pheromone_evaporation = pheromone_evaporation
        self.pheromone_deposit = pheromone_deposit

        self.attractiveness_alpha = attractiveness_alpha
        self.attractiveness_beta = attractiveness_beta

        self.init_pheromone_value = init_pheromone_value

    def update_pheromones(self, ant):
        # increase value for visited connections
        path = ant.path
        if self.last_best_path is None:
            pheromone_fitness_denominator = 1.0 # + path.fitness
        else:
            pheromone_fitness_denominator = 1.0 + ((self.last_best_path.fitness - path.fitness) / self.last_best_path.fitness)
        for item_id, item_taken in enumerate(path.item_list):
            if item_taken == 1 and pheromone_fitness_denominator != 0:
                self.items[item_id].accept_visitor(ant, self.pheromone_deposit / pheromone_fitness_denominator)

    def evaporate_pheromones(self):
        # pheromone evaporation
        for item in self.items:
            item.pheromone.evaporate(1.0 - self.pheromone_evaporation)

    def calculate_diversity_and_attractiveness(self, best_path):
        connections_with_pheromone = 0
        connections_number = 0
        attractiveness_list = []
        attractiveness_on_best_path = 0
        attractiveness_outside_best_path = 0
        for item in self.items:
            connections_number += 1
            attractiveness = item.pheromone.unknown_pheromone ** self.attractiveness_alpha * (1.0 / item.heuristic) ** self.attractiveness_beta
            attractiveness_list.append(attractiveness)

            if best_path.contains_item(item):
                attractiveness_on_best_path += attractiveness
            else:
                attractiveness_outside_best_path += attractiveness

            if item.pheromone.was_recently_updated(self.init_pheromone_value):
                connections_with_pheromone += 1

        diversity = (connections_with_pheromone / float(connections_number)) * 100
        if attractiveness_outside_best_path == 0:
            attractiveness_ratio = 100
        else:
            attractiveness_ratio = (attractiveness_on_best_path / float(attractiveness_outside_best_path)) * 100
        return diversity, attractiveness_list, attractiveness_ratio


class Assignment(object):
    def __init__(self, location_id, factory_id, coupling_value, init_pheromone_value, connection_list=None):
        if not connection_list:
            connection_list = []

        self.location_id = location_id
        self.factory_id = factory_id
        self.coupling_value = coupling_value
        self.connection_no = 0
        self.connection_list = connection_list
        self.init_pheromone_value = init_pheromone_value
        self.pheromone = Pheromone(init_pheromone_value)

    def accept_visitor(self, visitor, pheromone_value):
        visitor.visit(self, pheromone_value)

    def __eq__(self, other):
        if isinstance(other, Assignment):
            return self.location_id == other.location_id and self.factory_id == other.factory_id
        else:
            return False

class Item(object):
    def __init__(self, constraints, init_pheromone_value, profit, id, heuristic):
        self.constraints = constraints
        self.pheromone = Pheromone(init_pheromone_value)
        self.profit = profit
        self.id = id
        self.heuristic = heuristic

    def accept_visitor(self, visitor, pheromone_value):
        visitor.visit(self, pheromone_value)

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.constraints == other.constraints and self.profit == other.profit
        else:
            return False

#TODO: necessary?
class Connection(object):
    def __init__(self, distance, source_location, destination_location):
        self.distance = distance
        self.source_location = source_location
        self.destination_location = destination_location


class Pheromone(object):
    def __init__(self, init_value):
        self.ac_pheromone = init_value
        self.ec_pheromone = init_value
        self.gc_pheromone = init_value
        self.bc_pheromone = init_value
        self.unknown_pheromone = init_value

        self.total_pheromone = self.ac_pheromone + self.ec_pheromone + self.gc_pheromone + self.bc_pheromone \
                               + self.unknown_pheromone

    def update_ac_pheromone(self, value):
        self.ac_pheromone += value
        self.__update_total_pheromone()

    def update_ec_pheromone(self, value):
        self.ec_pheromone += value
        self.__update_total_pheromone()

    def update_gc_pheromone(self, value):
        self.gc_pheromone += value
        self.__update_total_pheromone()

    def update_bc_pheromone(self, value):
        self.bc_pheromone += value
        self.__update_total_pheromone()

    def update_unknown_pheromone(self, value):
        self.unknown_pheromone += value
        self.__update_total_pheromone()

    def evaporate(self, factor):
        self.ac_pheromone *= factor
        self.ec_pheromone *= factor
        self.gc_pheromone *= factor
        self.bc_pheromone *= factor
        self.unknown_pheromone *= factor
        self.__update_total_pheromone()

    def was_recently_updated(self, init_pheromone_value):
        return self.ac_pheromone > init_pheromone_value or self.ec_pheromone > init_pheromone_value \
               or self.gc_pheromone > init_pheromone_value or self.bc_pheromone > init_pheromone_value \
               or self.unknown_pheromone > init_pheromone_value
        #return self.unknown_pheromone > init_pheromone_value

    def __update_total_pheromone(self):
        self.total_pheromone = self.ac_pheromone + self.ec_pheromone + self.gc_pheromone + self.bc_pheromone \
                               + self.unknown_pheromone

    def __str__(self):
        output_str = 'AC: '
        output_str += str(self.ac_pheromone) + '\n'
        output_str += 'EC: '
        output_str += str(self.ec_pheromone) + '\n'
        output_str += 'GC: '
        output_str += str(self.gc_pheromone) + '\n'
        output_str += 'BC: '
        output_str += str(self.bc_pheromone) + '\n'
        output_str += 'Total: '
        output_str += str(self.total_pheromone) + '\n'
        output_str += 'Unknown: '
        output_str += str(self.unknown_pheromone) + '\n'
        return output_str


# Average distance in graph is used to setup initial pheromone value
def compute_average_distance(distance_matrix):
    total_distance = 0.0
    number_of_connections = 0

    connection_queue = []
    visited_cities = [0]

    connection_queue.extend(get_connection_list(0, distance_matrix))

    while connection_queue:
        (source_id, destination_id) = connection_queue.pop(0)

        total_distance += distance_matrix[source_id][destination_id]
        number_of_connections += 1

        if destination_id in visited_cities:
            continue
        else:
            connection_queue.extend(get_connection_list(destination_id, distance_matrix))
            visited_cities.append(destination_id)

    return total_distance / number_of_connections


def get_connection_list(city_id, distance_matrix):
    connection_list = []

    for destination_id in range(len(distance_matrix[city_id])):
        if distance_matrix[city_id][destination_id] is not None:
            connection_list.append((city_id, destination_id))

    return connection_list
