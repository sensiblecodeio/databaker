class DirectlyLeftEngine(object):

    def __init__(self, cell_bag):
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

        self.tiered_dict = {}

        for cell in cell_bag:

            ## reset dictionary to starting point
            dict_pointer = self.tiered_dict

            # Stringify in case it's needed
            string_y = str(cell.y)

            viewed_layer = 0
            for numString in [char for char in string_y]:

                    if numString in dict_pointer.keys():
                        pass # life is good
                    else:
                        dict_pointer.update({numString:{}})

                    dict_pointer = dict_pointer[numString]
                    viewed_layer += 1

                    if viewed_layer == len(string_y):

                        if "get" in dict_pointer.keys():
                            dict_pointer["get"].append(cell)
                        else:
                            dict_pointer.update({"get": [cell]})
                        break

    def lookup(self, cell):

        string_y = str(cell.y)

        dict_pointer = self.tiered_dict
        viewed_layer = 0

        for numString in [char for char in string_y]:

                if numString in dict_pointer.keys():
                    dict_pointer = dict_pointer[numString]
                else:
                    if viewed_layer+1 != len(string_y):
                        raise ValueError("Lookup Failure 1")

                viewed_layer += 1

                if viewed_layer == len(string_y):

                    found_cells = dict_pointer["get"]

                    self.last_cell_found = None

                    for found_cell in found_cells:

                        # Left
                        if found_cell.y == cell.y and found_cell.x < cell.x :

                            if self.last_cell_found != None:
                                if found_cell.x > self.last_cell_found.x:
                                    self.last_cell_found = found_cell
                            else:
                                self.last_cell_found = found_cell

                    if self.last_cell_found != None:
                        return self.last_cell_found
                    else:
                        raise ValueError("Lookup Failure 2")