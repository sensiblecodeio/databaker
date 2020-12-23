import json
import os

from behave import *
from pathlib import Path

from databaker.framework import loadxlstabs
from databaker.overrides import excel_ref
from databaker.overrides import is_not_whitespace

def get_fixture(file_name):
    """Helper to get specific files out of the fixtures dir"""
    feature_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
    fixture_file_path = Path(feature_path, "fixtures", file_name)
    return fixture_file_path

@given(u'we define non-whitespace year as the non-whitespace values in cells "{period_range}"')
def step_impl(context, period_range):
    #raise NotImplementedError(u'STEP: Given we define year as the non-blank values in cells "A11:A250"')
    context.tab = context.tabs[4]
    context.non_whitespace_year = context.tab.excel_ref(period_range).is_not_whitespace()


@then(u'we confirm non-whitespace year contains no whitespace cells.')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Then we confirm year contains no blank cells.')
    assert "'" not in str(context.non_whitespace_year), "{} \n\ncontains whitespace cells \n\n".format(str(context.non_whitespace_year))

    #if "'" not in str(context.non_whitespace_year):
    #    step = "Success"
    #else:
    #    raise NotImplementedError(u'STEP: Then we confirm year contains no blank cells.') 

#@then(u'we confirm non-whitespace year contains 58 cells.')
#def step_impl(context):
#    raise NotImplementedError(u'STEP: Then we confirm non-whitespace year contains 58 cells.')

@then(u'we confirm non-whitespace year contains "{non_ws_len}" cells.')
def step_impl(context, non_ws_len):
    #raise NotImplementedError(u'STEP: Then we confirm non-whitespace year contains 58 cells.')
    assert len(context.non_whitespace_year) == int(non_ws_len), "{} \n\nbag contains unexpected number of cells \n\n {}\n".format(str(context.non_whitespace_year), str(non_ws_len))

    #if len(context.non_whitespace_year) == int(non_ws_len):
    #    step = "Success"
    #else:
    #    raise NotImplementedError(u'STEP: Then we confirm year contains no blank cells.') 

@then(u'we confirm that non-whitespace year without whitespace is equal to')
def step_impl(context):
    expected = set()
    temp_actual = []
    actual = set()

    #Build a set of cells from the expected output.
    #Where each cell is the string between the two "<, >"
    for char in range(0, len(str(context.text))):
        cell = ""
        if str(context.text)[char] == "<":
            cell = cell + str(context.text)[char]
            current = char
            next_char = str(context.text)[current + 1]
            while next_char != ">":
                cell = cell + next_char
                current += 1
                next_char = str(context.text)[current + 1]
            cell = cell + ">"
            expected.add(cell)

    #Build a list of actual values found via databaker.
    for cell in context.non_whitespace_year:
        temp_actual.append(str(cell))

    #Use that list to make a new set in the same string format as the output expects.
    #No "{, }"
    for cell in temp_actual:
        new_cell = cell.replace("{", "")
        new_cell = new_cell.replace("}", "")
        actual.add(new_cell)

    #If set difference produces an empty set, then both sets contain the same items regardless of order.
    assert len(expected.difference(actual)) == 0, "{} \n\ndoes not match the expected output \n\n {}\n".format(str(actual), str(expected))

    #if len(expected.difference(actual)) == 0:
    #    step = "Success"
    
    #else:
    #    raise NotImplementedError(u'STEP: Then we confirm that year is equal to')
    
    