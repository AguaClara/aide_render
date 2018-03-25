import aide_render.render as render
import aide_render.yaml as yaml
import os
from aide_design.play import u

# Pyramid example - let's build a pyramid, testing each building block along the way!


def test_block_stack():
    # book_stack Folder Path:
    folder_path = os.path.abspath('tests/test_templates/block_stack_example')

    rendered = render.start_aide_render(folder_path, "block_stack.yaml", {})
    print(rendered)
    assert isinstance(yaml.load(rendered), dict)


def test_build_block():
    # Pyramid Folder Path:
    folder_path = os.path.abspath('tests/test_templates/pyramid_example')
    # a custom function I want to pass in:
    def surface_area_block(h, w, L):
        return 2*(h * w + h * L + L * w)
    rendered = render.start_aide_render(folder_path, "block.yaml", {'block_inputs':{'h': 100*u.cm, "L": 2*u.m, "w": 2*u.feet,
                                                                    'density': 45*u.kg/u.m**3, 'material': 'rock',
                                                                    "surface_area_block": surface_area_block,
                                                                    "usage": "pyramid", "cost": 40*u.dollar}})
    print(rendered)
    assert isinstance(yaml.load(rendered), dict)


def test_build_pyramid():
    # Pyramid Folder Path:
    folder_path = os.path.abspath('tests/test_templates/pyramid_example')
    # Some custom functions I want to pass in (for permanently adding things to the aide_render workspace, modify the
    # aide_render_dict in aide_render.render.py
    def surface_area_block(h, w, L):
        return 2*(h * w + h * L + L * w)
    rendered = render.start_aide_render(folder_path, "pyramid.yaml", {'h': 100*u.m, "L": 2*u.m, "w": 2*u.feet,
                                                                      'density': 45*u.kg/u.m**3, 'material': 'rock',
                                                                      "surface_area_block": surface_area_block})
    loaded = yaml.load(rendered)
    assert isinstance(yaml.load(rendered), dict)

    # Turn this on to see result:
    print(loaded)
    assert False
