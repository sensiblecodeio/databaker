import json
import pprint as pp

from databaker.constants import ABOVE, BELOW, LEFT, RIGHT, DIRECTION_DICT

class DirectlyEngine(object):

    def __init__(self, cell_bag, DIRECTION, label):
        """
        We're going to write the cell_bag into a tiered dictionary (you
        could use a flat dictionary, but this'll be quicker).

        The tiers will be grouped around base 10 indexes, so to get the
        dimension_cell for (for example) y position 123456 we store the
        cells at tiered_dict[1][2][3][4][5][6]["get"].

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
        self.direction = DIRECTION
        self.label = label

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

            for numString in [char for char in string_i]:

                if numString in dict_pointer.keys():
                    pass # life is good
                else:
                    dict_pointer.update({numString:{}})

                dict_pointer = dict_pointer[numString]
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
                        return self.last_cell_found

        # It's not neat but output the engine contents before the message (in case there's thousands
        # of entries which buries the message)
        raise ValueError("\n{}\nLookup Engine Failure for direction: {} and cell {} with xy {}.\n" 
                        .format(pp.pformat(self.tiered_dict), DIRECTION_DICT[self.direction], 
                        cell, {cell.x, cell.y}))