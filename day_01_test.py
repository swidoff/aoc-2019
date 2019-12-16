from day_01 import fuel, total_fuel


def test_fuel():
    assert (fuel(12) == 2)
    assert (fuel(14) == 2)
    assert (fuel(1969) == 654)
    assert (fuel(100756) == 33583)


def test_total_fuel():
    assert (total_fuel(14) == 2)
    assert (total_fuel(1969) == 966)
    assert (total_fuel(100756) == 50346)
