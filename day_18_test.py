from day_18 import shortest_path, board_from_img


def test_shortest_path():
    img = """
#########
#b.A.@.a#
#########
"""
    assert (shortest_path(board_from_img(img)).steps == 8)

    img = """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""
    assert (shortest_path(board_from_img(img)).steps == 86)

    img = """
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
"""
    assert (shortest_path(board_from_img(img)).steps == 132)

    img = """
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
"""
    assert (shortest_path(board_from_img(img)).steps == 136)

    img = """
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
"""
    assert (shortest_path(board_from_img(img)).steps == 81)


def test_multiple_robots():
    img = """
#######
#a.#Cd#
##@#@##
#######
##@#@##
#cB#Ab#
#######
"""
    assert (shortest_path(board_from_img(img)).steps == 8)

    img = """
###############
#d.ABC.#.....a#
######@#@######
###############
######@#@######
#b.....#.....c#
###############
"""
    assert (shortest_path(board_from_img(img)).steps == 24)

    img = """
#############
#DcBa.#.GhKl#
#.###@#@#I###
#e#d#####j#k#
###C#@#@###J#
#fEbA.#.FgHi#
#############
"""
    assert (shortest_path(board_from_img(img)).steps == 32)

    img = """
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############
"""
    assert (shortest_path(board_from_img(img)).steps == 72)
