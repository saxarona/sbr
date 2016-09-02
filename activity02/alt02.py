# alt02.py
# Since this looks terrible, I'm redoing everything. I'm sorry.

from agents import *
from grid import *
from search import *
from utils import *
from lib import *   # This is the redblob games lib for hexagons!
from collections import defaultdict

class Hexagon(Problem):
    """docstring for Hexagon"""
    def __init__(self, initial_state, goal=None):
        self.initial_state = initial_state
        self.goal = goal
        self.all_acts = ['L', 'BL', 'BR', 'R', 'TR', 'TL']  # possible actions
        self.grid = self.create_grid()

    def actions(self, state):
        """Return the actions that can be executed in the given state.
        The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        acts = []
        for act in self.all_acts:
            # check if act is legal
            if (is_legal(act)):
                acts.append(act) # if it is, append to acts
            
        return acts

        
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        pass


    def create_grid(self):
        """Grid creation!"""

        grid = defaultdict()  # This is the grid dictionary (hash table)

        # The grid is named using capital letters for rows and numbers for each
        # column.

        grid['A1'] = Hex(0, 2, -2)
        grid['A2'] = Hex(1, 1, -2)
        grid['A3'] = Hex(2, 0, -2)
        grid['B1'] = Hex(-1, 2, -1)
        grid['B2'] = Hex(0, 1, -1)
        grid['B3'] = Hex(1, 0, -1)
        grid['B4'] = Hex(2, -1, -1)
        grid['C1'] = Hex(-2, 2, 0)
        grid['C2'] = Hex(-1, 1, 0)
        grid['C3'] = Hex(0, 0, 0)  # Center
        grid['C4'] = Hex(1, -1, 0)
        grid['C5'] = Hex(2, -2, 0)
        grid['D1'] = Hex(-2, 1, 1)
        grid['D2'] = Hex(-1, 0, 1)
        grid['D3'] = Hex(0, -1, 1)
        grid['D4'] = Hex(1, -2, 1)
        grid['E1'] = Hex(-2, 0, 2)
        grid['E2'] = Hex(-1, -1, 2)
        grid['E3'] = Hex(0, -2, 2)

        return grid

    def get_neighbors(self, target, mode):
        """
        Get neighbors of the target and returns a list of 6 neighbors.
        Each neighbor is a tuple with 2 elements (direction, cellname)
        The first element is its direction (ready for use with hex_neighbor),
        and the second element is the name of the hexagonal cell (key in grid).
        """

        houses = []
        neighborhood = []

        for i in range(6):
            houses.append(hex_neighbor(target, i))

        for home in houses:
            for keyes, val in self.grid.items():
                if(val == home):
                    neighborhood.append((houses.index(home), keyes))
        if mode != 'hex':
            mody = neighborhood
        else:
            mody = houses

        return mody


    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        pass