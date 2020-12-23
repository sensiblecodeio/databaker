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

#From the tab we capture the bag of cells containing the year values described by a range of cells in one column.
@given(u'we define year as the values in cells "{cell_range}"')
def step_impl(context, cell_range):
    #raise NotImplementedError(u'STEP: Given we define year as the values in cells "A11:A250"')
    context.tab = context.tabs[4]
    context.year = context.tab.excel_ref(cell_range)


#Check if the captured cells are the expected 'bag' type.
@then(u'we confirm year is defined as type cell, equal to')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Then we confirm year is defined as type cell, equal to')
    expected = context.text
    actual = str(type(context.year))

    assert expected == actual, "{} \n\ndoes not match the expected type \n\n {}\n".format(str(actual), str(expected))

    #if expected == actual:
    #    step = "Sucess"
    #else:
    #    raise NotImplementedError(u'STEP: Then we confirm year is defined as type cell, equal to')

#@then(u'we confirm that year is equal to')
#def step_impl(context):
#    expected = []
#    temp_actual = []
#    actual = []

    #Build a list of cell from the expected output.
    #Where each cell is the string between the two "<, >"
#    for char in range(0, len(str(context.text))):
#        cell = ""
#        if str(context.text)[char] == "<":
#            cell = cell + str(context.text)[char]
#            current = char
#            next_char = str(context.text)[current + 1]
#            while next_char != ">":
#                cell = cell + next_char
#                current += 1
#                next_char = str(context.text)[current]
#            cell = cell + ">"
#            expected.append(cell)

    #Build a list of actual values found via databaker.
#    for cell in context.year:
#        temp_actual.append(str(cell))

    #Use that list to make a new list in the same string format as the output expects.
    #No "{, }"
#    for cell in actual:
#        new_cell = cell.replace("{", "")
#        new_cell = new_cell.replace("}", "")
#        actual.append(new_cell)

    #Output == expected if all values are removed from actual list as there is a
    #directly corresponding value in the expected list.
#    for cell in actual:
#        if cell in expected:
#            actual.remove(cell)
        
#        else:
#            print("ERROR 1")
#            print("")
#            print(expected)
#            print("")
#            print(actual)
#            raise NotImplementedError(u'STEP: Then we confirm that year is equal to')

#    if len(actual) == 0:
#        step = "Success"

#    else:
#        print("ERROR 2")
#        raise NotImplementedError(u'STEP: Then we confirm that year is equal to')

#Check if the captured cells contain the correct year values.
@then(u'we confirm that year is equal to')
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
    for cell in context.year:
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