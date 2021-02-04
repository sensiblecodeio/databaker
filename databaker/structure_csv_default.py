"""
Template/Options file for altering the structure of the .csv flatfile output.

"""

import collections
headermeasurements = [
    ('observation',            "OBS"), 
    ('data_marking',           "DATAMARKER"), 
    ('statistical_unit_eng',   "STATUNIT"),      'statistical_unit_cym', 
    ('measure_type_eng',       "MEASURETYPE"),   'measure_type_cym', 'observation_type', 'empty', 'obs_type_value', 
    ('unit_multiplier',        "UNITMULTIPLIER"),
    ('unit_of_measure_eng',    "UNITOFMEASURE"), 'unit_of_measure_cym', 'confidentuality', 'empty1', 
    ('geographic_area',        "GEOG"),          'empty2', 'empty3', 
    ('time_dim_item_id',       "TIME"),               
    ('time_dim_item_label_eng',"TIME"),          'time_dim_item_label_cym', 
    ('time_type',              "TIMEUNIT"),      'empty4', 
    ('statistical_population_id',       "STATPOP"),
    ('statistical_population_label_eng',"STATPOP"), 'statistical_population_label_cym', 
    ('cdid', "CDID"), 'cdiddescrip', 'empty5', 'empty6', 'empty7', 'empty8', 'empty9', 'empty10', 'empty11', 'empty12'
]

headeradditionals = [ 
    ("dim_id",      "NAME"),  ("dimension_label_eng",      "NAME"),  "dimension_label_cym",
    ("dim_item_id", "VALUE"), ("dimension_item_label_eng", "VALUE"), "dimension_item_label_cym",  
    "is_total", "is_sub_total"
]

conversionsegmentnumbercolumn = "empty11"

# Do you want to split the OBS, placing non float data into your next column.
SH_Split_OBS = "DATAMARKER"  # see value set to int value below


####  Below this point is derived data (used in old code) from the above tables

# derive the elements of the headernames above into the values below 
headermeasurementnames = list(collections.OrderedDict.fromkeys(k[1]  for k in headermeasurements  if isinstance(k, tuple)))
headermeasurementnamesSet = set(headermeasurementnames) 

# Create variables (This is terrible!)
# TODO: Do this more cleanly e.g. as in https://stackoverflow.com/q/4859217/
exec("%s = '%s'" % (", ".join(headermeasurementnames), "', '".join(map(str, headermeasurementnames))))
exec("SH_Split_OBS = %s" % SH_Split_OBS)

__all__ = list(headermeasurementnames) # don't expose unnecessary items when using `from foo import *`



