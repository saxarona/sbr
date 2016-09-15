"""
Othello7

A01170065 - Xavier Sánchez
A01299000 - Erim Sezer

This is the Othello (Reversi) game.
This implementation needs to run alpha_beta_search function from
the games module.

We use the same convention used in AIMA:
- actions in lowercase.
- states in UPPERCASE.

We need some basic stuff for the game to work:
- The state as a string, like 'A'.
- The actions in a LIST.

The available MINIMAX tree is a dictionary of dictionaries:
each state is a dictionary that maps actions (keys) to states (values).
Since this is a map inside a map, a useful way to get to the actions
can be seen in the Fig52Game class, in the games module:

>>> list(mydict.get(state, {}).keys())

This will get all keys (actions) of a state, or get an empty dictionary
if state has no available actions.

The utilities of all states can be stored in another dictionary
that maps states to its utility.

The board of the game is a dictionary that maps a cell (x,y)
to its player: {(x,y) : Player}, where Player is WHITE or BLACK.

This needs to be saved in a namedtuple called GameState:

>>> GameState(to_move, utility, board, moves)

to_move is the player whose turn it is now.
utility is a cached utility.
board is the board as a dictionary.
moves is a list of actions.

When checking neighborhoods, the following rules are followed:
If a cell is in (x,y), then:
- N is (x, y-1)
- NE is (x+1, y-1)
- E is (x+1, y)
- SE is (x+1, y+1)
- S is (x, y+1)
- SW is (x-1, y+1)
- W is (x-1, y)
- NW is (x-1, y-1)
"""

# TODO
# Validate actions--DONE!
# Implement actions and changes
# Create heuristic function
# Calculate Utilities

from games import *

# Change what the players are using in the board

WHITE = 'W'
BLACK = 'B'
EMPTY = '0'


class Othello7(Game):
    """This class extends Game class from games module.
    All method definitions need to be implemented here.
    """

    def __init__(self):
        self.moves = []
        self.initial = GameState(to_move=BLACK, utility=0,
                                 board=self.build_board(), moves=self.moves)
        self.current_state = self.initial

    def build_board(self):
        """Construct initial board.
        White pieces are using WHITE constant,
        while Black pieces use BLACK constant.
        """
        board = {}

        for j in range(1, 9):
            for i in range(1, 9):
                board[(i, j)] = EMPTY

        # Initial distribution of pieces

        board[(4, 4)] = WHITE
        board[(5, 5)] = WHITE
        board[(4, 5)] = BLACK
        board[(5, 4)] = BLACK

        return board

    def get_pos(self, state):
        """Helper function that returns the position
        of all state.to_move pieces in state.
        The return value is a list with all positions (x,y)
        of color pieces, which are the keys of the state dictionary.
        """

        pos = []
        if state.to_move == BLACK:
            obj = WHITE
        else:
            obj = BLACK

        for each_item in state.board.items():
            if each_item[1] == obj:
                pos.append(each_item[0])

        return pos

    def check_neighborhood(self, cell, objective):
        """Check cell's neighborhood in order to find objective.
        cell should be a tuple with the form (x,y).
        Returns a list with the contents of neighborhood as:
        >>> [N, NE, E, SE, S, SW, W, NW]
        Where N is North, and so on.
        """
        neighborhood = []

        board = self.current_state.board

        # check N
        north = board.get((cell[0], cell[1]-1))
        if north == objective:
            print("Found {0} in north".format(objective))  # debug print
            neighborhood.append((cell[0], cell[1]-1))

        # check NE
        northeast = board.get((cell[0]+1, cell[1]-1))
        if northeast == objective:
            print("Found {0} in northeast".format(objective))  # debug print
            neighborhood.append((cell[0]+1, cell[1]-1))

        # check E
        east = board.get((cell[0]+1, cell[1]))
        if east == objective:
            print("Found {0} in east".format(objective))  # debug print
            neighborhood.append((cell[0]+1, cell[1]))

        # check SE
        southeast = board.get((cell[0]+1, cell[1]+1))
        if southeast == objective:
            print("Found {0} in southeast".format(objective))  # debug print
            neighborhood.append((cell[0]+1, cell[1]+1))

        # check S
        south = board.get((cell[0], cell[1]+1))
        if south == objective:
            print("Found {0} in south".format(objective))  # debug print
            neighborhood.append((cell[0], cell[1]+1))

        # check SW
        southwest = board.get((cell[0]-1, cell[1]+1))
        if southwest == objective:
            print("Found {0} in southwest".format(objective))  # debug print
            neighborhood.append((cell[0]-1, cell[1]+1))

        # check W
        west = board.get((cell[0]-1, cell[1]))
        if west == objective:
            print("Found {0} in west".format(objective))  # debug print
            neighborhood.append((cell[0]-1, cell[1]))

        # check NW
        northwest = board.get((cell[0]-1, cell[1]-1))
        if northwest == objective:
            print("Found {0} in northwest".format(objective))  # debug print
            neighborhood.append((cell[0]-1, cell[1]-1))

        return neighborhood

    def check_empty_neigh(self, pos):
        """Check for empty neighbors of color pieces in
        the current state.
        pos is a list of tuples (x,y) where color pieces
        are located.
        """

        empties = []

        for each_item in pos:
            empties = empties + self.check_neighborhood(each_item, EMPTY)

        print("My empty neighbors are", empties)  # debug

        return empties

    def get_direction(self, cell_a, cell_b):
        """Check the direction of cell_b from cell_a.
        Returns a string in the form of 'NE', and such.
        """
        print("Getting direction from {0} to {1}".format(cell_a, cell_b))

        dirs = {'N': (0, -1), 'NE': (1, -1), 'E': (1, 0),
                'SE': (1, 1), 'S': (0, 1), 'SW': (-1, 1),
                'W': (-1, 0), 'NW': (-1, -1)}

        diff = (cell_b[0] - cell_a[0], cell_b[1] - cell_a[1])

        for each_dir, each_val in dirs.items():
            if each_val == diff:
                direction = each_dir

        print("I guess direction is {0}".format(direction))
        return direction

    def check_direction(self, cell, direction, objective):
        """Check direction of cell looking for objective.
        Returns true if objective is found, false otherwise.
        """
        not_found = True
        x = cell[0]
        y = cell[1]

        dirs = {'N': (0, -1), 'NE': (1, -1), 'E': (1, 0),
                'SE': (1, 1), 'S': (0, 1), 'SW': (-1, 1),
                'W': (-1, 0), 'NW': (-1, -1)}

        mydir = dirs[direction]

        if objective == BLACK:
            mypiece = WHITE
        else:
            mypiece = BLACK

        print("Letting you know my direction is", direction)
        print("Im looking for {0}, and will stop if I found {1}".format(
            objective, mypiece))
        print("You should know mydir is", mydir)

        while not_found:
            # check there's room for search!
            print("There's a {0} in this direction".format(
                self.current_state.board[(x + mydir[0], y + mydir[1])]))

            # get value of cell in direction from cell
            if self.current_state.board[(
                    x + mydir[0], y + mydir[1])] == mypiece:
                return True
            elif self.current_state.board[(
                    x + mydir[0], y + mydir[1])] == EMPTY:
                not_found = False
            elif self.current_state.board[(
                    x + mydir[0], y + mydir[1])] is None:
                not_found = False
            # if its objective, return true
            x = x + mydir[0]
            y = y + mydir[1]

            print('Now checking cell at {0}'.format((x, y)))

        print("Then {0} is not valid".format(cell))

        return False

    def validate_moves(self, empty):
        """Validates which cells are available to occupy.
        empty parameter is a list of empty spaces.
        """
        valid_moves = []

        if self.current_state.to_move == BLACK:
            obj = WHITE
        elif self.current_state.to_move == WHITE:
            obj = BLACK

        for each_empty in empty:
            print("Analyzing {0} now".format(each_empty))
            neighborhood = self.check_neighborhood(each_empty, obj)
            for each_neigh in neighborhood:
                dir_of_obj = self.get_direction(each_empty, neighborhood[0])
                if self.check_direction(each_empty, dir_of_obj, obj):
                    if each_empty not in valid_moves:
                        valid_moves.append(each_empty)

        # Check for whites in dir
        # if whites in dir:
        # if last occurrence of white + 1 in dir is mycolor:
        # then valid move

        return valid_moves

    def actions(self, state):
        """Returns a list of the allowed moves at this point.
        state is a board, a list of lists?
        """

        acts = []  # meanwhile

        # get position of all whites
        pos = self.get_pos(state)

        # search for empty spaces adjacent to whites
        empties = self.check_empty_neigh(pos)

        # check if empty are valid
        acts = self.validate_moves(empties)

        return acts

    def result(self, state, move):
        """Returns the state resulting from making a move in state."""

        next_state = GameState(
                to_move=(WHITE if state.to_move == BLACK else BLACK),
                utility=self.compute_utility(board, move, state.to_move),
                board=board, moves=moves)

        return next_state

    def utility(self, state, player):
        """Returns the value of this final state to player."""

        value = 0  # meanwhile

        return value

    def terminal_test(self, state):
        """Returns True if this is a final state for the game."""

        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""

        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""

        state = self.initial  # test
        for j in range(1, 9):
            line = []
            for i in range(1, 9):
                line.append(state[i, j])
            print(line)

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


othello = Othello7()

print("Mah moves are", othello.actions(othello.current_state))
