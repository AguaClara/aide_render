"""
aide_render tests.
"""

import os

import jinja2
from aide_design.play import *
from aide_render.jinja_render.render import render_constants, assert_inputs, source_from_path, start_aide_render


def test_render_constants():
    """
    Test some simple renderings from tests/test_templates/simple
    """
    folder_path = os.path.abspath('tests/test_templates/simple')
    template_name = 'test_render_constants.yaml'
    env = jinja2.Environment(
        loader=jinja2.loaders.FileSystemLoader(folder_path),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    print(folder_path)

    assert render_constants(env, template_name) == {'implicitly_defined_quantity': 45*u.meter, 'that constant as a Jinja variable': None}

def test_render_constants_no_environment():
    s = """
name: A
cp:
    this: is
    a: test
    of: renderconstants
"""
    doc = {'a': 'test', 'of': 'renderconstants', 'this': 'is'}
    assert render_constants(None, s) == doc



def test_render_recursive():
    """
    Test calling extract_types() within a template
    """
    folder_path = os.path.abspath('tests/test_templates/simple')
    output_file_path = os.path.abspath('tests/test_templates/simple/test_render_recursive_output.yaml')
    user_inputs = {"flow": 5*u.L/u.s}
    rendered = start_aide_render(folder_path, "test_render_recursive_parent.yaml", user_inputs)
    print(rendered)
    assert rendered == source_from_path(output_file_path)


def test_assert_inputs():
    """
    Test assert_inputs asserts the correct types without throwing an error, and test for when an error is thrown.
    """
    assert assert_inputs({"a": 1, "b": 2.0, "c": "3", "d": 4*u.meter}, {"a": int, "b": float, "c": str, "d": u.mile})


def test_source_from_path():
    file_path = os.path.abspath("tests/test_source_from_path.txt")
    assert source_from_path(file_path) == "This is some source text."