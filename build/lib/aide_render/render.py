import yaml
import jinja2
from aide_design.units import unit_registry as u
import aide_design
import numpy as np
import os
import sys
import re
from aide_design.play import *
import pint

"""Implement a "print for Fusion" function that takes a pint value and prints it as a
string-representable Fusion unit input.

Implement a yaml class that can serialize and deserialize pint.
"""

def strip_jinja(string: str):
    """
    Strip all Jinja tags from the string.
    >>> strip_jinja("hi there, a {{ jinja.statement }} and a {% jinja.expr %}")
    "hi there, a and a"
    """
    # Match Jinja statements
    regex = re.compile("({{.*?}})")
    string = re.sub(regex, '', string)
    # Match Jinja expression
    regex = re.compile("({%.*?%})")
    string = re.sub(regex, '', string)
    # Match Jinja expression
    regex = re.compile("({#.*?#})")
    string = re.sub(regex, '', string)
    return re.sub(regex, '', string)

def create_aide_environment(template_fp):
    """
    This will use a prefix loader to create the aide environment. The prefixes
    are nested such that each nesting corresponds to a folder, so that within
    each template, the next nested template is passed the evaluated nesting.
    """


def render_constants(template: str):
    """
    Extract all Jinja tags from a template and render the remaining constants as
    a dict.
    Examples
    --------
    >>> render_constants("{'a jinja statement':{{5*u.m}}, 'jinja expr':{%yo%}, 'string expr': 'this works'}")
    {'a jinja statement': None, 'jinja expr': None, 'string expr': 'this works'}
    """
    stripped_template = strip_jinja(template)
    return yaml.load(stripped_template)

def render(template_path, d):
    """
    Render the template with d variables (a dict) and return the rendered file
    using the aide_render environment.
    This method should be called from within templates.
    >>> from aide_design.play import *
    >>> import os
    >>> d = {"u":u}
    >>> file_path = os.path.abspath('./tests/test_templates/simple/test.yaml')
    >>> render(file_path, d)

    """
    folder_path = "/".join(file_path.split("/")[:-1])
    env = jinja2.Environment(
        loader=jinja2.loaders.FileSystemLoader(folder_path),
        trim_blocks=True,
        lstrip_blocks=True
    )
    env.globals.update(d)
    template = env.get_template(file_path.split("/").pop())
    return template.render()
