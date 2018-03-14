"""
aide_render tests.
"""

import pytest
from aide_design.play import *
from aide_render.render import render, render_constants
from aide_render import yaml
import os
import sys


# s = """this:
#       - a
#       - test
#       - of
#     the strip_jinja function: [ {{did it work?}} ]
#     {% how about now? %}
#     """

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
    d = {"u": u}
    assert render(open(file_path, 'r'), d) == {'implicitly_defined_quantity': 45*u.meter, 'that constant as a Jinja variable': 45*u.meter}


def test_render_recursive():
    """
    Test calling render() within a template
    """
    file_path = os.path.abspath('tests/test_templates/simple/test_render_recursive_parent.yaml')
    output_file_path = os.path.abspath('tests/test_templates/simple/test_render_recursive_output.yaml')
    d = {"u": u, "os": os, "render": render, "open": open}
    print(render(open(file_path, 'r'), d))
    assert render(open(file_path, 'r'), d) == yaml.load(open(output_file_path, 'r'))
