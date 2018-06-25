"""Main aide_render designs. All designs should go in here. For now, the syntax for building a design is:
aide_render(yaml_string)
The root of the YAML string is the name of a class that will be built to represent that string. Any inner parameters
are passed directly to the init functioin of that class. The return is an output YAML of the finished design.
"""

def render_lfom():
    from aide_render.builder_classes import DP, HP
    from .templates.lfom import LFOM
    from aide_design.units import unit_registry as u
    my_lfom = LFOM(HP(20, u.L / u.s))
    import sys
    from aide_render.builder import extract_types
    lfom_design_dict = extract_types(my_lfom, [DP], [])
    from aide_render.yaml import yaml
    yaml.dump(lfom_design_dict, stream=sys.stdout)