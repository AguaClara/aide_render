"""aide_render's YAML decomposition logic. aide_render uses standard pyYaml with
additional tags supported. Here's a list of the currently supported tags and
their use case:
  * !u: used with a unit string (ie: 5 meter) to represent a pint quantity.
  * !quantity: used to represent a pint quantity: <Quantity(1.25, 'liter / second')>
"""

from yaml import add_constructor, add_representer, add_implicit_resolver, load, dump
from aide_design.units import unit_registry as u
import re


def units_representer(dumper, data):
    return dumper.represent_scalar(u'!u', str(data))


add_representer(u.Quantity, units_representer)


def units_constructor(loader, node):
    value = loader.construct_scalar(node)
    mag, units = value.split(' ')
    return u.Quantity(float(mag), units)


add_constructor(u'!u', units_constructor)


# resolve units implicitly:
pattern = re.compile(r'[+-]?([0-9]*[.])?[0-9]+[ ]([A-z]+[/*]*[0-9]*)')
add_implicit_resolver(u'!u', pattern)


def quantity_representer(dumper, data):
    return dumper.represent_scalar(u'!quantity', data)


add_representer(u.Quantity, quantity_representer)


def quantity_constructor(loader, node):
    value = loader.construct_scalar(node)
    magnitude_pattern = re.compile(r'\((.*),')
    units_pattern = re.compile(r'(.*)')
    mag, units = re.match(magnitude_pattern).group(), re.match(units_pattern).group()
    return u.Quantity(float(mag), units)


add_constructor(u'!quantity', quantity_constructor)

pattern = re.compile(r'<Quantity\(.*\)>')
add_implicit_resolver(u'!quantity', pattern)
