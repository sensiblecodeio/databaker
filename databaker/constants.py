from xypath import DOWN, UP, LEFT, RIGHT
import bake
from template_csv_default import *        # Import tempalte so constants are availible to recipe
from hamcrest import *
import csv

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
    
   
# Returns a list of headers, for use by the write_headers function 
def rewrite_headers(dims, filename):
    with open(filename, 'rb') as fr:
        myreader = csv.reader(fr, delimiter=',')
        start_len = len(start.split(','))
        repeat_len = len(repeat.split(','))
        for row in myreader:
            allcells = row
            for i in range(0,start_len-1):
                if i >= start_len:
                    which_cell_in_spread = (i - start_len) % repeat_len
                    which_dim = (i - start_len) / repeat_len
                    which_dim = int(which_dim) + 1
                    if value_spread[which_cell_in_spread] == 'value':
                        allcells[i] = dims[which_dim-1] 
            fr.close()
            return allcells   


# Funtion to rewrite topic headers as dimensions if needed   
def write_headers(dims, filename):
    if not topic_headers_as_dims:     # If the user hasnt indicated they want dimensions as dimension item headers return
        return
    header_list = []
    # Read all data from the csv file.
    with open(filename, 'rb') as b:
        headers = csv.reader(b)
        header_list.extend(headers)
    
    # data to override in the format {line_num_to_override:data_to_write}. 
    line_to_override = {0:rewrite_headers(dims, filename) }
    
    # Write data to the csv file and replace the lines in the line_to_override dict.
    with open(filename, 'wb') as b:
        writer = csv.writer(b)
        for line, row in enumerate(header_list):
             data = line_to_override.get(line, row)
             writer.writerow(data)    
