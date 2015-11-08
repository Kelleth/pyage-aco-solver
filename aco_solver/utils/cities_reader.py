import math


class CitiesReader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.cities_count = 0
        self.cities_positions = []

    def read_file(self):
        with open('inputs/examples/' + self.file_name + '.cities', "r") as f:
            lines = f.readlines()
            self.cities_count = len(lines)
            for line in lines:
                splitted = line.split()
                self.cities_positions.append((int(splitted[0]), int(splitted[1])))

    def create_distance_matrix(self):
        matrix = [[0 for _ in range(self.cities_count)] for _ in range(self.cities_count)]
        for idxFrom, cityFrom in enumerate(self.cities_positions):
            for idxTo, cityTo in enumerate(self.cities_positions):
                matrix[idxFrom][idxTo] = math.sqrt((cityFrom[0] - cityTo[0]) ** 2 + (cityFrom[1] - cityTo[1]) ** 2)
        return matrix

    def get_positions(self):
        return self.cities_positions
