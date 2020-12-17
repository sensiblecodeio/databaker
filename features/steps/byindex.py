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

@given(u'we define a bag as every value in row "{row_num}".')
def step_impl(context, row_num):
    #raise NotImplementedError(u'STEP: Given we define a bag as every value in row "5".')
    context.tab = context.tabs[4]
    context.index_unit_row = context.tab.excel_ref("A"+row_num+":Z"+row_num)

@given(u'we define by index unit as the value at index "{index}" in this bag.')
def step_impl(context, index):
    #raise NotImplementedError(u'STEP: Given we define by index unit as the value at index "15" in this bag.')
    context.index_unit = context.index_unit_row.by_index(int(index))


@then(u'we confirm by index unit is defined as type cell, equal to')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Then we confirm by index unit is defined as type cell, equal to')
    expected = context.text
    actual = str(type(context.index_unit))
    if expected == actual:
        step = "Success"
    else:
        raise NotImplementedError(u'STEP: Then we confirm unit is defined as type cell, equal to')


@then(u'we confirm that by index unit is equal to')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Then we confirm that by index unit is equal to')
    expected = str(context.text).strip()
    actual = str(context.index_unit).strip()

    if expected == actual:
        step = "Success"
    else:
        raise NotImplementedError(u'STEP: Then we confirm unit is defined as type cell, equal to')