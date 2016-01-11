
# Start = list of standard headers. 
start = "observation,data_marking,statistical_unit_eng,statistical_unit_cym,measure_type_eng,measure_type_cym,observation_type,empty,obs_type_value,unit_multiplier,unit_of_measure_eng,unit_of_measure_cym,confidentuality,empty1,geographic_area,empty2,empty3,time_dim_item_id,time_dim_item_label_eng,time_dim_item_label_cym,time_type,empty4,statistical_population_id,statistical_population_label_eng,statistical_population_label_cym,cdid,cdiddescrip,empty5,empty6,empty7,empty8,empty9,empty10,empty11,empty12"

OBS = -9
DATAMARKER = -8
STATUNIT = -7
MEASURETYPE = -6
UNITMULTIPLIER = -5
UNITOFMEASURE = -4
GEOG = -3
TIME = -2
TIMEUNIT = -1
STATPOP = 0

SKIP_AFTER = {OBS: 0,            # 1..2
              DATAMARKER: 0,     # 2..3
              STATUNIT: 1,       # 3..5
              MEASURETYPE: 4,    # 5..10
              UNITMULTIPLIER: 0, # 10..11
              UNITOFMEASURE: 3,  # 11..15
              GEOG: 2,           # 15..18/19
              TIME: 1,           # 18/19..21
              TIMEUNIT: 1,       # 21..23/24
              STATPOP:11}        # 23/24..36/37
LAST_METADATA = STATPOP


# Repeat - list of headers to be repeated for each topic dimension
repeat = "dim_id_{num},dimension_label_eng_{num},dimension_label_cym_{num},dim_item_id_{num},dimension_item_label_eng_{num},dimension_item_label_cym_{num},is_total_{num},is_sub_total_{num}"

# Match up the captured name and dimension value with the repeat shown above
def get_topic_headers(name, value):  # DONT alter this line
    return (name, name, '', value, value, '', '', '')   # Change this line
    

