from xypath import DOWN, UP, LEFT, RIGHT
import bake
from hamcrest import *
import csv

# IF theres a custom template use it, Otherwise use the default.
try:
    from structure_csv_user import *
except:
    from structure_csv_default import *


ABOVE = UP
BELOW = DOWN

DIRECTLY = True
CLOSEST = False

class NotEnoughParams(Exception):
    pass

def PARAMS(position=None):
    if position is None:
        return bake.Opt.params
    else:
        try:
            return bake.Opt.params[position]
        except IndexError:
            raise NotEnoughParams("Unable to find PARAM({!r}). Only {!r} parameters were passed on the command line: {!r}".format(position, len(bake.Opt.params), bake.Opt.params))


# Funtion to dynamically assign colours to dimensions for preview
def create_colourlist():
    colours = ["lavender", "violet", "gray25", "sea_green",
              "pale_blue", "blue", "gray25", "rose", "tan", "light_yellow", "light_green", "light_turquoise",
              "light_blue", "sky_blue", "plum", "gold", "lime", "coral", "periwinkle", "ice_blue", "aqua"]
    numbers = []
    for i in range(len(SKIP_AFTER)-1, -(len(colours) - len(SKIP_AFTER)), -1):
            numbers.append(-i)
    colourlist = dict(zip(numbers, colours))
    return colourlist
    
   
    
def rewrite_headers(filename):
    with open(filename, 'rb') as fr:
        myreader = csv.reader(fr, delimiter=',')
        for row in myreader:
            dims = dimlist[0: (len(row) - len(start.split(',')) / len(value_spread))]
            for i in range(0,len(row)):
                if i >= len(start.split(',')):
                    which_cell_in_spread = (i - len(start.split(','))) % len(value_spread)
                    which_dim = (i - len(start.split(','))) / len(value_spread)
                    which_dim = int(which_dim)
                    if value_spread[which_cell_in_spread] == 'value':
                        row[i] = dims[which_dim] 
            fr.close()
            return row   # Return as a string to match other inputs for csvwriter


    
def write_headers(filename):
    if not topic_headers_as_dims:     # If the user hasnt indicated they want dimensions as dimension item headers return
        return
    header_list = []
    # Read all data from the csv file.
    with open(filename, 'rb') as b:
        headers = csv.reader(b)
        header_list.extend(headers)
    
    # data to override in the format {line_num_to_override:data_to_write}. 
    line_to_override = {0:rewrite_headers(filename)}
    
    # Write data to the csv file and replace the lines in the line_to_override dict.
    with open(filename, 'wb') as b:
        writer = csv.writer(b)
        for line, row in enumerate(header_list):
             data = line_to_override.get(line, row)
             writer.writerow(data)    
