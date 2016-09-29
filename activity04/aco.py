"""
ACO
1170065 Xavier Sánchez
1299000 Erim Sezer

The basic algorithm (taken from Dorigo 1996) is something like this:

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
   For every edge (i,j):
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
from random import *


class Ant(object):
    """This is the Ant class.
    Each ant has:
    - a human-readable name
    - a current position
    - a list of the current tour
    - the evaluation of the current tour
    - a list of the best tour
    - the evaluation of the best tour
    - a tabu list
    """
    def __init__(self, name):
        self.name = name
        self.pos = None
        self.tabu = []
        self.tour = []
        self.eval = 0
        self.best_tour = []
        self.best_eval = 0

    def __str__(self):
        return("I'm {0}! My best tour is {1},"
               "my best cost is {2}, and my tour so far is {3}".format(
                self.name, str(self.best_tour),
                self.best_eval, self.tour))

    def choose_town(self):
        """Returns which town j should the ant go next,
        considering it is in town i (pos)
        """

        # do a complex calculation

        trails = []

        actual_phero_map = []
        actual_cities = []

        for row in cities:
            for city in row:
                if city not in self.tabu:
                    indie_j = cities.index(row)
                    indie_i = row.index(city)
                    actual_cities.append(city)
                    actual_phero_map.append(pheromone_map[indie_j][indie_i])

        # print("Actual available cities:", actual_cities)

        sum_of_trails = sum(actual_phero_map)
        # print("The sum of pheromone trails is", sum_of_trails)

        prob_list = []

        for city in actual_cities:
            prob = actual_phero_map[actual_cities.index(city)] ** alpha \
                 * 1 ** beta / sum_of_trails
            prob_list.append(prob)

        # print("List of Probabilities:", prob_list)

        chosen_prob = max(prob_list)
        # print("Best probability", chosen_prob)

        best = []
        for i in range(len(prob_list)):
            if prob_list[i] == chosen_prob:
                best.append(actual_cities[i])

        # print(best)
        chosen_one_of_faith = choice(best)

        # print("Finally, my chosen one was", chosen_one_of_faith)

        return chosen_one_of_faith

    def forget(self):
        """Re-initializes forgettable memories from ants, namely:
        - tabu list
        - tour
        """

        self.tabu = []
        self.tour = []


def tau(i, j):
    """Calculates new pheromone value for i,j.
    New pheromone value replaces pheromone values
    for destination city in pheromone_map[y][x].
    """

    delta_taus = []
    row = j
    col = i
    destination = get_city_from_index(j, i)

    for ant in colony:
        if destination in ant.tour:
            delta_tau = Q
        else:
            delta_tau = 0
        delta_taus.append(delta_tau)

    pheromone_val = rho * pheromone_map[row][col] + sum(delta_taus)

    return pheromone_val


def setup_data():
    """Prepares data for evaluation of the heuristic function"""

    x = []

    for i in range(2, 21, 2):
        x.append(i)

    y = [26, -1, 4, 20, 0, -2, 19, 1, -4, 19]

    data = list(zip(x, y))

    return data


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
    This matrix stores the pheromone values for each city.
    """

    pheromone_map = []

    for j in range(len(variables)):
        aux_list = []
        for i in range(ran):
            aux_list.append(min_pheromone_lvl)
        pheromone_map.append(aux_list)

    return pheromone_map


def heur(x, a0, a1, a2, a3):
    """This is the objective function"""

    f = a0 / x ** 2 + a1 * e ** (a2 / x) + a3 * sin(x)

    return f


def create_ants(n):
    """Creates n ants, and returns their colony
    (in a list).
    """

    colony = []

    for i in range(n):
        colony.append(Ant(get_first_name(gender='female')))

    return colony


def get_index_of_city(city):
    """Helper function that transforms city to index
    in [row][col] format so that it is easier to manipulate.
    Returns a tuple in the form (row,col).
    """
    indie_j = city[1]
    indie_i = city[3:]

    return (int(indie_j), int(indie_i))


def get_city_from_index(j, i):
    """Helper function that transforms indices to a city
    in cities.
    Returns a string in the form ax_y.
    """

    mycity = 'a' + str(j) + '_' + str(i)

    return mycity


# problem-specific vars

variables = ['a0', 'a1', 'a2', 'a3']
ran = 16  # domain of variables, [0-ran]
data = setup_data()  # list of (x,y) coords

# ant system vars

t = 0  # time counter
NC = 0  # cycle counter
NCMAX = 70  # max cycles
m = 15  # number of ants
alpha = 3  # importance of the trail
beta = 1  # importance of visibility
rho = 0.5  # trail persistence
Q = 1  # quantity of trail
min_pheromone_lvl = 1

colony = create_ants(m)  # create ants
cities = setup_cities(ran, variables)  # create vertices
pheromone_map = setup_phero_map(ran, variables)  # cities pheromone lvl

for iterations in range(NCMAX):
    # place ants at random starts
    for ant in colony:
        ant.forget()
        index = randint(0, len(variables)-1)  # choose a variable
        ant.pos = choice(cities[index])  # choose a value
        ant.tour.append(ant.pos)
        # Update tabu list
        for row in cities:
            for city in row:
                if city[0:2] == ant.pos[0:2]:
                    ant.tabu.append(city)

    # constructing solution

    for ant in colony:
        while len(ant.tabu) != 64:
            # Choose the town j to move to, with calculated probability.
            next_town = ant.choose_town()
            ant.tour.append(next_town)
            # Move the ant to town j.
            ant.pos = next_town
            # Update tabu list accordingly
            for row in cities:
                for city in row:
                    if city[0:2] == ant.pos[0:2]:
                        ant.tabu.append(city)
            print(ant)

    for ant in colony:
        # Evaluate performance.
        myeval = []
        mytour = sorted(ant.tour)
        mya0 = int(mytour[0][3:])
        mya1 = int(mytour[1][3:])
        mya2 = int(mytour[2][3:])
        mya3 = int(mytour[3][3:])

        for (x, y) in data:
            myeval.append(heur(x, mya0, mya1, mya2, mya3))
        myminimize = []

        for i in range(len(data)):
            myminimize.append(abs(data[i][1] - myeval[i]))

        ant.eval = sum(myminimize)

        if ant.eval < ant.best_eval or ant.best_eval is 0:
            # Update shortest tour found.
            ant.best_eval = ant.eval
            ant.best_tour = ant.tour

        print(ant)

    # Update pheromone trail
    for ant in colony:
        for step in ant.tour:
            indices = get_index_of_city(step)
            j = indices[0]
            i = indices[1]
            pheromone_map[j][i] = tau(i, j)

    t = t + len(variables)
    NC += 1

    best_evals = []
    for ant in colony:
        best_evals.append(ant.best_eval)

    best_eval_so_far = min(best_evals)
    for ant in colony:
        if best_eval_so_far == ant.best_eval:
            best_tour_so_far = ant.best_tour
            best_ant = ant.name

    print("Best tour so far is {0}, with cost {1},"
          " and was found by {2}!".format(
           best_tour_so_far, best_eval_so_far, best_ant))
print('================')
print("Best tour was {0}, with cost {1},"
      " and was found by {2}!".format(
       best_tour_so_far, best_eval_so_far, best_ant))
