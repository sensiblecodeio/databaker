import json
import os

from behave import *
from pathlib import Path

from databaker.framework import loadxlstabs
from databaker.overrides import excel_ref
from databaker.overrides import rich_text

def get_fixture(file_name):
    """Helper to get specific files out of the fixtures dir"""
    feature_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
    fixture_file_path = Path(feature_path, "fixtures", file_name)
    return fixture_file_path

@given(u'we define construction type as each non-richtext and non-blank cell.')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Given we define construction type as each non-richtext and non-blank cell.')
    #EXPLAIN WHY ITS INDEX_UNIT_ROW
    context.construction_type = context.index_unit_row.is_not_richtext().is_not_blank()

@then(u'we confirm construction type contains the correct number of values: "{cons_typ_len}"')
def step_impl(context, cons_typ_len):
    #raise NotImplementedError(u'STEP: Then we confirm construction type contains the correct number of values: "7"')
    if len(context.construction_type) == int(cons_typ_len):
        step = "Success"
    else:
        raise NotImplementedError(u'STEP: Then we confirm year contains no blank cells.')

@then(u'we confirm that construction type is equal to')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Then we confirm that construction type is equal to')
    #raise NotImplementedError(u'STEP: Then we confirm that whitespace year without value-containing cels is equal to')
    #raise NotImplementedError(u'STEP: Then we confirm that year without blanks is equal to')
    expected = []
    temp_actual = []
    actual = []
   
    #Build a list of cell from the expected output.
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
                next_char = str(context.text)[current]
            cell = cell + ">"
            expected.append(cell)

    #Build a list of actual values found via databaker.
    for cell in context.construction_type:
        temp_actual.append(str(cell))

    #Use that list to make a new list in the same string format as the output expects.
    #No "{, }"
    for cell in actual:
        new_cell = cell.replace("{", "")
        new_cell = new_cell.replace("}", "")
        actual.append(new_cell)

    #Output == expected if all values are removed from actual list as there is a
    #directly corresponding value in the expected list.
    for cell in actual:
        if cell in expected:
            actual.remove(cell)
        
        else:
            raise NotImplementedError(u'STEP: Then we confirm that year is equal to')

    if len(actual) == 0:
        step = "Success"

    else:
        raise NotImplementedError(u'STEP: Then we confirm that year is equal to')


@given(u'we define construction type as each richtext and non-blank cell.')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Given we define construction type as each richtext and non-blank cell.')
    context.construction_type = context.index_unit_row.is_richtext().is_not_blank()


@then(u'we confirm construction type is equal to')
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
    for cell in context.construction_type:
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