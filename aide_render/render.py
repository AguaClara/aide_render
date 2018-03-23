from aide_render import yaml
import jinja2
from aide_design.units import unit_registry as u
import aide_design
import numpy as np
import os
import sys
import re
from aide_design.play import *
import copy
from jinja_atoms.ext import JinjaAtomsExtension
from jinja_atoms.decorators import atom


from jinja2 import contextfunction, environmentfunction

@atom('/Users/ethankeller/git_repos/AguaClara/AIDE/aide_render/tests/test_templates', 'test_atom.yaml')
def simple_atom(my_arg, my_kwarg=None):
  return {'arg': my_arg, 'kwarg': my_kwarg}


@contextfunction
def show_context(context):
    """Shows what you can do with the context

    Parameters
    ----------
    context

    Returns
    -------

    Examples
    --------

    >>> import jinja2
    >>> env = jinja2.Environment()
    >>> env.globals.update({"yo": "yodles"})
    >>> t = env.from_string("{{show_context()}}")
    >>> t.render({"local_variable":"hello", "show_context": show_context})
    a variable: hello
    the parent: <class 'dict'>
    the environment: <class 'jinja2.environment.Environment'>
    the variables: {}
    the exported_vars: set()
    the names: None
    the blocks: {}
    the eval_ctx: <class 'jinja2.nodes.EvalContext'>
    'None'


    """
    print("a variable:", context["local_variable"])
    print("the parent:", type(context.parent))
    print("the environment:", type(context.environment))
    print("the variables:", context.vars)
    print("the exported_vars:", context.exported_vars)
    print("the names:", context.name)
    print("the blocks:", context.blocks)
    print("the eval_ctx:", type(context.eval_ctx))


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
    >>> render_constants("{'explicit unit':!q 20 meter, 'implicit unit': 36 meter**3, 'complex implicit unit': 0.25 meter**3/liter}")
    {'explicit unit': <Quantity(20.0, 'meter')>, 'implicit unit': <Quantity(36.0, 'meter ** 3')>, 'complex implicit unit': <Quantity(0.25, 'meter ** 3 / liter')>}

    """
    # Convert stream to string so we can use regex.
    if not isinstance(stream, str):
        stream = stream.read()
    stripped_template = strip_jinja(stream)
    d = yaml.load(stripped_template)
    t = type(d)
    if not t == dict:
        raise ValueError("Template must parse into a dict. Template was parsed as a {}".format(str(t)))
    return yaml.load(stripped_template)


@contextfunction
def render(context, template, template_folder_path, d={}):
    """Render the template with d variables (a dict) and return the rendered file
    using the aide_render environment.
    This method should be called from within templates.

    Examples
    --------

    """

    if not context and not template_folder_path:
        raise ValueError("Need a template folder path if not called within template.")

    elif template_folder_path:
        loader = jinja2.loaders.FileSystemLoader(template_folder_path)
    elif context:
        loader = context.environment.loader

    overlay_env = jinja2.Environment(
                             loader=jinja2.loaders.FileSystemLoader(template_folder_path),
                             trim_blocks=True,
                             lstrip_blocks=True
                             )

    source, filename, uptodate = overlay_env.loader.get_source(overlay_env, template)

    # Get the constant variables defined in YAML to put into Jinja context.
    variables = render_constants(source)

    template = overlay_env.get_template(template)

    new_context = {}

    # Add YAML variables if there are any.
    if variables:
        variables.update(d)
    # Add context variables if there are any.
    print(context.parent)
    if context:
        for k, v in context.parent.items():
            new_context[k] = v

        new_context.update(variables)

    d = yaml.load(template.render(new_context))

    return d


def source_from_path(file_path: str) -> str:
    """

    Parameters
    ----------
    file_path: Absolute path to the file to read.

    Returns
    -------
    str
        The contents of the file.

    """
    with open(file_path) as f:
        return f.read()

@contextfunction
def assert_inputs(variables:dict, types_dict:dict, strict=True, silent=False):
    """Check variables against their expected type. Also can check more complex types, such as whether the expected
    and actual dimensionality of pint units are equivalent.

    Parameters
    ----------
    variables : dict
        Contain variable_name : variable_object key-value pairs.
    types_dict : dict
        A dictionary containing variable:type key value pairs.
    strict :obj: bool, optional
        If true, the function ensures all the variables in types_dict are present in variables.
    silent :obj: bool, optional
        If true, the function only returns a boolean rather than throwing an error.

    Returns
    -------
    bool
        True if the variables dict passes the assert_inputs check as described.

    Raises
    ------
    ValueError
        If silent is turned to false and the inputs do not pass the assert_inputs test

    Examples
    --------

    Standard usage showing a passing collection of parameters. This passes both the non-strict and strict options.

    >>> variables = {"a" : 1, "b" : 1.0, "c" : "string"}
    >>> types_dict = {"a" : int, "b" : float, "c" : str}
    >>> assert_inputs(variables,types_dict)
    True

    Wrong types error thrown:

    >>> types_dict = {"a" : str, "b" : str, "c" : str}
    >>> assert_inputs(variables,types_dict)
    Traceback (most recent call last):
    TypeError: Can't convert the following implicitly: {'a': "Actual type: <class 'int'> Intended type: <class 'str'>", 'b': "Actual type: <class 'float'> Intended type: <class 'str'>"}.

    Not enough variables are present:
    >>> assert_inputs({"a":1}, {"a":int, "b": int})
    Traceback (most recent call last):
    NameError: names 'b' are not defined

    >>> from aide_design.play import *
    >>> assert_inputs({"length" : 1*u.meter},{"length" : u.mile})
    True
    >>> assert_inputs({"length" : 1*u.meter**2},{"length" : u.mile})
    Traceback (most recent call last):
    TypeError: Can't convert the following implicitly: {'length': 'Actual dimensionality: [length] ** 2 Intended dimensionality: [length]'}.

    """
    check = True
    # Store the intended types
    type_error_dicionary = {}
    # Store the missing variables
    missing = []

    for name, t in types_dict.items():
        try:
            var = variables[name]
            # print(var)
            # print(t.__repr__)

            # check if this is a pint variable and has compatible dimensionality.
            if isinstance(var, u.Quantity):
                if not var.dimensionality == t.dimensionality:
                    type_error_dicionary[name] = "Actual dimensionality: {} Intended dimensionality: {}".format(
                        var.dimensionality, t.dimensionality)

            # check if types are compatible
            elif not isinstance(var, t):
                type_error_dicionary[name] = "Actual type: {} Intended type: {}".format(type(var), t)

        # If the variable is missing
        except KeyError:
            missing.append(name)

    check = not type_error_dicionary
    if strict and check:
        check = not missing

    if not silent and not check:
        if missing:
            raise NameError("names {} are not defined".format("'" + "', '".join(missing) + "'"))
        if type_error_dicionary:
            raise TypeError("Can't convert the following implicitly: {}.".format(type_error_dicionary))
    return check

aide_render_dict = {"u": u, "os": os, "render": render, "render_constants": render_constants, "assert_inputs":
    assert_inputs, "dict": dict, "show_context": show_context, "str": str, "float": float, "np": np, "dump": yaml.dump}


@contextfunction
def start_aide_render(template_folder_path, template_to_render, user_params):
    env = jinja2.Environment(
                             loader=jinja2.loaders.FileSystemLoader(template_folder_path),
                             trim_blocks=True,
                             lstrip_blocks=True,
                            extensions=[JinjaAtomsExtension]
                             )
    env.globals.update(aide_render_dict)
    return env.get_template(template_to_render).render(user_params)