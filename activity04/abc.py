"""
ABC
1170065 Xavier Sánchez
1299000 Erim Sezer

The basic algorithm proposed by Karaboga in 2005 is something like this:

1. Initialize n scout bees with a random search and evaluate their aptitude.
2. Select m best sites for a neighbor-search.
3. Select e sites for elite patches, such that e < m.
4. Select m - e sites for normal patches.
5. Determine patch-size, usually denoted as ngh.
6. Repeat until max_iterations:
7. Create bees for the patches:
    - some for elite patches
    - some_more for normal patches, such that some > some_more
8. Select bee with best evaluation for each patch.
9. Asign n - m bees to randomly search again.
10. Select bee with best evaluation this iteration, and GOTO 6.
"""

from math import e, sin
from names import *
from random import *


class Bee(object):
    """This is the Bee class.
    A Bee is a solution that contains:
    - an a0
    - an a1
    - an a2
    - an a3
    - a human-readable name
    - the evaluation of its current solution
    - a patch where the bee stands
    """
    def __init__(self, name):
        self.name = name + "_" + str(randint(0, 100))
        self.a0 = None
        self.a1 = None
        self.a2 = None
        self.a3 = None
        self.eval = 1000
        self.patch = None

    def __str__(self):
        return("{0}: My evaluation is {1}, "
               "My distribution is a0={2}, a1={3}, a2={4}, a3={5}, "
               "and I am in patch {6}".format(
                self.name, self.eval, self.a0, self.a1,
                self.a2, self.a3, self.patch))

    def evaluate(self):
        """Evaluate this bee's position"""

        myeval = []
        mya0 = self.a0
        mya1 = self.a1
        mya2 = self.a2
        mya3 = self.a3

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


def create_bees(n):
    """Creates n bees, and returns their hive
    (in a list).
    """

    hive = []

    for i in range(n):
        hive.append(Bee(get_first_name(gender='female')))

    return hive


def assign_location(beehive, ref=None):
    """Helper function to assign location of bees.
    This function randomly selects a location for bees
    in a 4-dimensional space.
    When optional argument ref is provided, bees will be
    allocated to patch of reference. E.g.,
    bee.a0  will be a random integer from ref.a0 - ngh
    to ref.a0 + ngh.
    """
    if ref is None:
        for bee in beehive:
            bee.a0 = randint(0, 15)
            bee.a1 = randint(0, 15)
            bee.a2 = randint(0, 15)
            bee.a3 = randint(0, 15)
    else:
        refa0 = ref.a0
        refa1 = ref.a1
        refa2 = ref.a2
        refa3 = ref.a3

        for bee in beehive:
            bee.a0 = randint(refa0 - ngh, refa0 + ngh)
            bee.a1 = randint(refa1 - ngh, refa1 + ngh)
            bee.a2 = randint(refa2 - ngh, refa2 + ngh)
            bee.a3 = randint(refa3 - ngh, refa3 + ngh)


def val_to_bee(val):
    """Look for value in existing bee groups.
    If value is found, then return the bee.
    Else, return False"""

    found = False

    for bee in hive:
        if val == bee.eval:
            chosen = bee
            found = True
            break

    if found:
        return chosen
    else:
        return found


def print_group(group):
    """Helper function to print all members of group"""
    for bee in group:
        print(bee)


def bees_to_patches(group):
    """Helper function that returns a list of length n,
    where n is the number of patches present in the group"""

    known_patches = []
    patches = []

    for bee in group:
        if bee.patch is not None:
            if bee.patch not in known_patches:
                known_patches.append(bee.patch)

    for patch in known_patches:
        aux_list = []
        for bee in group:
            if bee.patch == patch:
                aux_list.append(bee)
        patches.append(aux_list)

    return patches


# problem-specific vars
data = setup_data()  # list of (x,y) coords

# bee colony vars
n = 10  # number of bees
m = 5  # number of patches
e = 2  # number of elite-patches
ne = 2  # number of bees for elite-patches
np = m-e  # number of normal-patches
nnp = 1  # number of bees for normal-patches
ngh = 3  # size of patches, this means look for patch center +- 1
iterations = 0
max_iterations = 50
best_bee_ever = Bee("Test")

# create bees
scout_group = create_bees(n)
hive = scout_group

# assign random location for bees
assign_location(hive)

while iterations < max_iterations:
    # evaluate location of the bees
    evaluations = []

    for bee in hive:
        bee.evaluate()
        evaluations.append(bee.eval)
        print(bee)

    # getting elite-patches bees
    elite_evals = []

    for i in range(e):
        elite_evals.append(min(evaluations))
        evaluations.remove(min(evaluations))

    # print("elite_evals is", elite_evals)  # debug

    elite_bees = []

    for i in elite_evals:
        bee = val_to_bee(i)
        elite_bees.append(bee)
        bee.patch = get_first_name(gender='male') + "_" + str(randint(0, 100))

    print("================\n"
          "Elite bees are:")

    print_group(elite_bees)

    # getting normal-patches bees
    patches_evals = []

    for i in range(np):
        patches_evals.append(min(evaluations))
        evaluations.remove(min(evaluations))

    # print("Patches_evals is", patches_evals)  # debug

    patches_bees = []

    for i in patches_evals:
        bee = val_to_bee(i)
        patches_bees.append(bee)
        bee.patch = get_first_name(gender='male') + "_" + str(randint(0, 100))

    print("================\n"
          "Patches bees are:")

    print_group(patches_bees)

    # create new bees for elite-patches

    for bee in elite_bees:
        work_group = create_bees(ne)  # I've created ne bees
        assign_location(work_group, bee)
        for new_bee in work_group:
            new_bee.patch = bee.patch  # Added each new_bee to its patch
            new_bee.evaluate()  # Added evaluation for each new_bee
        elite_bees = elite_bees + work_group  # Added new_bees to elite_bees
        hive = hive + work_group  # And also to the bee count!

    print("================\n"
          "New elite bees are:")

    print_group(elite_bees)

    # create new bees for normal-patches

    for bee in patches_bees:
        work_group = create_bees(nnp)  # I've created nnp bees
        assign_location(work_group, bee)
        for new_bee in work_group:
            new_bee.patch = bee.patch  # Added each new_bee to its patch
            new_bee.evaluate()  # Added evaluation for each new_bee
        patches_bees = patches_bees + work_group  # Added them to patches_bees
        hive = hive + work_group  # And also to the bee count!

    print("================\n"
          "New patches bees are:")

    print_group(patches_bees)

    elite_patches = bees_to_patches(elite_bees)
    patches = bees_to_patches(patches_bees)
    # select bee with best evaluation for each patch

    best_bees_evals = []
    for each_patch in elite_patches:
        evaluations = []
        for bee in each_patch:
            evaluations.append(bee.eval)
        best_bees_evals.append(min(evaluations))

    for each_patch in patches:
        evaluations = []
        for bee in each_patch:
            evaluations.append(bee.eval)
        best_bees_evals.append(min(evaluations))

    best_bees = []

    for each_eval in best_bees_evals:
        best_bees.append(val_to_bee(each_eval))

    print("================\n"
          "Best bees are:")
    print_group(best_bees)

    # Assign n-m bees to randomly search again

    new_scout_group = create_bees(n-m)  # create n-m scouting bees
    assign_location(new_scout_group)
    for bee in new_scout_group:
        bee.evaluate()

    hive = best_bees + new_scout_group

    aux_list = []
    for bee in hive:
        aux_list.append(bee.eval)

    best_val = min(aux_list)
    best_bee = val_to_bee(best_val)

    if best_bee_ever.eval is None or best_bee.eval < best_bee_ever.eval:
        best_bee_ever = best_bee

    print("Best bee this iteration was", str(best_bee))
    print("===============")
    print("Best bee so far is", str(best_bee_ever))
    iterations += 1
