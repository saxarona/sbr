"""Calcudoku Light

A01170065 - Xavier Sánchez
A01299000 - Erim Sezer

The Calcudoku Light is described as a CSP:
- Each cell is a variable.
- The domain of each variable (cell) is {1, 2 , 3, 4}.
- Variables have different constraints, explained below.

Constraints:
- Each value should appear only once per column.
- Each value should appear only once per row.
- Each cell is restricted to the values that yield
the goal for each group.


Using the program:
Simply change the CHALLENGE constant from 1 to 4 and run it.
A list of {variables: value} will be printed as the solution.

Additional inline comments are presented in the code
that further detail specific parts of the program.
"""

from csp import *

# Change this from 1 - 4 to solve an instance!
CHALLENGE = 4


def calcudoku_constraint(A, a, B, b):
    """This is calcudoku's constraint function.

    Constraints change depending on the CHALLENGE constant.
    This function returns True if the value a of variable A
    and the value b of variable B satisfy the constraints.
    If not, then returns False.
    """

    if CHALLENGE == 1:

        if A == 'A1' and B == 'B1':
            return a != b and (a + b == 3)
        elif A == 'A2' and B == 'B2':
            return a != b and (a + b == 7)
        elif A == 'A3' and B == 'A4':
            return a != b and (a + b == 6)
        elif A == 'B3' and B == A:
            return a == 1
        elif A == 'B4' and B == 'C4':
            return a != b and (a + b == 4)
        elif A == 'C1' and B == 'C2':
            return a != b and (a + b == 6)
        elif A == 'C3' and B == 'D3':
            return a != b and (a + b == 5)
        elif A == 'D1' and B == 'D2':
            return a != b and (a + b == 4)
        elif A == 'D4' and B == A:
            return a == 4
        else:
            return not (a == b)

    elif CHALLENGE == 2:

        if A == 'A1' and B == 'A2':
            return a != b and (a * b == 4)
        elif A == 'A3' and B == A:
            return a == 2
        elif A == 'A4' and B == 'B4':
            return a != b and (a * b == 3)
        elif A == 'B1' and B == 'C1':
            return a != b and (a * b == 8)
        elif A == 'B2' and B == 'B3':
            return a != b and (a * b == 6)
        elif A == 'C2' and B == 'D2':
            return a != b and (a * b == 3)
        elif A == 'C3' and B == 'C4':
            return a != b and (a * b == 4)
        elif A == 'D1' and B == A:
            return a == 3
        elif A == 'D3' and B == 'D4':
            return a != b and (a * b == 8)
        else:
            return not (a == b)

    elif CHALLENGE == 3:

        if A == 'A1' and B == A:
            return a == 2
        elif A == 'A2' and B == 'A3':
            return a != b and (abs(a - b) == 1)
        elif A == 'A4' and B == 'B4':
            return a != b and (a + b == 4)
        elif A == 'B1' and B == 'B2':
            return a != b and (a + b == 6)
        elif A == 'B3' and B == 'C3':
            return a != b and (abs(a - b) == 3)
        elif A == 'C1' and B == 'D1':
            return a != b and (a + b == 4)
        elif A == 'C2' and B == A:
            return a == 3
        elif A == 'C4' and B == 'D4':
            return a != b and (abs(a - b) == 2)
        elif A == 'D2' and B == 'D3':
            return a != b and (abs(a - b) == 1)
        else:
            return not (a == b)

    elif CHALLENGE == 4:

        if A == 'A1' and B == 'A2':
            return a != b and (a * b == 2)
        elif A == 'A3' and B == A:
            return a == 4
        elif A == 'A4' and B == 'B4':
            return a != b and (a * b == 6)
        elif A == 'B1' and B == 'C1':
            return a != b and (a / b == 4 or b / a == 4)
        elif A == 'B2' and B == 'B3':
            return a != b and (a * b == 12)
        elif A == 'C2' and B == 'D2':
            return a != b and (a * b == 6)
        elif A == 'C3' and B == 'C4':
            return a != b and (a / b == 2 or b / a == 2)
        elif A == 'D1' and B == A:
            return a == 3
        elif A == 'D3' and B == 'D4':
            return a != b and (a / b == 4 or b / a == 4)
        else:
            return not (a == b)

# Here we begin constructing the problem instance
# This is the grid, which consists of 4 rows.
# Each row is labeled with a letter from A to D,
# and each column is labeled with a number from 1 to 4.
# The resulting cells are labeled as A1, ..., D4.

A = ['A1', 'A2', 'A3', 'A4']
B = ['B1', 'B2', 'B3', 'B4']
C = ['C1', 'C2', 'C3', 'C4']
D = ['D1', 'D2', 'D3', 'D4']

# variables is a list containing all cells in Calcudoku
variables = A + B + C + D

# Both the domains and the neighbors are declared as dictionaries.
# There's an entry in each dictionary for all variables,
# where conflicting neighbors and domain values for each variable
# are stored.

domains = {}
neighbors = {}

# Here we fill-in the domain for each cell,
# instead of declaring it manually.

for each_cell in variables:
    domains[each_cell] = [1, 2, 3, 4]

# Now we fill-in all conflicting neighbors for each var,
# instead of declaring them manually.

for each_cell in variables:
    for each_row in [A, B, C, D]:
        if each_cell in each_row:
            neighbors[each_cell] = list(each_row)
            neighbors[each_cell].remove(each_cell)
    for each_cell2 in variables:
        if each_cell[-1] in each_cell2:
            neighbors[each_cell].append(each_cell2)
    if each_cell in neighbors[each_cell]:
        neighbors[each_cell].remove(each_cell)

# CHALLENGE specific domains and constraints are re-defined here.

if CHALLENGE == 1:
    domains['B3'] = [1]
    domains['D4'] = [4]

elif CHALLENGE == 2:
    domains['A3'] = [2]
    domains['D1'] = [3]

elif CHALLENGE == 3:
    domains['A1'] = [2]
    domains['C2'] = [3]

elif CHALLENGE == 4:
    domains['A3'] = [4]
    domains['D1'] = [3]

# Now we declare our Calcudoku class


class Calcudoku(CSP):
    """Make a CSP for the Calcudoku."""

    def __init__(self, variables, domains, neighbors, constraints):
        """Initialize data structures for Calcudoku."""
        CSP.__init__(self, None, domains, neighbors, constraints)

# This is where our Calcudoku class is being instantiated.

problem = Calcudoku(variables, domains, neighbors, calcudoku_constraint)

# You can uncomment these lines to view specific parts of the CSP

# print("My vars:", problem.variables)  # debug
# print("My domains", problem.domains)  # debug
# print("My neighborhood", problem.neighbors)  # debug

# The solution is printed here.

print("Solution is:", backtracking_search(
      problem, select_unassigned_variable=mrv, inference=forward_checking))
