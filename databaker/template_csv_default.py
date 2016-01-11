
start = "observation,data_marking,statistical_unit_eng,statistical_unit_cym,measure_type_eng,measure_type_cym,observation_type,empty,obs_type_value,unit_multiplier,unit_of_measure_eng,unit_of_measure_cym,confidentuality,empty1,geographic_area,empty2,empty3,time_dim_item_id,time_dim_item_label_eng,time_dim_item_label_cym,time_type,empty4,statistical_population_id,statistical_population_label_eng,statistical_population_label_cym,cdid,cdiddescrip,empty5,empty6,empty7,empty8,empty9,empty10,empty11,empty12"
repeat = "dim_id_{num},dimension_label_eng_{num},dimension_label_cym_{num},dim_item_id_{num},dimension_item_label_eng_{num},dimension_item_label_cym_{num},is_total_{num},is_sub_total_{num}"

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

"https://github.com/python-excel/xlwt/blob/master/xlwt/Style.py#L307"




"""
# Replaces skipafter dictionary from bake.py with tuple of tuples in structure csv template. Updated bake.py
# code to use lengthg and order of tuples to determine processing order of dimensions 


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