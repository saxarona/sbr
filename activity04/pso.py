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
from copy import deepcopy


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
        self.velocity = [0, 0, 0, 0]
        self.pos = [None, None, None, None]
        self.neighbors = []
        self.eval = 10000
        self.best_pos = [None, None, None, None]
        self.best_eval = self.eval
        self.gbest_pos = [None, None, None, None]
        self.gbest_eval = None

    def __str__(self):
        return("{0}: My evaluation is {1}, "
               "My position is a0={2}, a1={3}, a2={4}, a3={5}, "
               "and my velocity is {6}. My best so far is {7}".format(
                self.name, self.eval, self.pos[0], self.pos[1],
                self.pos[2], self.pos[3], self.velocity, self.best_eval) +
               "\nGbest is a0={0}, a1={1}, a2={2}, a3={3}".format(
                self.gbest_pos[0], self.gbest_pos[1],
                self.gbest_pos[2], self.gbest_pos[3]))

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

    def update_best(self):
        """Update personal best"""

        if self.eval < self.best_eval:
            self.best_eval = self.eval
            self.best_pos = self.pos

        if self.best_pos[0] is None:
            self.best_pos = self.pos

    def guess_gbest(self):
        """Gets position and evaluation of gbest"""
        neighbors_evals = []
        for duck in self.neighbors:
            neighbors_evals.append(duck.eval)

        self.gbest_eval = min(neighbors_evals)
        self.gbest_pos = val_to_duck(self.gbest_eval).pos

    def calculate_velocity(self):
        """Calculates velocity of the duck.
        Velocity is a 4-dimensional vector in the form of <a0, a1, a2, a3>.
        It is a sum of three vectors a + b + c, where
        a is the past velocity vector,
        b is the personal best vector and
        c is the group best vector.
        """
        new_velocity = []
        past_velocity = []
        personal = []
        group = []

        # fill vectors
        for i in range(len(self.pos)):
            past_velocity.append(c0 * self.velocity[i])
            personal.append(c1 * randint(0 - vmax, vmax) *
                            (self.best_pos[i] - self.pos[i]))
            group.append(c2 * randint(0 - vmax, vmax) *
                         (self.gbest_pos[i] - self.pos[i]))
            # fill new_velocity vector
            new_velocity.append(past_velocity[i] +
                                personal[i] + group[i])

            if abs(new_velocity[i] - self.velocity[i]) > vmax:
                if new_velocity[i] < 0:
                    new_velocity[i] = 0 - vmax
                else:
                    new_velocity[i] = vmax

        self.velocity = new_velocity

    def calculate_position(self):
        """Calculates new position of the duck.
        New position is updated with the sum of velocity vector
        plus the previous position vector
        """
        new_position = []

        for i in range(len(self.pos)):
            new_position.append(self.pos[i] + self.velocity[i])

        print("New position is", new_position)

        self.pos = new_position


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


def create_ducks(n):
    """Generate n ducks for PSO solving and returns them in a list."""
    flock = []
    for i in range(n):
        flock.append(Duck(get_first_name(gender="male")))

    return flock


def print_group(group):
    for duck in group:
        print(duck)


def assign_location(flock):
    """Helper function to assign location of ducks.
    This function randomly selects a location for ducks
    in a 4-dimensional space.
    """
    for duck in flock:
        mya0 = randint(0, 15)
        mya1 = randint(0, 15)
        mya2 = randint(0, 15)
        mya3 = randint(0, 15)

        duck.pos = [mya0, mya1, mya2, mya3]


def assign_neighbors(flock):
    """Helper function to assign duck neighborhood.
    This function checks index of duck in flock and
    updates accordingly.
    By default, neighborhood is of size 3,
    i.e. duck.neighbors = [duck - 1, duck + 1].
    """

    for duck in flock:
        if flock.index(duck) == 0:
            duck.neighbors.append(flock[-1])
            duck.neighbors.append(duck)
            duck.neighbors.append(flock[1])
        elif flock.index(duck) == len(flock) - 1:
            duck.neighbors.append(flock[-2])
            duck.neighbors.append(duck)
            duck.neighbors.append(flock[0])
        else:
            duck.neighbors.append(flock[flock.index(duck)-1])
            duck.neighbors.append(duck)
            duck.neighbors.append(flock[flock.index(duck)+1])


# problem-specific vars
data = setup_data()  # list of (x,y) coords

# particle swarm vars
n = 10  # number of ducks
c0 = 1  # importance of velocity
c1 = 2  # importance of personal best
c2 = 2  # importance of neighborhood best
vmax = 3  # max velocity i.e. abs(a0(t+1) - a0(t)) <=  3
iterations = 0
max_iterations = 50
best_duck_ever = Duck("Test")

# 1. Initialize ducks
flock = create_ducks(n)
assign_location(flock)
assign_neighbors(flock)

# 2. For each duck:
while iterations < max_iterations:
    for duck in flock:
        duck.evaluate()  # Calculate its evaluation
        duck.update_best()  # If evaluation is best than his best, then update

    print_group(flock)

    for duck in flock:
        duck.guess_gbest()  # 3. Choose duck with best evaluation as `gbest`

    # 4. For each duck:

    for duck in flock:
        duck.calculate_velocity()  # Calculate new velocity with eq. (a)
        duck.calculate_position()  # Calculate new position with eq. (b)

    evaluations = []
    for duck in flock:
        evaluations.append(duck.eval)

    global_best_eval = min(evaluations)
    global_best_duck = deepcopy(val_to_duck(global_best_eval))

    if(best_duck_ever.eval is None or
       global_best_duck.eval < best_duck_ever.eval):
        best_duck_ever = global_best_duck

    print_group(flock)

    print("Best duck this iteration:", str(global_best_duck))
    print("===============")
    print("Best duck so far is", str(best_duck_ever))
    iterations += 1
