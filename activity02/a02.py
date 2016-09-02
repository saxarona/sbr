# Activity02

from lib import *   # This is the redblob games lib for hexagons!
from collections import OrderedDict

# We need to define a "map" where to store the hexagons
# We use a class named Hex, which is a namedtuple
# that is imported (from collections.py).
# Hex objects need 3 parameters: their q, r and s coordinates
# which are relative to their x, y, z coordinates.

grid = OrderedDict()  # This is the grid dictionary (hash table)

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

print(hex_distance(grid['C1'], grid['C5']))