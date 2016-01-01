import numpy


class QAPReader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.size = 0
        self.flow_matrix = []
        self.distance_matrix = []
        self.potencial_d = []
        self.potencial_f = []

    def read_file(self):
        with open('inputs/qap/' + self.file_name + '.dat', "r") as f:
            self.size = int(f.readline())
            f.readline()
            for i in xrange(self.size):
                line = [int(x) for x in f.readline().split()]
                self.distance_matrix.append(line)
            f.readline()
            for i in xrange(self.size):
                line = [int(x) for x in f.readline().split()]
                self.flow_matrix.append(line)

        for i in xrange(self.size):
            pot_d = 0
            pot_f = 0
            for j in xrange(self.size):
                pot_d += self.distance_matrix[i][j]
                pot_f += self.flow_matrix[i][j]
            self.potencial_d.append(pot_d)
            self.potencial_f.append(pot_f)
        self.coupling_matrix = numpy.outer(numpy.array(self.potencial_d), numpy.array(self.potencial_f)).tolist()

    def get_distance_matrix(self):
        return self.distance_matrix

    def get_flow_matrix(self):
        return self.flow_matrix

    def get_coupling_matrix(self):
        return self.coupling_matrix

    def get_flow_potentials(self):
        return self.potencial_f
