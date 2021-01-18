import json
import os

from behave import *
from pathlib import Path

from databaker.framework import loadxlstabs

def get_fixture(file_name):
    """Helper to get specific files out of the fixtures dir"""
    feature_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
    fixture_file_path = Path(feature_path, "fixtures", file_name)
    return fixture_file_path

@given('we load an xls file named "{xls_file}"')
def step_impl(context, xls_file):
    path_to_xls = get_fixture(xls_file)
    context.last_xls_loaded = path_to_xls
    context.tabs = loadxlstabs(path_to_xls)

@given('get "{thing_wanted}" from the transform')
def step_impl(context, thing_wanted):

    transform_code = context.text

    # Nasty, but needs must
    here = Path(os.path.dirname(os.path.abspath(__file__))).parent
    with open(Path(here / "temp_transform.py"), "w") as f:
        f.write("from databaker.framework import *\n\n")

        # Need to split this and crowbar in our xls load
        transform_lines = transform_code.split("\n")
        f.write(transform_lines[0]+"\n")
        f.write('    tabs = loadxlstabs("{}")'.format(context.last_xls_loaded)+"\n")
        for line in transform_lines[1:]:
            f.write(line+"\n")

    from temp_transform import transform_xlsx
    returned_from_transform = transform_xlsx()
    context.databaker_outputs = {thing_wanted: returned_from_transform}

@then(u'the output "{thing_wanted}" should be equal to')
def step_impl(context, thing_wanted):

    expected_output = context.text
    #actual_output = context.databaker_outputs[thing_wanted][0].name
    actual_output = context.tabs[2].name
    assert expected_output == actual_output, "{} \n\ndoes not match the expected output \n\n {}\n".format(str(actual_output), str(expected_output))

@then(u'we confirm the names of the loaded tabs are equal to')
def step_impl(context):
    tabs_wanted = json.loads(context.text)
    for tab in tabs_wanted:
        assert tab in [x.name for x in context.tabs]
    assert len(context.tabs) == len(tabs_wanted)
