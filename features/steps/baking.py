import json
import os

from behave import *
from pathlib import Path
from databaker.framework import loadxlstabs
from databaker.jupybakeutils import *
from databaker.structure_csv_default import *
from databaker.constants import *


def get_fixture(file_name):
    """Helper to get specific files out of the fixtures dir"""
    feature_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
    fixture_file_path = Path(feature_path, "fixtures", file_name)
    return fixture_file_path

@given(u'we define the dimensions and observations')
def step_impl(context):
    context.tab = context.tabs[2]

    context.year = "2018"
    context.nuts1_area = context.tab.excel_ref("A4:A42").is_not_blank()
    context.industry = context.tab.excel_ref("C3:C3").is_not_blank()
    context.measure_type = context.tab.excel_ref("B4:B42").is_not_blank()
    context.unit = "£ millions"

    context.observations = context.measure_type.waffle(context.industry)

    #context.returns = [context.year, context.nuts1_area, context.industry, context.measure_type, context.unit, context.observations]


@then(u'we create a list of dimensions (HDim objects) with their relation to observations.')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Then we create a list of dimensions (HDim objects) with their relation to observations.')
    context.dimensions = [
        HDimConst("Year", context.year),
        HDim(context.nuts1_area, "NUTS1 Area", CLOSEST, ABOVE),
        HDim(context.industry, "Industry", DIRECTLY, ABOVE),
        HDim(context.measure_type, "Measure Type", DIRECTLY, LEFT),
        HDimConst("Unit", context.unit)
    ]

@then(u'we create a ConversionSegment object.')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Then we create a ConversionSegment object.')
    #import pdb; pdb.set_trace()
    #breakpoint()
    
    context.tidy_sheet = ConversionSegment(context.tab, context.dimensions, context.observations)


@then(u'we convert the ConversionSegment object into a pandas dataframe.')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Then we convert the ConversionSegment object into a pandas dataframe.')
    #import pdb
    #pdb.set_trace()
 
    context.df = context.tidy_sheet.topandas()

@then(u'we do this by defining timeunitmessage which calls the process function.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then we do this by defining timeunitmessage which calls the process function.')


@then(u'in turn this will define a list (processedrows) by looping through obslist and calling the lookupobs function.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then in turn this will define a list (processedrows) by looping through obslist and calling the lookupobs function.')


@then(u'this will call the svalue function - for each ob still.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then this will call the svalue function - for each ob still.')


@then(u'also loop for each HDim object in the dimensions list, we define hcell and val by calling the cellvalobs function - still for each ob.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then also loop for each HDim object in the dimensions list, we define hcell and val by calling the cellvalobs function - still for each ob.')


@then(u'we can define val if ob is in cellvalueoverride to return hcell as None and val as cellvalueoverride[ob]')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then we can define val if ob is in cellvalueoverride to return hcell as None and val as cellvalueoverride[ob]')


@then(u'(or) if not, we can define hcell if hbagset is not None by calling celllookup(ob) else hcell is None - still for each ob.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then (or) if not, we can define hcell if hbagset is not None by calling celllookup(ob) else hcell is None - still for each ob.')


@then(u'celllookup returns best_cell using functions of smaller scope: betweencells(), same_row_col() and mult()')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then celllookup returns best_cell using functions of smaller scope: betweencells(), same_row_col() and mult()')


@then(u'we finally return hcell and val but val is defined by calling the headcellval function using hcell')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then we finally return hcell and val but val is defined by calling the headcellval function using hcell')


@then(u'headcellval can return val as cellvalueoverride[hcell] if hcell is not None and hcell is in cellvalueoverride')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then headcellval can return val as cellvalueoverride[hcell] if hcell is not None and hcell is in cellvalueoverride')


@then(u'(or) if hcell is just not None val is assigned as using the svalue function still for each ob.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then (or) if hcell is just not None val is assigned as using the svalue function still for each ob.')


@then(u'if hcell is None then val is assigned as None too.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then if hcell is None then val is assigned as None too.')


@then(u'val can be found and returned if its in cellvalueoverride, it gets assigned as cellvalueoverride[val]')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then val can be found and returned if its in cellvalueoverride, it gets assigned as cellvalueoverride[val]')


@then(u'(or) val can be found and returned if its type is in cellvalueoverride. val gets assigned as cellvalueoverride[type(val)](val)')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then (or) val can be found and returned if its type is in cellvalueoverride. val gets assigned as cellvalueoverride[type(val)](val)')


@then(u'back in the lookupobs function, a dict can be filled with HDim labels and vals.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then back in the lookupobs function, a dict can be filled with HDim labels and vals.')


@then(u'more processing is done to this dict before returning it to processedrows list - end of looping for each ob.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then more processing is done to this dict before returning it to processedrows list - end of looping for each ob.')


@then(u'penultimately some stuff is done regarding timeunitmessage including calls to the functions: guesstimeunit() and fixfromtimeunit()')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then penultimately some stuff is done regarding timeunitmessage including calls to the functions: guesstimeunit() and fixfromtimeunit()')


@then(u'lastly the dataframe is declared and defined from the dictionaries in the processedrows list.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then lastly the dataframe is declared and defined from the dictionaries in the processedrows list.')