"""
aide_render tests.
"""

import pytest
from aide_design.play import *
from aide_render.render import render, render_constants, assert_inputs, source_from_path
from aide_render import yaml
import os


def test_yaml_units():
    """
    Test the conversion of YAML that has the units (!u) tags.
    """
    s = "!u 1 meter"
    assert yaml.load(s) == 1*u.meter


def test_render_constants():
    """
    Test some simple renderings from tests/test_templates/simple
    """
    file_path = os.path.abspath('tests/test_templates/simple/test_render_constants.yaml')
    assert render_constants(open(file_path, 'r')) == {'implicitly_defined_quantity': 45*u.meter, 'that constant as a Jinja variable': None}


def test_render_recursive():
    """
    Test calling render() within a template
    """
    file_path = os.path.abspath('tests/test_templates/simple/test_render_recursive_parent.yaml')
    output_file_path = os.path.abspath('tests/test_templates/simple/test_render_recursive_output.yaml')
    d = {"u": u, "os": os, "render": render, "open": open}
    print(render(open(file_path, 'r'), d))
    assert render(open(file_path, 'r'), d) == yaml.load(open(output_file_path, 'r'))


def test_assert_inputs():
    """
    Test assert_inputs asserts the correct types without throwing an error, and test for when an error is thrown.
    """
    assert assert_inputs({"a": 1, "b": 2.0, "c": "3", "d": 4*u.meter}, {"a": int, "b": float, "c": str, "d": u.mile})


def test_source_from_path():
    file_path = os.path.abspath("tests/test_source_from_path.txt")
    assert source_from_path(file_path) == "This is some source text."