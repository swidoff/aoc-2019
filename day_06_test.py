from day_06 import *


def test_total_orbits():
    assert (total_orbits({'B': 'COM',
                          'C': 'B',
                          'D': 'C',
                          'E': 'D',
                          'F': 'E',
                          'G': 'B',
                          'H': 'G',
                          'I': 'D',
                          'J': 'E',
                          'K': 'J',
                          'L': 'K', }) == 42)


def test_min_transfers():
    assert (min_transfers({'B': 'COM',
                           'C': 'B',
                           'D': 'C',
                           'E': 'D',
                           'F': 'E',
                           'G': 'B',
                           'H': 'G',
                           'I': 'D',
                           'J': 'E',
                           'K': 'J',
                           'L': 'K',
                           'YOU': 'K',
                           'SAN': 'I'}, 'YOU', 'SAN') == 4)
