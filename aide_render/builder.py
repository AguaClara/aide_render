"""A module that can build instances of plant components into a valide aide_draw yaml"""
from aide_render.builder_classes import DP

def render(component_instance):
    """Take in an instance of a component and produce the dict necessary to design it."""
    DP_dict = {}

    for name, var in vars(component_instance).items():
        if isinstance(var, DP):
            DP_dict[name] = var

    return DP_dict
