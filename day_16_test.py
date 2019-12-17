from day_16 import fft_phase, fft, fft2


def test_fft_phase():
    assert fft_phase([1, 2, 3, 4, 5, 6, 7, 8]) == [4, 8, 2, 2, 6, 1, 5, 8]
    assert fft_phase([4, 8, 2, 2, 6, 1, 5, 8]) == [3, 4, 0, 4, 0, 4, 3, 8]
    assert fft_phase([3, 4, 0, 4, 0, 4, 3, 8]) == [0, 3, 4, 1, 5, 5, 1, 8]
    assert fft_phase([0, 3, 4, 1, 5, 5, 1, 8]) == [0, 1, 0, 2, 9, 4, 9, 8]


def test_fft():
    assert fft('80871224585914546619083218645595')[:8] == '24176176'
    assert fft('19617804207202209144916044189917')[:8] == '73745418'
    assert fft('69317163492948606335995924319873')[:8] == '52432133'


def test_fft2():
    assert fft2('03036732577212944063491565474664') == '84462026'
    assert fft2('02935109699940807407585447034323') == '78725270'
    assert fft2('03081770884921959731165446850517') == '53553731'

#
# 0 3 0 3 6 7 3 2 5 7 7 2 1 2 9 4 4 0 6 3 4 9 1 5 6 5 4 7 4 6 6 4
# 1 0-1 0 1 0-1 0 1 0-1 0 1 0-1 0 1 0-1 0 1 0-1 0 1 0-1 0 1 0-1 0
# 0 1 1 0 0-1-1 0 0 1 1 0 0-1-1 0 0 1 1 0 0-1-1 0 0 1 1 0 0-1-1 0
# 0 0 1 1 1 0 0 0-1-1-1 0 0 0 1 1 1 0 0 0-1-1-1 0 0 0 1 1 1 0 0 0-1-1-1 0 0 0
# 0 0 0 1 1 1 1 0 0 0 0-1-1-1-1 0 0 0 0 1 1 1 1 0 0 0 0-1-1-1-1 0 0 0 0
#
# 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
# 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
# 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
# 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1-1

# 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3
# 0 0 0-1-1-1-1 0 0 0 0 1 1 1 1 0 0 0 0
# 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0-1-1-1-1
# input = 32
# pattern = 4
