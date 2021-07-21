""" Misc functions not attached to classes """
from random import randint
from math import sqrt
import pygame


def roll_damage(damage, modifier=1):
    """Rolls the damage using various dice rolls"""
    if damage == 20:
        return roll_d_20() * modifier
    elif damage == 12:
        return roll_d_12() * modifier
    elif damage == 10:
        return roll_d_10() * modifier
    elif damage == 8:
        return roll_d_8() * modifier
    elif damage == 6:
        return roll_d_6() * modifier
    elif damage == 4:
        return roll_d_4() * modifier
    else:
        return flip_coin() * modifier


def roll_d_8():
    """roll a d8"""
    return randint(1, 8)


def roll_d_6():
    """roll a d6"""
    return randint(1, 6)


def roll_d_4():
    """roll d4"""
    return randint(1, 4)


def flip_coin():
    """flips a coin"""
    return randint(0, 1)


def roll_d_20():
    """roll a d 20, original isn't it"""
    return randint(1, 20)


def roll_d_10():
    """roll a d 10"""
    return randint(1, 10)


def roll_d_12():
    """roll a d 12"""
    return randint(1, 12)


def is_in_fov(mob, player):
    """check if a player and a mob can see eachother"""
    if (player.x, player.y, player.z) in mob.fov:
        return True
    return False


def move_cost(c1, c2):
    """Calculate the cost of moving between spots on the map (Euclidean)"""
    return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)


def pick_wall_tile(tiles):
    """pick the specific wall / fog tiles based on the adjacent values"""
    tl_corner = False
    tr_corner = False
    bl_corner = False
    br_corner = False
    left = False
    right = False
    top = False
    bottom = False
    if tiles[1][0] == 1:
        top = True
    if tiles[2][1] == 1:
        right = True
    if tiles[1][2] == 1:
        bottom = True
    if tiles[0][1] == 1:
        left = True
    if tiles[0][0] == 1:
        tl_corner = True
    if tiles[2][0] == 1:
        tr_corner = True
    if tiles[0][2] == 1:
        bl_corner = True
    if tiles[2][2] == 1:
        br_corner = True

    if (
        left == False
        and right == False
        and top == False
        and bottom == False
        and tl_corner == False
        and tr_corner == False
        and bl_corner == False
        and br_corner == False
    ):
        # no floors around normal black tile
        return 0
    elif (
        left
        and right == False
        and top == False
        and bottom == False
        and bl_corner
        and br_corner
        and tl_corner
        and tr_corner == False
    ):
        # left and bottom right corner
        return 26
    elif (
        left
        and right == False
        and top == False
        and bottom == False
        and bl_corner
        and br_corner == False
        and tl_corner
        and tr_corner
    ):
        # left and top right corner
        return 27
    elif (
        left == False
        and right
        and top == False
        and bottom == False
        and bl_corner
        and br_corner
        and tl_corner == False
        and tr_corner
    ):
        # right and bottom left corner
        return 28
    elif (
        left == False
        and right
        and top == False
        and bottom == False
        and bl_corner == False
        and br_corner
        and tl_corner
        and tr_corner
    ):
        # right and top left corner
        return 29
    elif (
        left == False
        and right == False
        and top == False
        and bottom == False
        and tl_corner
    ):
        # top left corner
        return 15
    elif (
        left == False
        and right == False
        and top == False
        and bottom == False
        and tr_corner
    ):
        # top right corner
        return 16
    elif (
        left == False
        and right == False
        and top == False
        and bottom == False
        and bl_corner
    ):
        # bottom left corner
        return 17
    elif (
        left == False
        and right == False
        and top == False
        and bottom == False
        and br_corner
    ):
        # bottom right corner
        return 18
    elif left == False and right == False and bottom and top == False and tl_corner:
        # bottom and top left corner
        return 19
    elif left == False and right == False and bottom and top == False and tr_corner:
        # bottom and top right corner
        return 20
    elif (
        left == False
        and right == False
        and bottom
        and top == False
        and tl_corner
        and tr_corner
    ):
        # bottom and top left / right corners
        return 21
    elif (
        left == False
        and right == False
        and bottom == False
        and top
        and bl_corner
        and br_corner == False
        and tl_corner
        and tr_corner
    ):
        # top and bottom left corner
        return 22
    elif (
        left == False
        and right == False
        and bottom == False
        and top
        and bl_corner == False
        and br_corner
        and tl_corner
        and tr_corner
    ):
        # top and bottom right
        return 23
    elif (
        left == False
        and right == False
        and bottom == False
        and top
        and bl_corner
        and br_corner
        and tl_corner
        and tr_corner
    ):
        # top and bottom left / right corners
        return 24
    elif left == False and right == False and top == False and bottom:
        # bottom has a floor
        return 1
    elif left and right == False and top == False and bottom:
        # bottom and left have floors
        return 2
    elif left and right and top == False and bottom:
        # bottom left and right have floors
        return 3
    elif left == False and right and top == False and bottom:
        # bottom and right have floors
        return 4
    elif left and right == False and top and bottom:
        # bottom, top and left have floors
        return 5
    elif left == False and right and top and bottom:
        # bottom, top and right have floors
        return 6
    elif left and right == False and bottom == False and top == False:
        # left has a floor
        return 7
    elif left and right and top == False and bottom == False:
        # left and right have floors
        return 8
    elif left == False and right and top == False and bottom == False:
        # right has a floor
        return 9
    elif left == False and right == False and top and bottom == False:
        # top has a floor
        return 10
    elif left == False and right == False and top and bottom:
        # top and bottom have a floor
        return 11
    elif left and right == False and top and bottom == False:
        # top and left have floors
        return 12
    elif left and right and top and bottom == False:
        # top, left and right have floors
        return 13
    elif left == False and right and top and bottom == False:
        # top and right have floors
        return 14
    elif (
        left
        and right
        and top
        and bottom
        and bl_corner
        and br_corner
        and tl_corner
        and tr_corner
    ):
        # walled in
        return 25
    else:
        # Catch all go for black for now
        return 0


def make_cursor(arrow):
    """generate a cursor"""
    hotspot = None
    for y in range(len(arrow)):
        for x in range(len(arrow[y])):
            if arrow[y][x] in ["x", ",", "O"]:
                hotspot = x, y
                break
        if hotspot != None:
            break
    if hotspot == None:
        raise Exception("No hotspot specified for cursor!")
    s2 = []
    for line in arrow:
        s2.append(line.replace("x", "X").replace(",", ".").replace("O", "o"))
    cursor, mask = pygame.cursors.compile(s2, "X", ".", "o")
    size = len(arrow[0]), len(arrow)
    return size, hotspot, cursor, mask
