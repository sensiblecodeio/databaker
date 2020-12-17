import json
import os

from behave import *
from pathlib import Path

from databaker.framework import loadxlstabs
from databaker.overrides import excel_ref
from databaker.overrides import one_of
#from databaker.constants import *

def get_fixture(file_name):
    """Helper to get specific files out of the fixtures dir"""
    feature_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
    fixture_file_path = Path(feature_path, "fixtures", file_name)
    return fixture_file_path

@given(u'we define all years as every value in from column "{all_years}" down')
def step_impl(context, all_years):
    #raise NotImplementedError(u'STEP: Given we define all years as every value in from column "A" down')
    context.tab = context.tabs[4]
    context.all_years = context.tab.excel_ref(all_years).is_not_blank()


@given(u'we define the last 5 years as every value in all years and in the list: "{last_5_list}"')
def step_impl(context, last_5_list):
    #raise NotImplementedError(u'STEP: Given we define the last 5 years as every value in all years and in the list: "2015.0,2016.0,2017.0,2018.0,2019.0"')
    s = last_5_list.split(",")
    context.last_5_years = context.all_years.one_of(s)

@then(u'we confirm last 5 years contains the correct number of values: "{last_5_len}"')
def step_impl(context, last_5_len):
    #raise NotImplementedError(u'STEP: Then we confirm last 5 years contains the correct number of values: "15"')
    if len(context.last_5_years) == int(last_5_len):
        step = "Success"
    else:
        raise NotImplementedError(u'STEP: Then we confirm year contains no blank cells.')

@then(u'we confirm that the last 5 years is equal to')
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
    for cell in context.last_5_years:
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
