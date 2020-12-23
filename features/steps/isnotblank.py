import json
import os

from behave import *
from pathlib import Path

from databaker.framework import loadxlstabs
from databaker.overrides import excel_ref

def get_fixture(file_name):
    """Helper to get specific files out of the fixtures dir"""
    feature_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
    fixture_file_path = Path(feature_path, "fixtures", file_name)
    return fixture_file_path

@given(u'we define year as the non-blank values in cells "{cell_range}"')
def step_impl(context, cell_range):
    #raise NotImplementedError(u'STEP: Given we define year as the non-blank values in cells "A11:A250"')
    context.tab = context.tabs[4]
    context.non_blank_year = context.tab.excel_ref(cell_range).is_not_blank()

@then(u'we confirm year contains no blank cells.')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Then we confirm year contains no blank cells.')
    assert "'" not in str(context.non_blank_year), "{} \n\ncontains blank cells \n\n".format(str(context.non_blank_year))

    #if "'" not in str(context.non_blank_year):
    #    step = "Success"
    #else:
    #    raise NotImplementedError(u'STEP: Then we confirm year contains no blank cells.')    


@then(u'we confirm that year without blanks is equal to')
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
    for cell in context.non_blank_year:
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
    
    