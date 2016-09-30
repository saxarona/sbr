# Activity02
# Intelligent Systems
# 01170065 - Xavier Sánchez Díaz
# 01299000 - Erim Sezer

from lib import *   # This is the redblob games lib for hexagons!
from collections import defaultdict
from search import *
import sys

# We need to define a "map" where to store the hexagons
# We use a class named Hex, which is a namedtuple
# that is imported (from collections.py).
# Hex objects need 3 parameters: their q, r and s coordinates
# which are relative to their x, y, z coordinates.

class Hexagon(Problem):
    """docstring for Hexagon"""
    def __init__(self, initial, goal=None):
        Problem.__init__(self, initial, goal)
        self.grid = self.create_grid()
        self.initial = self.grid[initial]  # A string in the sense of 'A1'
        self.goal = self.name_to_hex(goal)
        self.visited = [self.initial]
        self.state = self.name_to_hex(initial)
        self.all_acts = ['L', 'BL', 'BR', 'R', 'TR', 'TL']
        print("Goal is", self.goal)

    def goal_test(self,state):
        """Am I there yet?!"""

        if self.state == self.goal:
            print("WE'RE THERE, MATE!")
            self.print_path()
            sys.exit()
        
        return state == self.goal

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
        grid['C3'] = Hex(0, 0, 0)  # Center of the grid map
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

    def print_path(self):
        """
        Prints the path till termination.
        Not necessarily the shortest, of course.
        """
        mah_path =[]
        for ea in self.visited:
            mah_path.append(self.hex_to_name(ea))
        
        print("Path was:",mah_path)

        # This was actually a placeholder, since we wanted to add
        # a way to visualize movement
        # print("""
        #     _ _ 1 _ 1 _ 1 _ _
        #     _ 1 _ 1 _ 1 _ 1 _
        #     1 _ 1 _ 1 _ 1 _ 1
        #     _ 1 _ 1 _ 1 _ 1 _
        #     _ _ 1 _ 1 _ 1 _ _
        #     """)


    def actions(self, state, mode='hex'):
        """Return the actions that can be executed in the given state.
        The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""

        print(self.state)

        print("Actions input: ", state)

        if not state:
            print("No solution via this way!")
            self.print_path()
            sys.exit()
        
        acts = []
        
        my_state = (state)
        for act in self.all_acts:
            # check if act is legal
            if (self.validate_action(act, state)):
                acts.append(act) # if it is, append to acts

        # print(acts)
            
        #if mode == 'hex':
        hex_acts = []
        for ea in acts:
            hex_acts.append(self.dir_to_number(ea))
            acts = hex_acts

        print("I have finished actions function, actions are:", acts)

        return acts


    def result(self, state, action, mode='hex'):
        """Returns the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        print("Result input: ", state, action)
        
        my_state = state # self.name_to_hex(state)
        my_action = action #self.dir_to_number(action)

        if type(my_state) is str:
            my_state = self.name_to_hex(my_state)
        if type(my_action) is str:
            my_action = self.dir_to_number(my_action)

        # print(my_state, my_action)

        # valid_actions = self.actions(state)
        # print("Valid actions are:", valid_actions)

        my_result = self.neighbor_at(my_state, my_action)# hexval of the neighbor at action
        print("My result is:", my_result)
        # print("GO TO " + self.hex_to_name(my_result))

        if mode != 'hex':
            my_result = self.hex_to_name(my_result)

        print(my_result)

        self.new_state(my_result, my_action)
        print(self.state)

    def h(self, node):
        """
        This is the definition of our heuristic method.
        
        The heuristic method uses the hex_distance function
        from the redblob library. This function gets the actual
        distance from a tile to another.

        Completion rate is used to measure how close we are to the goal.
        """

        return hex_distance(node.state, self.name_to_hex(self.goal))


    def new_state(self, state, action):
        """
        Set the new state.
        """
        print("New State input: ", state, action)
        # my_action = self.dir_to_number(action)
        # my_result = (self.result(self.state, action))
        self.state = state
        print("New state is:", self.hex_to_name(self.state))

        self.visited.append(self.state)

        self.goal_test(self.state)


    def neighbor_at(self, target, my_dir, mode='hex'):
        """ Return hexval of neighbor of target at direction dir """
        print("Neighbor At input: ", target, my_dir)
        my_neighborhood = self.get_neighbors(target, 'name')

        print("Mah neighbors are:", my_neighborhood)
        # print(my_dir)

        for ea in my_neighborhood:
            if my_dir in ea:
                print("target is in neighborhood!")
                whois = self.name_to_hex(ea[1])
                break
            else:
                whois = target


        # if mode != 'hex':
        #     whois = self.hex_to_name(whois)

        print("Whois this guy:", whois)

        return whois


    def get_neighbors(self, target, mode='hex'):
        """
        Get neighbors of the target and returns a list of 6 neighbors.
        Each neighbor is a tuple with 2 elements (direction, cellname)
        The first element is its direction (ready for use with hex_neighbor),
        and the second element is the name of the hexagonal cell (key in grid).
        """

        print("Get Neighbors input: ", target)
        if type(target) is str:
            target = self.name_to_hex(target)

        if not target:
            print("No solution via this way!")
            self.print_path()
            sys.exit()

        houses = []
        neighborhood = []
        existing_houses = []

        for i in range(6):
            houses.append(hex_neighbor(target, i))

        for home in houses:
            for keyes, val in self.grid.items():
                if(val == home):
                    neighborhood.append((houses.index(home), keyes))
                    existing_houses.append(home)
        if mode != 'hex':
            mody = neighborhood
        else:
            mody = existing_houses

        return mody


    def get_coords(self, target):
        """
        Returns the coordinates of target hex.
        """
        return [target.q, target.r, target.s]


    def hex_to_name(self, target):
        """
        Converts target from hex coordinates to human-readable name.
        """
        print("hex->name input: ", target)
        for keyes, val in self.grid.items():
            if val == target:
                name = keyes

        return name


    def name_to_hex(self, target):
        """
        Converts human-readable hexagon to hexagonal coordinate system.
        """
        print("name->hex input: ", target)
        if target in self.grid:
            hexval = self.grid.get(target)

        return hexval


    def dir_to_number(self, target):
        """
        Change the name of an action to a number and returns the
        appropriate number to perform some measurements.
        """
        print("Dir->num input:", target)

        if target == 'TR':
            my_dir = 0
        elif target == 'R':
            my_dir = 1
        elif target == 'BR':
            my_dir = 2
        elif target == 'BL':
            my_dir = 3
        elif target == 'L':
            my_dir = 4
        elif target == 'TL':
            my_dir = 5

        return my_dir


    def number_to_dir(self, target):
        """
        Associates a number to a direction and returns a string.
        """

        if target == 0:
         my_dir = 'TR'
        elif target == 1:
         my_dir = 'R'
        elif target == 2:
         my_dir = 'BR'
        elif target == 3:
         my_dir = 'BR'
        elif target == 4:
         my_dir = 'L'
        elif target == 5:
         my_dir = 'TL'

        return my_dir


    def validate_action(self, action, state):
        """
        Returns true if an action is allowed in the following state
        """
        print("Validate action Input:", action, state)

        if not state:
            print("No solution via this way!")
            self.print_path()
            sys.exit()

        if type(state) is str:
            state = self.name_to_hex(state)
        if type(action) is str:
            action = self.dir_to_number(action)


        my_state = state # self.name_to_hex(state)  # convert state to hex
        my_action = action # self.dir_to_number(action)  # converts direction to number
        neighborhood = self.get_neighbors(my_state, 'name')  # look for state's neighs

        # since neighborhood is a list of tuples in the form (numdir, name)
        # we need to convert them to hex
        hex_neighborhood = []

        for house in neighborhood:
            hex_neighborhood.append((house[0],self.name_to_hex(house[1])))

        print("I'm at validate action, neighborhood is:", neighborhood)
        print("my action is", my_action)
        valid_action = False

        for house in hex_neighborhood:
            print("pls:", house)
            if my_action == house[0]:
                print("Valid action found!")
                valid_action = True
                break

        # print(hex_neighborhood)

        return valid_action


    def show_solution(goal_node):
        """Shows the solution of the problem"""
        actions = goal_node.solution()
        nodes = goal_node.path()

        print(actions)
        print(nodes)

        print('Solution:')
        print('State: ', nodes[0].state)

        for na in range(len(actions)):
            if actions[na] == 'L':
                print("Move left!")
            elif actions[na] == 'BL':
                print("Move bottom left!")
            elif actions[na] == 'BR':
                print("Move bottom right!")
            elif actions[na] == 'R':
                print("Move right!")
            elif actions[na] == 'TR':
                print("Move top right!")
            elif actions[na] == 'TL':
                print("Move top left!")
            print('State:',nodes[na+1].state)
        print('End.')


def main():
    # Uncomment to try another cases, or replace 'C2' and 'C3'
    # for some other values, from A1-3, B1-4, C1-5, D1-4 or E1-3.
    
    prob = Hexagon('C2', 'C3')  # solvable
    # prob = Hexagon('A1', 'C3')
    # prob = Hexagon('A3', 'C3')

    # print("Starting state is " + prob1.hex_to_name(prob1.initial))
    #print(prob1.validate_action('BL', 'A1'))
    # actionman = prob1.result('A1', 'L')
    # print("State is now " + prob1.hex_to_name(actionman))
    #print(prob1.actions(prob1.initial))

    goal = breadth_first_search(prob) 
    # goal = depth_first_graph_search(prob)
    
    # goal = astar_search(prob) # throws exception


if __name__ == '__main__':
    main()
