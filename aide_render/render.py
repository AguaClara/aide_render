from aide_render import yaml
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
    'hi there, a  and a '
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


def render_constants(stream):
    """
    Strip all Jinja tags from a template and render the remaining constants as
    a dict.
    Examples
    --------
    Jinja tags are returned as None:

    >>> render_constants("{'a jinja statement':{{5*u.m}}, 'jinja expr':{%yo%}, 'string expr': 'this works'}")
    {'a jinja statement': None, 'jinja expr': None, 'string expr': 'this works'}

    The aide_render YAML implementation parses the units tag explicitly (!u) and implicitly ( 5 meter)
    >>> render_constants("{'explicit unit':!u 20 meter, 'implicit unit': 36 meter**3, 'complex implicit unit': 0.25 meter**3/liter}")
    {'explicit unit': <Quantity(20.0, 'meter')>, 'implicit unit': <Quantity(36.0, 'meter ** 3')>, 'complex implicit unit': <Quantity(0.25, 'meter ** 3 / liter')>}

    """
    # Convert stream to string so we can use regex.
    if not isinstance(stream, str):
        stream = stream.read()
    stripped_template = strip_jinja(stream)
    return yaml.load(stripped_template)


def render(stream, d=None):
    """
    Render the template with d variables (a dict) and return the rendered file
    using the aide_render environment.
    This method can be called from within templates.
    >>> from aide_design.play import *
    >>> import os
    >>> d = {"u":u}
    >>> template_string = "{defined_units_in_jinja: {{ 5*u.meter }}}"
    >>> template_string2 = "{a: 5 meter, b: {{a}}}"
    >>> render(template_string, d)
    {'defined_units_in_jinja': <Quantity(5.0, 'meter')>}
    >>> render(template_string2, d)
    {'a': <Quantity(5.0, 'meter')>, 'b': <Quantity(5.0, 'meter')>}
    """

    # Convert stream to string so we can use regex.
    if not isinstance(stream, str):
        stream = stream.read()

    env = jinja2.Environment(
        loader=jinja2.loaders.DictLoader({"template": stream}),
        trim_blocks=True,
        lstrip_blocks=True
    )
    # Get the constant variables defined in YAML to put into Jinja context.
    variables = render_constants(stream)
    if d is not None:
        env.globals.update(d)
    if variables is not None:
        env.globals.update(variables)
    template = env.get_template("template")
    return yaml.load(template.render())


def create_aide_environment(template_fp):
    """
    This will use a prefix loader to create the aide environment. The prefixes
    are nested such that each nesting corresponds to a folder, so that within
    each template, the next nested template is passed the evaluated nesting.
    """
    return "TODO"