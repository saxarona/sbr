"""
ACO
1170065 Xavier Sánchez
1299000 Erim Sezer

The basic algorithm goes something like this:

1. Initialize:
    a) Set time counter to 0
    b) Set cycles counter (NC) to 0
    c) For every edge (i,j) set an initial value of trail
    d) Place m ants on the n nodes
2. Set tabu list for all ants (or allowed moves, we'll see)
3. Repeat until tabu list is full (or allowed is empty):
    a) For all ants:
        a1) Choose the town j to move to, with calculated
        probability.
        a2) Move the ant to town j.
        a3) Update tabu list accordingly
4. For all ants:
    a) Evaluate performance.
    b) Update shortest tour found.
    c) For every edge (i,j):
        c1) For all ants:
            c1.1) Update pheromone trail
5. For every edge (i,j) compute pheromone trails
6. If cycles counter < max cycles counter and there's no stagnation:
    a) then
        a1) Empty all tabu lists (or re-fill)
        a2) Go back to step 2
    b) else
        b1) Print shortest tour
        b2) Stop

"""

from math import e, sin
from names import *


def setup_cities(ran, variables):
    """This function initializes cities as a
    len(variables)-row matrix, with range ran.
    """

    cities = []

    for j in range(len(variables)):
        aux_list = []
        for i in range(ran):
            aux_list.append(variables[j] + '_' + str(i))
        cities.append(aux_list)

    return cities


def setup_phero_map(ran, variables):
    """This function initializes the pheromone map,
    which is a matrix of len(variables) rows, and
    ran columns.
    """

    pheromone_map = []

    for j in range(len(variables)):
        aux_list = []
        for i in range(ran):
            aux_list.append(0)
        pheromone_map.append(aux_list)

    return pheromone_map


def heur(x, a0, a1, a2, a3):
    """This is the objective function"""

    f = a0 / x ** 2 + a1 * e ** (a2 / x) + a3 * sin(x)

    return f


class Ant(object):
    """This is the Ant class.
    This object contains:
    - current tour
    - best tour
    - a name
    Why using objects? Because I want a name for each!
    """
    def __init__(self, name):
        self.name = name
        self.tour = []
        self.best_tour = []

    def __str__(self):
        return "I'm {0} and my best tour is {1}".format(self.name, str(self.best_tour))
def main():
    """Everything goes here"""

    variables = ['a0', 'a1', 'a2', 'a3']
    ran = 16  # domain of variables, [0-ran]
    t = 0  # time counter
    NC = 0  # cycle counter
    m = 10 # number of ants

    testAnt = Ant(get_first_name(gender='female'))
    print(testAnt)

    cities = setup_cities(ran, variables)
    pheromone_map = setup_phero_map(ran, variables)

if __name__ == '__main__':
    main()
