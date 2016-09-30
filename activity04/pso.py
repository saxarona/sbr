"""
PSO
1170065 Xavier Sánchez
1299000 Erim Sezer

Particle Swarm Optimization is based on ducks flying.
Each duck has a velocity, and also remembers its best position.
Also, each duck has a neighborhood, and knows the best
neighborhood position.

These three components are combined to obtain the direction
which the duck shall follow.
In the end, all ducks will move near the best spot.

The code is pretty straight-forward, like most metaheuristics.
Instead of using particles, we'll be using ducks:

1. Initialize ducks
2. For each duck:
    - Calculate its evaluation
    - If its evaluation is best than his best, then update.
3. Choose duck with best evaluation as gbest
4. For each duck:
    - Calculate new velocity with eq. (a)
    - Calculate new position with eq. (b)
5. GOTO 2
6. Repeat while iterations < max_iterations

These are the equations:

Eq. (a):
duck.vel = c0 * duck.vel +
           c1 * rand() * (duck.pbest - duck.pos) +
           c2 * rand() * (duck.gbest - duck.pos)

Eq. (b):
duck.pos = duck.pos + duck.vel
"""

from math import e, sin
from names import *
from random import *


class Duck(object):
    """This is the Duck class.
    A Duck is a vector that contains:
    - a velocity
    - a position (in the <a0, a1, a2, a3> sense)
    - the evaluation of its current position
    - a neighborhood
    - a personal best position
    - a personal best evaluation
    """
    def __init__(self, name):
        self.name = name + "_" + str(randint(0, 100))
        self.velocity = 0
        self.pos = [None, None, None, None]
        self.neighbors = []
        self.eval = 10000
        self.best_pos = []
        self.best_eval = self.eval

    def __str__(self):
        return("{0}: My evaluation is {1}, "
               "My position is a0={2}, a1={3}, a2={4}, a3={5}, "
               "and my velocity is {6}".format(
                self.name, self.eval, self.pos[0], self.pos[1],
                self.pos[2], self.pos[3], self.velocity))

    def evaluate(self):
        """Evaluate this duck's position"""

        myeval = []
        mya0 = self.pos[0]
        mya1 = self.pos[1]
        mya2 = self.pos[2]
        mya3 = self.pos[3]

        for (x, y) in data:
            myeval.append(heur(x, mya0, mya1, mya2, mya3))

        myminimize = []

        for i in range(len(data)):
            myminimize.append(abs(data[i][1] - myeval[i]))

        self.eval = sum(myminimize)


def setup_data():
    """Prepares data for evaluation of the heuristic function"""

    x = []

    for i in range(2, 21, 2):
        x.append(i)

    y = [26, -1, 4, 20, 0, -2, 19, 1, -4, 19]

    data = list(zip(x, y))

    return data


def heur(x, a0, a1, a2, a3):
    """This is the objective function"""

    f = a0 / x ** 2 + a1 * e ** (a2 / x) + a3 * sin(x)

    return f


def val_to_duck(val):
    """Look for value in existing neighborhoods.
    If value is found, then return the duck.
    Else, return False
    """

    found = False

    for duck in flock:
        if val == duck.eval:
            chosen = duck
            found = True
            break

    if found:
        return chosen
    else:
        return found

# problem-specific vars
data = setup_data()  # list of (x,y) coords

# particle swarm vars
n = 10  # number of ducks
c0 = 1  # importance of velocity
c1 = 1  # importance of personal best
c2 = 1  # importance of neighborhood best
vmax = 3  # max velocity i.e. a0 = randint(a0 - 3, a0 + 3)
iterations = 0
max_iterations = 50
best_duck_ever = Duck("Test")

# 1. Initialize ducks
# 2. For each duck:
#     - Calculate its evaluation
#     - If its evaluation is best than his best, then update.
# 3. Choose duck with best evaluation as `gbest`
# 4. For each duck:
#     - Calculate new velocity with eq. (a)
#     - Calculate new position with eq. (b)
# 5. GOTO 2
# 6. Repeat `while iterations` < `max_iterations`