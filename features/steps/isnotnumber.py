import json
import os

from behave import *
from pathlib import Path

from databaker.framework import loadxlstabs
from databaker.overrides import excel_ref
from databaker.overrides import is_not_number

def get_fixture(file_name):
    """Helper to get specific files out of the fixtures dir"""
    feature_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
    fixture_file_path = Path(feature_path, "fixtures", file_name)
    return fixture_file_path

@given(u'we define the string observations as all values between cell refs "{obs_start}" and "{obs_end}" excluding the GBP values.')
def step_impl(context, obs_start, obs_end):
    #raise NotImplementedError(u'STEP: Given we define the string observations as all values between cell refs "C8" and "K57" excluding the GBP values.')
    context.tab = context.tabs[1]
    context.percent_obs = context.tab.excel_ref(obs_start+":"+obs_end).is_not_number().is_not_blank()


@then(u'we confirm the string observations contains the correct number of values: "{percent_len}"')
def step_impl(context, percent_len):
    #raise NotImplementedError(u'STEP: Then we confirm the string observations contains the correct number of values: "48"')
    if len(context.percent_obs) == int(percent_len):
        step = "Success"
    else:
        raise NotImplementedError(u'STEP: Then we confirm year contains no blank cells.')


@then(u'we confirm that the string observations are equal to')
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
    for cell in context.percent_obs:
        temp_actual.append(str(cell))

    #Use that list to make a new set in the same string format as the output expects.
    #No "{, }"
    for cell in temp_actual:
        new_cell = cell.replace("{", "")
        new_cell = new_cell.replace("}", "")
        actual.add(new_cell)

    #If set difference produces an empty set, then both sets contain the same items regardless of order.
    if len(expected.difference(actual)) == 0:
        step = "Success"
    
    else:
        raise NotImplementedError(u'STEP: Then we confirm that year is equal to')