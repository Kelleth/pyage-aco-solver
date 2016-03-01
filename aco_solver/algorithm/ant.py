import random

from aco_solver.algorithm.commons import Path


# Template class for different kinds of ants - implements basic ant behaviour in "find_path" method
class Ant(object):
    def __init__(self, graph, path):
        self.graph = graph
        self.path = path

    def find_path(self):
        self.current_constraints = [x for x in self.graph.constraints]
        chosen_items = [0 for x in range(self.graph.item_count)]

        start_item = self.__choose_start_item()

        chosen_items[start_item.id] = 1
        self.current_constraints = [self.current_constraints[x] - start_item.constraints[x] for x in range(self.graph.constraint_count)]

        forbidden_items = []

        while True:
            item = self.choose_next_item(self.graph.items, chosen_items, forbidden_items)
            if item == -1:
                break
            chosen_items[item] = 1
            self.current_constraints = [self.current_constraints[x] - self.graph.items[item].constraints[x] for x in range(self.graph.constraint_count)]
            if (chosen_items.count(1) + len(forbidden_items) == self.graph.item_count):
                break

        self.path = Path(chosen_items, self.graph)
        return self.path

    def choose_next_item(self, items, chosen_items, forbidden_items):
        pass

    # Override in subclasses to provide attractiveness value based on ant kind
    def calculate_item_attractiveness(self, item, current_constraints):
        return 0

    # Visitor pattern used to update pheromone value while visiting paths without using "instance of"
    # By default unknown pheromone (which isn't assigned to any ant species) is updated
    def visit(self, assignment, pheromone_value):
        assignment.pheromone.update_unknown_pheromone(pheromone_value)

    def __choose_start_item(self):
        return random.choice(self.graph.items)

    def __repr__(self):
        return 'Distance: %s Path: %s' % (self.path.distance, self.path)


# Converts attractiveness of all available paths to their probability
# and randomly chooses path based on computed probabilities - paths with higher attractiveness will be more likely
# Base class for other ants used in experiment
class ShuffleAnt(Ant):
    def __init__(self, graph, path):
        super(ShuffleAnt, self).__init__(graph, path)

    def choose_next_item(self, items, chosen_items, forbidden_items):
        items_attractiveness = []
        found_element = False
        for item in items:
            if chosen_items[item.id] == 1 or item.id in forbidden_items:
                items_attractiveness.append(0.0)
            elif self.violates_constraints(item):
                items_attractiveness.append(0.0)
                forbidden_items.append(item.id)
            else:
                found_element = True
                items_attractiveness.append(self.calculate_item_attractiveness(item, self.current_constraints))

        if not found_element:
            return -1
        item_probabilities = self.calculate_item_probability(items_attractiveness)
        value = random.random()

        for i in range(len(item_probabilities) - 1):
            if item_probabilities[i] <= value < item_probabilities[i + 1]:
                return i

    def violates_constraints(self, item):
        return min([self.current_constraints[x] - item.constraints[x] for x in range(self.graph.constraint_count)]) < 0

    @staticmethod
    def calculate_item_probability(item_attractiveness):
        attractiveness_sum = float(sum(item_attractiveness))

        connections_probability = []

        if attractiveness_sum > 0:
            for i in range(len(item_attractiveness)):
                connections_probability.append(item_attractiveness[i] / attractiveness_sum)
        else:
            for i in range(len(item_attractiveness)):
                connections_probability.append(1.0 / len(item_attractiveness))

        converted_form = [0.0]
        for probability in connections_probability:
            converted_form.append(converted_form[-1] + probability)
        converted_form[-1] = 1.0

        return converted_form


# ClassicAnt which computes attractiveness like pheromone^alpha * (1/distance)^beta
class ClassicAnt(ShuffleAnt):
    def __init__(self, graph, path, pheromone_influence, distance_influence):
        super(ClassicAnt, self).__init__(graph, path)
        self.pheromone_influence = pheromone_influence
        self.distance_influence = distance_influence

    def calculate_item_attractiveness(self, item, current_constraints):
        return item.pheromone.unknown_pheromone ** self.pheromone_influence * \
               (item.heuristic) ** self.distance_influence


#TODO: fix all other implementations
# Always chooses path with best attractiveness - used only for tests
class GreedyAnt(Ant):
    def __init__(self, graph, path, pheromone_influence, distance_influence):
        super(GreedyAnt, self).__init__(graph, path)
        self.pheromone_influence = pheromone_influence
        self.distance_influence = distance_influence

    def calculate_item_attractiveness(self, assignment, current_constraints):
        return assignment.pheromone ** self.pheromone_influence * \
               (1.0 / assignment.coupling_value) ** self.distance_influence


# The individuals who are "altercentric" would follow the mass
class AltercentricAnt(ShuffleAnt):
    def __init__(self, graph, path, pheromone_influence=2.0):
        super(AltercentricAnt, self).__init__(graph, path)
        self.pheromone_influence = pheromone_influence

    def visit(self, assignment, pheromone_value):
        assignment.pheromone.update_ac_pheromone(pheromone_value)

    def calculate_item_attractiveness(self, assignment, current_constraints):
        return assignment.pheromone.total_pheromone ** self.pheromone_influence


# The individuals who are "egocentric" would be more creative to try to find a new solution,
# finding their own way, less caring for others and for pheromone trail.
class EgocentricAnt(ShuffleAnt):
    def __init__(self, graph, path, distance_influence=3.0):
        super(EgocentricAnt, self).__init__(graph, path)
        self.distance_influence = distance_influence

    def visit(self, assignment, pheromone_value):
        assignment.pheromone.update_ec_pheromone(pheromone_value)

    def calculate_item_attractiveness(self, assignment, current_constraints):
        return (1.0 / assignment.coupling_value) ** self.distance_influence


# These good at conflict handling will wait and observe the others.
class GoodConflictAnt(ShuffleAnt):
    def __init__(self, graph, path):
        super(GoodConflictAnt, self).__init__(graph, path)

    def visit(self, assignment, pheromone_value):
        assignment.pheromone.update_gc_pheromone(pheromone_value)

    def calculate_item_attractiveness(self, assignment, current_constraints):
        return ((14.0 * assignment.pheromone.ec_pheromone + 2.0 * assignment.pheromone.ac_pheromone  #
                 + 2.5 * assignment.pheromone.gc_pheromone + 0.5 * assignment.pheromone.bc_pheromone) / 4.0) ** 2.0


# Those bad at conflict handling will behave impulsively (in effect randomly)
class BadConflictAnt(Ant):
    def __init__(self, graph, path):
        super(BadConflictAnt, self).__init__(graph, path)

    def visit(self, assignment, pheromone_value):
        assignment.pheromone.update_bc_pheromone(pheromone_value)

    def choose_next_location(self, possible_assignments, chosen_locations):
        next_location = None
        all_locations = xrange(len(self.graph.assignments))
        possible_locations = list(set(all_locations) - set(chosen_locations))

        return random.choice(possible_locations)