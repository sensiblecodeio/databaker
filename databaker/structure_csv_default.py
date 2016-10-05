"""
Template/Options file for altering the structure of the .csv flatfile output.

"""
from __future__ import division
# = Standard Dimensions ========

# Start = list of standard headers.
start = "observation,data_marking,statistical_unit_eng,statistical_unit_cym,measure_type_eng,measure_type_cym,observation_type,empty,obs_type_value,unit_multiplier,unit_of_measure_eng,unit_of_measure_cym,confidentuality,empty1,geographic_area,empty2,empty3,time_dim_item_id,time_dim_item_label_eng,time_dim_item_label_cym,time_type,empty4,statistical_population_id,statistical_population_label_eng,statistical_population_label_cym,cdid,cdiddescrip,empty5,empty6,empty7,empty8,empty9,empty10,empty11,empty12"

# Dimension names (as strings!)
dimension_names = ['OBS', 'DATAMARKER', 'STATUNIT', 'MEASURETYPE', 'UNITMULTIPLIER', 'UNITOFMEASURE', 'GEOG', 'TIME', 'TIMEUNIT', 'STATPOP']

# Create variables
for i, item in enumerate(reversed(dimension_names)):
    exec(item+"=-i")

__all__ = list(dimension_names) # don't expose unnecessary items when using `from foo import *`

# Columns to skip after each dimension is output. order as above
SKIP_AFTER = {OBS: 0,            # 1..2  MANDATORY, must be here, must be called OBS
              DATAMARKER: 0,     # 2..3
              STATUNIT: 1,       # 3..5
              MEASURETYPE: 4,    # 5..10
              UNITMULTIPLIER: 0, # 10..11
              UNITOFMEASURE: 3,  # 11..15
              GEOG: 2,           # 15..18/19
              TIME: 1,           # 18/19..21
              TIMEUNIT: 1,       # 21..23/24
              STATPOP:11}        # 23/24..36/37

# = Topic Dimensions ========

# Repeat - list of headers to be repeated for each topic dimension
repeat = "dim_id_{num},dimension_label_eng_{num},dimension_label_cym_{num},dim_item_id_{num},dimension_item_label_eng_{num},dimension_item_label_cym_{num},is_total_{num},is_sub_total_{num}"


# Where in the repeat do you want to output the dimensions name and value?
def get_topic_headers(name, value):  # DONT alter this
    return ([name, name, '', value, value, '', '', ''])   # Change this line

# Where are the values? (should match the above (minus the 'name entries)
value_spread = ['', '', '', 'value', 'value', '', '', '']

# do you want to output the 'name' value in the header of the value columns?
topic_headers_as_dims = False



# ====================== S-P-E-C-I-A-L handling ========================== (..fallout much?)
# Use the following to decide which STANDARD dimensionss should get special handling

# Standard Dimensions that need to be outputted twice in a row (i.e item|label combos)
SH_Repeat = [TIME, STATPOP]

# Do we want to create a TIMEUNIT dimension using a TIME dimension - ONS specific
SH_Create_ONS_time = True

# Do you want to split the OBS, placing non float data into your next column.
SH_Split_OBS = DATAMARKER
