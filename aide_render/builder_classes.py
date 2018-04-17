"""Include stub methods to indicate parameter types in plant python components."""

from aide_design.units import unit_registry as u


class DP(u.Quantity):
    """A Design Parameter is a pint quantity that is passed into Fusion to draw the plant. Classes that have design
    parameters as properties are considered Fusion components, and should have a corresponding Fusion component.
    """
    ...


class HP(u.Quantity):
    """A Hydraulic Parameter is a pint quantity used to characterize the hydraulic properties of a certain plant process.
    """
    ...

class Q(u.Quantity):
    """A Q (quantity) is an AIDE quantity.
    """
    ...
