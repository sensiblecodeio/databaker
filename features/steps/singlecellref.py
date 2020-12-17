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

@given(u'we define unit as the value in cell "{cell_ref}"')
def step_impl(context, cell_ref):
    #raise NotImplementedError(u'STEP: Given we define unit as the value in a cell')
    context.tab = context.tabs[4]
    context.unit = context.tab.excel_ref(cell_ref)


@then(u'we confirm unit is defined as type cell, equal to')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Then we confirm unit is defined as type cell, equal to')
    expected = context.text
    actual = str(type(context.unit))
    if expected == actual:
        step = "Success"
    else:
        raise NotImplementedError(u'STEP: Then we confirm unit is defined as type cell, equal to')

@then(u'we confirm that unit is equal to')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Then we confirm unit is defined as type cell, equal to')
    expected = str(context.text).strip()
    actual = str(context.unit).strip()

    if expected == actual:
        step = "Success"
    else:
        raise NotImplementedError(u'STEP: Then we confirm unit is defined as type cell, equal to')
