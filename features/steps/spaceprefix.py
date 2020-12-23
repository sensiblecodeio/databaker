import json
import os

from behave import *
from pathlib import Path

from databaker.framework import loadxlstabs
from databaker.overrides import excel_ref
from databaker.overrides import spaceprefix

def get_fixture(file_name):
    """Helper to get specific files out of the fixtures dir"""
    feature_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
    fixture_file_path = Path(feature_path, "fixtures", file_name)
    return fixture_file_path

@given(u'we define a bag as every value in column "{col}".')
def step_impl(context, col):
    #raise NotImplementedError(u'STEP: Given we define a bag as every value in column "B".')
    context.tab = context.tabs[2]
    context.income_column = context.tab.excel_ref(col).is_not_blank()

@given(u'we define income type as each cell which begins with "{ws_chars}" whitespace characters.')
def step_impl(context, ws_chars):
    #raise NotImplementedError(u'STEP: Given we define income type as each cell which begins with "5" whitespace characters.')
    context.income_type = context.income_column.spaceprefix(int(ws_chars))

@then(u'we confirm income type contains the correct number of values: "{inc_typ_len}"')
def step_impl(context, inc_typ_len):
    #raise NotImplementedError(u'STEP: Then we confirm income type contains the correct number of values: "20"')
    assert len(context.income_type) == int(inc_typ_len), "{} \n\nbag contains unexpected number of cells \n\n {}\n".format(str(actual), str(expected))

    #if len(context.income_type) == int(inc_typ_len):
    #    step = "Success"
    #else:
    #    raise NotImplementedError(u'STEP: Then we confirm year contains no blank cells.')    


@then(u'we confirm that income type is equal to')
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
    for cell in context.income_type:
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