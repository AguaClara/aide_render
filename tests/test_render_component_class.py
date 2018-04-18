from aide_render.builder_classes import HP, DP, Component
from aide_design.units import unit_registry as u
from aide_render.yaml import load, dump
from aide_render.builder import extract_types

class SpecialComponent(Component):
    # HP and DP are subclasses of u.Quantity from python.
    # This is where you specify defaults for a certain class.
    a_hydraulic_parameter = HP(5, u.meter)
    a_design_parameter = DP(24, u.meter)

    # static methods are used so that the functions don't depend on the existence of
    # these classes
    @staticmethod
    def special_add(a, b):
        return a + b

    def __init__(self, passed_in_param):
        self.output_parameter = self.special_add(passed_in_param, self.a_hydraulic_parameter)


def test_special_component():
    my_component = SpecialComponent(DP(30, u.meter))
    from aide_render.builder import extract_types
    assert extract_types(my_component, [DP], []) == {'a_design_parameter': 24 * u.meter, 'output_parameter': 35 * u.meter}


class MoreSpecialComponent(SpecialComponent):
    def __init__(self, a_special_component):
        self.special_component = a_special_component
        super(MoreSpecialComponent, self).__init__(DP(3, u.meter))


def test_more_special_component_recursive():
    my_component = SpecialComponent(DP(30, u.meter))
    my_recursive_component = MoreSpecialComponent(my_component)
    from aide_render.builder import extract_types
    rendered = extract_types(my_recursive_component, [DP], [SpecialComponent])
    assert rendered == {'output_parameter': 8*u.meter, 'special_component': {'a_design_parameter': 24*u.meter, 'output_parameter': 35*u.meter}}


def test_extract_types():
    class AListClass(list):
        a_class_attribute = 5

        def __init__(self):
            self.a_dict = {'a': 1, 'b': 2}

    my_class = AListClass()

    assert extract_types(my_class, [int], [AListClass, dict]) == {'a_class_attribute': 5, 'a_dict': {'a': 1, 'b': 2}}

