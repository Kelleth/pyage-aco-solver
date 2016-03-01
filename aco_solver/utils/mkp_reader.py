import numpy


class MKPReader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.constraint_count = 0
        self.item_count = 0
        self.item_profits = []
        self.constraint_item_matrix = []
        self.constraints = []

    def read_file(self):
        with open('inputs/mkp/' + self.file_name + '.dat', "r") as f:
            self.item_count, self.constraint_count = map(int, f.readline().split())
            self.item_profits = [int(x) for x in f.readline().split()]
            for i in xrange(self.constraint_count):
                line = [int(x) for x in f.readline().split()]
                self.constraint_item_matrix.append(line)
            self.constraints = [int(x) for x in f.readline().split()]

        # print self.item_count
        # print self.constraint_count
        # print self.item_profits
        # print self.constraints
        # for i in xrange(self.constraint_count):
        #     print self.constraint_item_matrix[i]
