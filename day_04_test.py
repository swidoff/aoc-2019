from day_04 import *


def test_valid_password1():
    assert (valid_password1(111111) == True)
    assert (valid_password1(223450) == False)
    assert (valid_password1(223456) == True)
    assert (valid_password1(123789) == False)
    assert (valid_password1(123788) == True)


def test_valid_password2():
    assert (valid_password2(111111) == False)
    assert (valid_password2(223450) == False)
    assert (valid_password2(223456) == True)
    assert (valid_password2(123789) == False)
    assert (valid_password2(123788) == True)
    assert (valid_password2(112233) == True)
    assert (valid_password2(123444) == False)
    assert (valid_password2(111122) == True)
