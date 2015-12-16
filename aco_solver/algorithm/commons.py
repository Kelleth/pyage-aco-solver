# Represents ant path
class Path(object):
    def __init__(self, assignment_list, graph):
        self.assignment_list = assignment_list
        self.fitness = self.calculate_assignment_fitness(graph.flow_matrix, graph.locations_connections, assignment_list)

    def calculate_assignment_fitness(self, flow_matrix, connection_list, assignment_list):
        total_fitness = 0.0
        for connection in connection_list:
            total_fitness += connection.distance * flow_matrix[assignment_list[connection.source_location]][assignment_list[connection.destination_location]]
        return total_fitness

    def get_cities_list(self):
        cities = [self.start_city]
        cities.extend(connection.destination_city for connection in self.connection_list)
        cities.append(self.start_city)
        return cities

    def get_assignments(self):
        return self.assignment_list

    # Comparing by distance
    def __cmp__(self, other):
        if self.fitness < other.fitness:
            return -1
        elif self.fitness > other.fitness:
            return 1
        else:
            return 0

    #TODO: probably wont be used for QAP
    def get_points(self):
        points = []
        for city in self.get_cities_list():
            points.append(city.get_position())
        return points

    def get_points_gnuplot(self):
        points = []
        for city in self.get_cities_list():
            points.append(city.get_position_string())

        return '\n'.join(points)

    def contains_connection(self, connection):
        return connection in self.connection_list

    def __str__(self):
        return 'Fitness {}, assignments {}'.format(self.fitness, self.assignment_list)
