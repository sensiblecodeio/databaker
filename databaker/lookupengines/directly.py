import json
import pprint as pp

from databaker.constants import ABOVE, BELOW, LEFT, RIGHT, DIRECTION_DICT

class DirectLookupException(Exception):
    """Raised when a DIRECT lookup fails"""

    def __init__(self, message):
        self.message = message

class DirectlyEngine(object):

    def __init__(self, cell_bag, direction, label, cellvalueoverride):
        """
        We're going to write the cell_bag into a tiered dictionary (you
        could use a flat dictionary, but this'll be quicker).

        The tiers will be grouped around base 10 indexes, so to store the
        dimension_cell for (for example) y position 123456 we store the
        cells at tiered_dict[1][2][3][4][5][6]["get"].

        As our starting point is a cell that knows it's own x or y offset,
        this'll let us jump straight to the relevant row/column cells when
        we do the lookup.

        The ["get"] key is included in each level to differentiate from
        the integer keys for further out children.

        i.e you'll have dicts of = {
            "0": { go deeper }
            "1": { go deeper }
            "get": [list of dimension cells on this axis]
        }

        This makes lookups explicit where you want to (for example) get the
        dimension cell for .y position 10, when you also have a dimension
        cell for 100, 10000 and 100000.
        """
        self.direction = direction
        self.label = label
        self.cellvalueoverride = cellvalueoverride if cellvalueoverride is not None else {}

        self.tiered_dict = {}

        for cell in cell_bag:

            ## reset dictionary to starting point
            dict_pointer = self.tiered_dict

            # Stringify relevent index
            if self.direction == ABOVE or self.direction == BELOW:
                string_i = str(cell.x)
            else:
                string_i = str(cell.y)

            viewed_layer = 0

            for num_string in [char for char in string_i]:

                if num_string in dict_pointer.keys():
                    pass # we have the key we need already
                else:
                    dict_pointer.update({num_string:{}})

                dict_pointer = dict_pointer[num_string]
                viewed_layer += 1

                if viewed_layer == len(string_i):

                    if "get" in dict_pointer.keys():
                        dict_pointer["get"].append(cell)
                    else:
                        dict_pointer.update({"get": [cell]})
                    break

    def lookup(self, cell):

        if self.direction == ABOVE or self.direction == BELOW:
            string_i = str(cell.x)
        else:
            string_i = str(cell.y)

        dict_pointer = self.tiered_dict
        viewed_layer = 0

        for numString in [char for char in string_i]:

                if numString in dict_pointer.keys():
                    dict_pointer = dict_pointer[numString]
                else:
                    if viewed_layer+1 != len(string_i):
                        raise ValueError("Aborting, surpassed lookup depth. Target {}"
                                        ". x:{}, y:{}".format(cell, cell.x, cell.y))

                viewed_layer += 1
                if viewed_layer == len(string_i) and "get" in dict_pointer.keys():

                    found_cells = dict_pointer["get"]
                    
                    self.last_cell_found = None

                    for found_cell in found_cells:

                        if self.direction == LEFT:
                            if found_cell.y == cell.y and found_cell.x < cell.x :
                                if self.last_cell_found != None:
                                    if found_cell.x > self.last_cell_found.x:
                                        self.last_cell_found = found_cell
                                else:
                                    self.last_cell_found = found_cell

                        elif self.direction == RIGHT:
                            if found_cell.y == cell.y and found_cell.x > cell.x :
                                if self.last_cell_found != None:
                                    if found_cell.x < self.last_cell_found.x:
                                        self.last_cell_found = found_cell
                                else:
                                    self.last_cell_found = found_cell

                        elif self.direction == ABOVE:
                            if found_cell.x == cell.x and found_cell.y < cell.y :
                                if self.last_cell_found != None:
                                    if found_cell.y < self.last_cell_found.y:
                                        self.last_cell_found = found_cell
                                else:
                                    self.last_cell_found = found_cell

                        elif self.direction == BELOW:
                            if found_cell.x == cell.x and found_cell.y > cell.y :
                                if self.last_cell_found != None:
                                    if found_cell.y > self.last_cell_found.y:
                                        self.last_cell_found = found_cell
                                else:
                                    self.last_cell_found = found_cell

                        else:
                            raise Exception("Direction must be one of LEFT, RIGHT, ABOVE, BELOW. Have {}"
                                            " x:{}, y{}.".format(self.direction,cell.x, cell.y))

                    if self.last_cell_found is not None:

                        # Apply str level cell value override if applicable
                        if self.last_cell_found.value in self.cellvalueoverride.keys():
                            value = self.cellvalueoverride[self.last_cell_found.value]
                        else:
                            value = self.last_cell_found.value

                        return self.last_cell_found, value

        # If we fall through to here the lookup has failed, raise an exception
        axis = "veritical" if DIRECTION_DICT[self.direction] in  ["ABOVE", "BELOW"] else "horizontal"
        
        # Sanitise the english
        of = "of " if axis == "horizontal" else ""

        message = f'DIRECT lookup for cell {cell} failed. The dimension "{self.label}" has no cells' \
                + f' directly {DIRECTION_DICT[self.direction]} {of}{cell} on the {axis} axis.'

        raise DirectLookupException(message)
