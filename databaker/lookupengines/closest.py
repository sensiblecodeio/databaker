from databaker.constants import ABOVE, BELOW, LEFT, RIGHT

class ClosestEngine(object):

    def __init__(self, cell_bag, direction):
        """
        Creates a lookup engine for dimensions defined with the
        CLOSEST, ABOVE relationship.

        Creates a dictionary of ranges, where the key i is an incrementing counter serving
        as the index. The ranges defined against each index are ordered by their low/high
        offsets.

        So min(i)["lowest_offset"] will be the absolute lowest y offset being considered.
        And max(i)["highest_offset"] will be the absolute highest y offset being considered.
        The others will run the gamut between (in order).

        example_range_dict = {i:
                            {
                            "highest_offset": <the highest y index value for cells in range>,
                            "lowest_offset": <the lowest y index value for cells in range>,
                            "dimension_cell": <the _XYCell to return>
                            }
                        }

        example_ranges = {
            0: {'highest_offset': 175, 'lowest_offset': 5, 'dimension_cell': 'foo_XYCell'},
            1: {'highest_offset': 799, 'lowest_offset': 176, 'dimension_cell': 'bar_XYCell'},
            2: {'highest_offset': 9942, 'lowest_offset': 800, 'dimension_cell': 'baz_XYCell'}
            }

        The lookup itself will search the range_dicts to find the
        appropriate range_dict (and the _XYCell representing a dimension
        item) based on the .y value of a given observation cell.
        """

        self.labelise = {
                (0, -1): "ABOVE",
                (1, 0): "RIGHT",
                (0, 1): "BELOW",
                (-1, 0): "LEFT"
             }

        self.direction = direction

        break_points = {}
        for cell in cell_bag:

            # TODO - we should utilise the existing databaker error for this
            if cell.value in break_points.keys():
                raise Exception("Aborting. You have defined two or more equally valid CLOSESTrelationships")

            if direction in [ABOVE, BELOW]:
                break_points.update({cell.y: cell})
            else:
                break_points.update({cell.x: cell})

        ordered_break_point_list = [int(k) for k in break_points.keys()]
        ordered_break_point_list.sort()

        max_offset = max(ordered_break_point_list)

        ranges = {}

        if direction in [ABOVE, LEFT]:
            x = 0
            for i in range(0, len(ordered_break_point_list)-1):
                ranges.update({x:
                    {"lowest_offset": ordered_break_point_list.copy()[i],
                    "highest_offset": ordered_break_point_list.copy()[i+1]-1,
                    "dimension_cell": break_points[ordered_break_point_list.copy()[i]]}
                    })
                x+=1
                ranges.update({x:
                                {"lowest_offset": ordered_break_point_list.copy()[-1],
                                "highest_offset": 99999999999,
                                "dimension_cell": break_points[ordered_break_point_list.copy()[-1]]}
                            })
        else:
            x = 0
            ranges.update({0:
                            {"lowest_offset": 0,
                            "highest_offset": ordered_break_point_list.copy()[0],
                            "dimension_cell": break_points[ordered_break_point_list.copy()[0]]}
                        })
            x = 1
            for i in range(1, len(ordered_break_point_list)):
                h = ordered_break_point_list.copy()[i]
                ranges.update({x:
                    {"lowest_offset": ordered_break_point_list.copy()[i-1]+1,
                    "highest_offset": h if h != max_offset else 99999999999,
                    "dimension_cell": break_points[ordered_break_point_list.copy()[i]]}
                    })
                x+=1           

        import pprint
        print(self.labelise[direction], pprint.pformat(ranges))

        self.ranges = ranges
        self.range_count = len(ranges)   # do this here, so we only do it once
        self.start_index = int(len(ranges)/2)

        # this is explained in self.lookup()
        self.bumped = True

        # track the correct one
        self.found_cell = None

    # recursive bi-section search of ranges
    def lookup(self, cell, index=None):

        found_it = False

        if index == None:
            index = self.start_index

        #print("index", index, "cell", cell)

        r = self.ranges[index]

        if self.direction == ABOVE:
            if cell.y < r["lowest_offset"]:
                if self.bumped == False and index != 0:
                        index = index-1
                        self.bumped = True
                else:
                    index = int(index /2)
                    if index < 0 : index = 0
                self.found_cell = self.lookup(cell, index=index)
            elif cell.y > r["highest_offset"]:
                if self.bumped == False and index != self.range_count:
                        index = index+1
                        self.bumped = True
                else:
                    index = int(index*2)
                    if index > self.range_count: index = self.range_count
                self.found_cell = self.lookup(cell, index=index)
            else:
                found_it = True

        if self.direction == BELOW:
            if cell.y > r["highest_offset"]:
                if self.bumped == False and index != self.range_count:
                        index = index+1
                        self.bumped = True
                else:
                    index = int(index*2)
                    if index > self.range_count: index = self.range_count
                self.found_cell = self.lookup(cell, index=index)
            elif cell.y < r["lowest_offset"]:
                if self.bumped == False and index != 0:
                        index = index-1
                        self.bumped = True
                else:
                    index = int(index /2)
                    if index < 0 : index = 0
                self.found_cell = self.lookup(cell, index=index)
            else:
                found_it = True

        if self.direction == LEFT:
            if cell.x < r["lowest_offset"]:
                if self.bumped == False and index != 0:
                        index = index-1
                        self.bumped = True
                else:
                    index = int(index /2)
                    if index < 0 : index = 0
                self.found_cell = self.lookup(cell, index=index)
            elif cell.x > r["highest_offset"]:
                if self.bumped == False and index != self.range_count:
                        index = index+1
                        self.bumped = True
                else:
                    index = int(index*2)
                    if index > self.range_count: index = self.range_count
                self.found_cell = self.lookup(cell, index=index)
            else:
                found_it = True

        if self.direction == RIGHT:
            if cell.x > r["highest_offset"]:
                if self.bumped == False and index != self.range_count:
                        index = index+1
                        self.bumped = True
                else:
                    index = int(index*2)
                    if index > self.range_count: index = self.range_count
                self.found_cell = self.lookup(cell, index=index)
            elif cell.x < r["lowest_offset"]:
                if self.bumped == False and index != 0:
                        index = index-1
                        self.bumped = True
                else:
                    index = int(index /2)
                    if index < 0 : index = 0
                self.found_cell = self.lookup(cell, index=index)
            else:
                found_it = True

        if found_it:
            # Found it !!

            # cells are implicitly selected right->down-a-row->right as you look at a spreadsheet
            # so we'll cache this index as there's a decent chance the next obs lookup is in the same range
            self.start_index = index

            # this right-then-down-then-right pattern also means that (often, not guaranteed),
            # if the next obs isn't in the last range checked, there's a decent chance it's in a
            # neighbouring range, so we'll "bump" the index once in the relevant direction on a
            # first miss.
            self.bumped = False

            self.found_cell = r["dimension_cell"]

        if self.found_cell is None:
            # If we fall through to here the lookup failed
            raise Exception("'CLOSEST' engine failed. Cannot find '{}' lookup for cell {}."
                            .format(self.labelise[self.direction], cell))

        return self.found_cell