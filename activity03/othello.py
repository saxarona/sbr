"""
Othello7

A01170065 - Xavier Sánchez
A01299000 - Erim Sezer

This is the Othello (Reversi) game.
This implementation needs to run alpha_beta_search function from
the games module.

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

The heuristic function was calculated as:

h = my_pieces + my_moves + 3 * my_gains - dangerous_places * my_losses / 2

Where:
- my_pieces is the number of pieces I got on the board now.
- my_moves is number of available moves I've got for my next turn.
- my_gains is the number of pieces converted to my color after my best move,
multiplied by 3.
- dangerous_places are number of valid, empty spaces next to my pieces.
- my_losses is an estimate of the worst case scenario for my opponent's next turn.

dangerous_places is multiplied by my_losses, and then divided by 2 in order
to get the average, like "how dangerous is my next opponent's move".

Many helper functions were created in order to ease up the search of
available moves. For example, we include functions to look for neighbors,
to decode strings to directions, and get the direction from a cell to another.
Some of these functions have a prediction mode used for the calculation of utilities.
"""

# TODO
# Validate actions -- DONE!
# Implement actions and changes -- DONE!
# Create heuristic function -- DONE!
# Calculate Utilities -- DONE!

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
        Empty spaces use EMPTY constant.
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

    def get_pos(self, state, predict=False):
        """Helper function that returns the position
        of all state.to_move pieces in state.
        The return value is a list with all positions (x,y)
        of color pieces, which are the keys of the state dictionary.
        """
        print("Starting getting position with prediction as", predict)

        pos = []
        if state.to_move == BLACK and not predict:
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
        print("Starting checking neighborhoods with objective", objective)
        neighborhood = []
        print("I'm looking for neighborhood of", cell)

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
        pos is a list of tuples (x,y) where pos pieces
        are located.
        """
        print("Starting checking empty neighbors")

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

    def check_direction(self, cell, direction, objective, steps=False):
        """Check direction of cell looking for objective.
        Returns true if objective is found, false otherwise.
        If steps is true, return number of steps needed to find
        objective in direction.
        """
        print("Starting checking direction with step mode as", steps)
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

        mysteps = []

        print("Steps is set as", steps)

        if not steps:
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
        if steps:
            print("I'm in the conditional now!")
            while not_found:
                #check there's room for search!
                print("There's a {0} in this direction".format(
                    self.current_state.board[(x + mydir[0], y + mydir[1])]))
                # get value of cell in direction from cell
                # if self.current_state.board[(
                #         x + mydir[0], y + mydir[1])] == mypiece:
                #     return True
                if self.current_state.board[(
                    x + mydir[0], y + mydir[1])] == EMPTY:
                        not_found = False
                elif self.current_state.board[(
                    x + mydir[0], y + mydir[1])] is None:
                        not_found = False
                # if its objective, return true
                mysteps.append((x, y))
                x = x + mydir[0]
                y = y + mydir[1]
                print("So far, mysteps is", mysteps)
            return mysteps


        print("Then {0} is not valid".format(cell))

        return False

    def validate_moves(self, empty, predict=False):
        """Validates which cells are available to occupy.
        empty parameter is a list of empty spaces.
        """
        print("Validating moves with prediction mode", predict)
        valid_moves = []

        if self.current_state.to_move == BLACK and not predict:
            obj = WHITE
        else:
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

    def change_board(self, state, move, predict=False, obj='opp'):
        """Returns the new board, after a piece has been moved.
        The return value should be the board, a dictionary that
        maps (x,y) coordinates to players: WHITE or BLACK.
        """
        print("Starting changing board!")
        board = state.board.copy()
        print("The state is as follows")
        self.display(state)
        print(state.utility)
        print("Prediction mode is", predict)

        print("Letting you know that my move is", move)

        board[move] = state.to_move # this

        if state.to_move == BLACK and obj == 'opp':
            obj = WHITE
        elif state.to_move == WHITE or obj == 'mine':
            obj = BLACK

        print("My objective here is", obj)

        # get adjacent whites, save their coords
        obj_neighs = self.check_neighborhood(move, obj)

        the_dirs = []

        # get direction for each white, save their direction
        for each_neigh in obj_neighs:
            mydir = self.get_direction(move, each_neigh)
            the_dirs.append(mydir)

        changed_pieces = []

        # for each white, go into its direction looking for state.to_move
        for i in range(len(obj_neighs)):
            changed_pieces = changed_pieces + self.check_direction(
                obj_neighs[i], the_dirs[i], obj, steps=True)

        # in each step, save its coords
        # when you find your objective, stop searching
        if not predict:
            # turn all saved coords to state.to_move
            for each_piece in changed_pieces:
                board[each_piece] = state.to_move

            print("I'm not in predict mode, and my board looks like",board)

            # return new board
            return board

        elif predict:
            return changed_pieces


    def actions(self, state):
        """Returns a list of the allowed moves at this point.
        state is a board, a list of lists?
        """
        print("Starting getting actions!")

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
        print("Starting getting results!")

        moves = self.actions(state)
        print("These are the moves I got", moves)
        print("This is the move I was sent", move)

        board = self.change_board(state, move)

        return GameState(
            to_move=(WHITE if state.to_move == BLACK else BLACK),
            utility=self.compute_utility(state, move), board=board, moves=moves)

    def utility(self, state, player):
        """Returns the value of this final state to player."""
        print("Starting getting utility!")

        return state.utility if player == BLACK else -state.utility

    def terminal_test(self, state):
        """Returns True if this is a final state for the game."""
        print("I'm starting terminal test")

        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""

        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""

        for j in range(1, 9):
            line = []
            for i in range(1, 9):
                line.append(state.board[i, j])
            print(line)

    def compute_utility(self, state, move):
        """Compute utility for a given move.
        This is the heuristic function used to determine
        how is the player doing.
        - Number of pieces is important.
        - Number of available moves is also relevant
        - Number of pieces that are gonna change with my move
        - Number of dangerous places that I'm leaving
        - Number of pieces changed in each dangerous place

        h = my_pieces + my_moves + my_gains
            - avg_of(dangerous_places * my_losses)
        """
        print('Im computing utilities for {0} and my move is {1}'.format(
            state.to_move, move))

        # count my pieces
        my_pieces = len(self.get_pos(state, predict=True))

        # count my available moves
        my_moves = len(self.actions(state))

        # count my gains
        my_gains = 3 * len(self.change_board(state, move, predict=True))
        
        # count my dangerous places
        # This should be seen as look for black checkers
        # look for valid spots as white

        opp_pos = self.get_pos(state)
        print("Opp_pos is", opp_pos)
        opp_empties = self.check_empty_neigh(self.get_pos(state, predict=True))
        print("Opp_empties is", opp_empties)
        opp_acts = self.validate_moves(opp_empties, predict=True)
        print("Opp_acts are", opp_acts)
        changed_mines = []
        best_opp_move = 0
        for each_act in opp_acts:
            mypossiblechanged = len(self.change_board(state, each_act, predict=True, obj='mine'))
            print("My possible changed is now", mypossiblechanged)
            changed_mines.append(mypossiblechanged)
            if mypossiblechanged > best_opp_move:
                best_opp_move = mypossiblechanged
            print("Best opp is", best_opp_move)
            print("Changed mines are", changed_mines)
        best_index = changed_mines.index(max(changed_mines))
        opp_gains = len(self.change_board(state, opp_acts[best_index], predict=True, obj='mine'))

        # This is the actual heuristic function
        return my_pieces + my_moves + my_gains - (len(opp_acts) * opp_gains) / 2

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

# Instantiation
othello = Othello7()
# Testing of alphabeta_search. It works!
alphabeta_search(othello.initial, othello)