import numpy as np

from .utils import get_optimal_configuration_and_fitness
from .plot import plot_chromosome


class Individual(object):
    """
    A class representation of an individual
    """
    def __init__(self, polygons, board_size, chromosome=None):
        """
        Initialization function. A random chromosome is generated if no chromosome is specified.
        :param polygons: initial polygon list
        :param board_size: size off the chessboard
        :param chromosome: order sequence of the pieces
        """
        self.n_pieces = len(polygons)
        self.chromosome = self.generate_chromosome() if chromosome is None else np.array(chromosome)
        self.polygons = polygons
        self.board_size = board_size
        self.fitness, self.placements = get_optimal_configuration_and_fitness(self.chromosome,
                                                                              polygons, board_size)

    def generate_chromosome(self):
        """
        Create a random chromosome sequence
        """
        return np.random.choice(range(self.n_pieces), self.n_pieces, replace=False).astype(int)

    def mutate(self, mutation_probability):
        """
        Mutate the chromosome by swapping the gene with a random gene if a condition is met
        :return: mutated chromosome
        """
        chromosome = self.chromosome.copy()
        for idx, c in enumerate(chromosome):
            if np.random.rand() < mutation_probability:
                rand_idx = np.random.choice(range(self.n_pieces))
                chromosome[idx], chromosome[rand_idx] = chromosome[rand_idx], chromosome[idx]
        self.chromosome = chromosome

    def mate(self, partner):
        """
        Create offspring with a order-crossover method
        :param partner: a second p1 which will participate in the mating
        :return: two new offspring individuals
        """
        c1, c2 = np.zeros((2, self.n_pieces))
        start, end = np.sort(np.random.choice(range(self.n_pieces), 2, replace=False))

        p1 = self.chromosome
        p2 = partner.chromosome

        c1[start:end + 1] = p1[start:end + 1]
        t = p2[range(end - self.n_pieces + 1, end + 1)]
        t = t[~np.in1d(t, p1[start:end + 1])]
        c1[range(end - self.n_pieces + 1, start)] = t
        c1 = c1.astype(int)

        c2[start:end + 1] = p2[start:end + 1]
        t = p1[range(end - self.n_pieces + 1, end + 1)]
        t = t[~np.in1d(t, p2[start:end + 1])]
        c2[range(end - self.n_pieces + 1, start)] = t
        c2 = c2.astype(int)

        return Individual(self.polygons, self.board_size, c1), Individual(self.polygons, self.board_size, c2)

    def plot(self, filename=''):
        if filename == '':
            plot_chromosome(self, self.polygons, self.board_size)
        else:
            plot_chromosome(self, self.polygons, self.board_size, filename)