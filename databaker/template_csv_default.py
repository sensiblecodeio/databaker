
start = "observation,data_marking,statistical_unit_eng,statistical_unit_cym,measure_type_eng,measure_type_cym,observation_type,empty,obs_type_value,unit_multiplier,unit_of_measure_eng,unit_of_measure_cym,confidentuality,empty1,geographic_area,empty2,empty3,time_dim_item_id,time_dim_item_label_eng,time_dim_item_label_cym,time_type,empty4,statistical_population_id,statistical_population_label_eng,statistical_population_label_cym,cdid,cdiddescrip,empty5,empty6,empty7,empty8,empty9,empty10,empty11,empty12"
repeat = "dim_id_{num},dimension_label_eng_{num},dimension_label_cym_{num},dim_item_id_{num},dimension_item_label_eng_{num},dimension_item_label_cym_{num},is_total_{num},is_sub_total_{num}"

# TODO - Bake 148 - repeat cal3led!



"""

# Standard Structure of the Output CSV  
Dim_Structure = (
                ('OBS', 0), 
                ('DATAMARKER', 0),
                ('STATUNIT', 1),
                ('MEASURETYPE', 4),
                ('UNITMULTIPLIER', 0),
                ('UNITOFMEASURE', 3),
                ('GEOG', 2),
                ('TIME', 0),
                ('TIME', 1),
                ('TIMEUNIT', 1),
                ('STATPOP', 0),
                ('STATPOP', 11),
)




# Structure of each Topic dimensions
def get_topic_headers(name, value):  # DONT alter this line
    return (name, name, '', value, value, '', '', '')


# -------- Funtions cor building the Structure

# Create List of Headers in the STandard part of the output CSV
def standard_headers():
    standard_headers = []
    for i in range(len(Dim_Structure)-1, 0, -1):
        standard_headers.append(Dim_Structure[i][0])
    return standard_headers

"""