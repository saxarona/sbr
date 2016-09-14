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

The initial state can be a simple string, like 'A'.
"""

from games import *


class Othello7(Game):
    """
    This class extends Game class from games module.
    All method definitions need to be implemented here.
    """

    def __init__(self):
        self.initial = ()
        self.actions = []

    def actions(self, state):
        """Returns a list of the allowed moves at this point."""

        acts = []  # meanwhile

        return acts

    def result(self, state, move):
        """Returns the state resulting from making a move in state."""

        next_state = state  # meanwhile

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
        print(state)

    def __repr__(self):
        return '<%s>' % self.__class__.__name__
