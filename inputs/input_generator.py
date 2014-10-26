import random


def main():
    number_of_cities = [10, 20, 50, 100, 500]
    net_range = [50, 200, 1000]

    for i in number_of_cities:
        for j in net_range:
            __generate_cities(i, j)


def __generate_cities(number_of_cities, net_range):
    f = open('generated/' + str(number_of_cities) + '.cities' + str(net_range) + '.range', 'w')
    points = set()

    for _ in range(number_of_cities):
        (x, y) = __generate_point(points, net_range)
        f.write(str(x) + ' ' + str(y) + '\n')

    f.close()


def __generate_point(points, net_range):
    while True:
        x = random.randrange(net_range)
        y = random.randrange(net_range)

        if not (x, y) in points:
            points.add((x, y))
            return x, y


if __name__ == '__main__':
    main()
