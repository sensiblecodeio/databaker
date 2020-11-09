import json
import os

from behave import given, when, then
from pathlib import Path

from databaker import loadxlstabs

def get_fixture(file_name):
    """Helper to get specific files out of the fixtures dir"""
    feature_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
    fixture_file_path = Path(feature_path, "fixtures", file_name)
    return fixture_file_path

@given('we load an an xls file named "{xls_file}"')
def step_impl(context, xls_file):
    path_to_xls = get_fixture(xls_file)
    context.tabs = loadxlstabs(path_to_xls)

@given('we confirm the names of the loaded tabs are equal to:')
def step_impl(context, xls_file):
    tabs_wanted = json.loads(context.text)
    for tab in tabs_wanted:
        assert tab in [x.name for x in context.tabs]
    assert len(context.tabs) == len(tabs_wanted)
