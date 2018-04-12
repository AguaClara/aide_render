from aide_render.yaml import load, dump
from aide_design.play import *

################### YAML tag testing ###############################

# UNITS

def test_load_yaml():
    # explicit with the u tag:
    s = """ {"quantity": !q 78 m} """
    assert load(s) == {"quantity": 78*u.meter}
    # implicit:
    s = """ {"quantity": 78 m} """
    assert load(s) == {"quantity": 78 * u.meter}


def test_dump_yaml():
    # explicit with the u tag:
    s = '{quantity: 78 meter}\n'
    assert dump({"quantity": 78*u.meter}) == s


def test_load_and_dump_yaml():
    s = """
    explicit_q: !q 12 m
    implicit_q: 34 mg/cm**3
    nested:
        e: !q 45 mg
        i: 10 m**3"""
    loaded = load(s)
    assert loaded == {'explicit_q': 12 *u.meter, 'implicit_q': 34*u.mg/u.cm**3, 'nested': {'e': 45*u.milligram, 'i': 10*u.meter ** 3}}
    dumped = dump(loaded)
    assert loaded == load(dumped)


def test_yaml_hard_units():
    #a list of dictionaries to test
    d_list = []
    d_list.append({"weird": 45 * u.m**3.5/ u.pound_force_per_square_inch*u.kg})
    for d in d_list:
        print(dump(d))
        # check if it is dumped reliably
        assert dump(d) == dump(load(dump(d)))
        #check if d is loaded reliably
        assert load(dump(d)) == load(dump(load(dump(d))))

