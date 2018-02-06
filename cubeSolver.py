#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Title: Cube Solver
# Author: Ryan Slater
# Date: 1/28/2017
# =============================================================================

import RubiksCube as Cube
import time
import matplotlib.pyplot as plt
import numpy as np
import statistics

def solve(scrambledCube, printNet=False, printStatistics=False):
    t0 = time.time()
    tc = Cube.cube(int(len(scrambledCube.net)/3))
    tc.net = scrambledCube.net
    if printNet:
        tc.printNet()
        print()
    if tc.size == 2:
        # First layer
        turns = []
        turns.extend(solve2x2corner(tc, 0))
        turns.extend(solve2x2corner(tc, 1))
        turns.extend(solve2x2corner(tc, 2))
        turns.extend(solve2x2corner(tc, 3))

        # OLL
        if not tc.checkSolved():
            turns.extend(oll2x2(tc))

        # PLL
        if not tc.checkSolved():
            turns.extend(pll2x2(tc))

    # Finish
    if printNet:
        tc.printNet()
        print()
    if printStatistics:
        t1 = time.time()
        pre = len(turns)
        turns = cleanSolution(turns)
        post = len(turns)
        print(str(len(turns)) + ' moves / ' + str(round(t1-t0, 1)) + ' seconds (' + str(round(len(turns)/(t1-t0), 1)) + ' moves/second)')
        print('Cleaning saved ' + str(pre-post) + ' turns')
        for i in turns:
            print(i.upper(), end=' ')
        print()
    if not tc.checkSolved():
        return 'failed'
    return(len(turns))


def areSame(x, y):
    if len(x) == len(y):
        if x[0] == y[0]:
            return True
    return False

def areReverses(x, y):
    if len(x) != len(y):
        if x[0] == y[0]:
            return True
    return False

def getReverse(x):
    prime = ""
    if len(x) == 1:
        prime = "'"
    return x[0] + prime

def cleanSolution(turns):
    # Removes conecutive different direction turns on the same face (u, u' = /)
    stop = len(turns)
    i = 1
    while i < stop:
        x = turns[i-1]
        y = turns[i]
        if areReverses(x, y):
            turns = turns[:i-1] + turns[i+1:]
            stop = len(turns)
            i = 0
        i += 1
    # Convert three identical consecutive turns to one opposite turn (u, u, u = u'), also fix scramble to do the same
    stop = len(turns)
    i = 2
    while i < stop:
        x = turns[i-2]
        y = turns[i-1]
        z = turns[i]
        if areSame(x, y) and areSame(y, z):
            turns = turns[:i-2] + [getReverse(x)] + turns[i+1:]
            stop = len(turns)
            i = 2
        i += 1
    # Removes conecutive different direction turns on the same face (u, u' = /)
    stop = len(turns)
    i = 1
    while i < stop:
        x = turns[i-1]
        y = turns[i]
        if areReverses(x, y):
            turns = turns[:i-1] + turns[i+1:]
            stop = len(turns)
            i = 0
        i += 1
    return turns

def solve2x2corner(cube, corner):
    turns = []
    pullup = True
    if corner == 0:
        if (cube.net[0][2] == 1 and cube.net[2][0] == 2 and cube.net[2][7] == 3) or (cube.net[0][2] == 3 and cube.net[2][0] == 1 and cube.net[2][7] == 2) or (cube.net[0][2] == 2 and cube.net[2][0] == 3 and cube.net[2][7] == 1) or (cube.net[0][3] == 1 and cube.net[2][5] == 3 and cube.net[2][6] == 2) or (cube.net[0][3] == 2 and cube.net[2][5] == 1 and cube.net[2][6] == 3) or (cube.net[0][3] == 3 and cube.net[2][5] == 2 and cube.net[2][6] == 1) or (cube.net[1][3] == 1 and cube.net[2][3] == 3 and cube.net[2][4] == 2) or (cube.net[1][3] == 2 and cube.net[2][3] == 1 and cube.net[2][4] == 3) or (cube.net[1][3] == 3 and cube.net[2][3] == 2 and cube.net[2][4] == 1) or (cube.net[1][2] == 1 and cube.net[2][1] == 3 and cube.net[2][2] == 2) or (cube.net[1][2] == 2 and cube.net[2][1] == 1 and cube.net[2][2] == 3) or (cube.net[1][2] == 3 and cube.net[2][1] == 2 and cube.net[2][2] == 1):
            pullup = False
        if not pullup:
            turns.extend(solve2x2CornerFromTop(cube, corner))
        if pullup:
            if (cube.net[4][3] == 1 and cube.net[3][3] == 2 and cube.net[3][4] == 3) or (cube.net[4][3] == 3 and cube.net[3][3] == 1 and cube.net[3][4] == 2) or (cube.net[4][3] == 2 and cube.net[3][3] == 3 and cube.net[3][4] == 1):
                turns.extend(["r", "u", "r'", "u'"])
                cube.performTurns(["r", "u", "r'", "u'"])
            elif (cube.net[5][3] == 1 and cube.net[3][5] == 2 and cube.net[3][6] == 3) or (cube.net[5][3] == 3 and cube.net[3][5] == 1 and cube.net[3][6] == 2) or (cube.net[5][3] == 2 and cube.net[3][5] == 3 and cube.net[3][6] == 1):
                turns.extend(["b", "u", "b'", "u'"])
                cube.performTurns(["b", "u", "b'", "u'"])
            elif (cube.net[5][2] == 1 and cube.net[3][7] == 2 and cube.net[3][0] == 3) or (cube.net[5][2] == 3 and cube.net[3][7] == 1 and cube.net[3][0] == 2) or (cube.net[5][2] == 2 and cube.net[3][7] == 3 and cube.net[3][0] == 1):
                turns.extend(["l", "u", "l'", "u'"])
                cube.performTurns(["l", "u", "l'", "u'"])
            turns.extend(solve2x2CornerFromTop(cube, corner))
    elif corner == 1:
        if (cube.net[0][2] == 1 and cube.net[2][0] == 3 and cube.net[2][7] == 5) or (cube.net[0][2] == 5 and cube.net[2][0] == 1 and cube.net[2][7] == 3) or (cube.net[0][2] == 3 and cube.net[2][0] == 5 and cube.net[2][7] == 1) or (cube.net[0][3] == 1 and cube.net[2][5] == 3 and cube.net[2][6] == 5) or (cube.net[0][3] == 5 and cube.net[2][5] == 1 and cube.net[2][6] == 3) or (cube.net[0][3] == 3 and cube.net[2][5] == 5 and cube.net[2][6] == 1) or (cube.net[1][3] == 1 and cube.net[2][3] == 5 and cube.net[2][4] == 3) or (cube.net[1][3] == 3 and cube.net[2][3] == 1 and cube.net[2][4] == 5) or (cube.net[1][3] == 5 and cube.net[2][3] == 3 and cube.net[2][4] == 1) or (cube.net[1][2] == 1 and cube.net[2][1] == 5 and cube.net[2][2] == 3) or (cube.net[1][2] == 3 and cube.net[2][1] == 1 and cube.net[2][2] == 5) or (cube.net[1][2] == 5 and cube.net[2][1] == 3 and cube.net[2][2] == 1):
            pullup = False
        if not pullup:
            turns.extend(solve2x2CornerFromTop(cube, corner))
        if pullup:
            if (cube.net[5][3] == 1 and cube.net[3][5] == 3 and cube.net[3][6] == 5) or (cube.net[5][3] == 5 and cube.net[3][5] == 1 and cube.net[3][6] == 3) or (cube.net[5][3] == 3 and cube.net[3][5] == 5 and cube.net[3][6] == 1):
                turns.extend(["b", "u", "b'", "u'"])
                cube.performTurns(["b", "u", "b'", "u'"])
            elif (cube.net[5][2] == 1 and cube.net[3][7] == 3 and cube.net[3][0] == 5) or (cube.net[5][2] == 5 and cube.net[3][7] == 1 and cube.net[3][0] == 3) or (cube.net[5][2] == 3 and cube.net[3][7] == 5 and cube.net[3][0] == 1):
                turns.extend(["l", "u", "l'", "u'"])
                cube.performTurns(["l", "u", "l'", "u'"])
            turns.extend(solve2x2CornerFromTop(cube, corner))
    elif corner == 2:
        if (cube.net[0][2] == 1 and cube.net[2][0] == 5 and cube.net[2][7] == 6) or (cube.net[0][2] == 6 and cube.net[2][0] == 1 and cube.net[2][7] == 5) or (cube.net[0][2] == 5 and cube.net[2][0] == 6 and cube.net[2][7] == 1) or (cube.net[0][3] == 1 and cube.net[2][5] == 6 and cube.net[2][6] == 5) or (cube.net[0][3] == 5 and cube.net[2][5] == 1 and cube.net[2][6] == 6) or (cube.net[0][3] == 6 and cube.net[2][5] == 5 and cube.net[2][6] == 1) or (cube.net[1][3] == 1 and cube.net[2][3] == 6 and cube.net[2][4] == 5) or (cube.net[1][3] == 5 and cube.net[2][3] == 1 and cube.net[2][4] == 6) or (cube.net[1][3] == 6 and cube.net[2][3] == 5 and cube.net[2][4] == 1) or (cube.net[1][2] == 1 and cube.net[2][1] == 6 and cube.net[2][2] == 5) or (cube.net[1][2] == 5 and cube.net[2][1] == 1 and cube.net[2][2] == 6) or (cube.net[1][2] == 6 and cube.net[2][1] == 5 and cube.net[2][2] == 1):
            pullup = False
        if not pullup:
            turns.extend(solve2x2CornerFromTop(cube, corner))
        if pullup:
            turns.extend(["l", "u", "l'", "u'"])
            cube.performTurns(["l", "u", "l'", "u'"])
            turns.extend(solve2x2CornerFromTop(cube, corner))
    elif corner == 3:
        turns.extend(solve2x2CornerFromTop(cube, corner))
    return turns

def solve2x2CornerFromTop(cube, corner):
    turns = []
    uCount = 0
    if corner == 0:
        if cube.net[4][2] == 1 and cube.net[3][2] == 3 and cube.net[3][1] == 2:
            return turns
        if (cube.net[0][2] == 1 and cube.net[2][0] == 2 and cube.net[2][7] == 3) or (cube.net[0][2] == 3 and cube.net[2][0] == 1 and cube.net[2][7] == 2) or (cube.net[0][2] == 2 and cube.net[2][0] == 3 and cube.net[2][7] == 1):
            uCount = 3
        elif (cube.net[0][3] == 1 and cube.net[2][5] == 3 and cube.net[2][6] == 2) or (cube.net[0][3] == 2 and cube.net[2][5] == 1 and cube.net[2][6] == 3) or (cube.net[0][3] == 3 and cube.net[2][5] == 2 and cube.net[2][6] == 1):
            uCount = 2
        elif (cube.net[1][3] == 1 and cube.net[2][3] == 3 and cube.net[2][4] == 2) or (cube.net[1][3] == 2 and cube.net[2][3] == 1 and cube.net[2][4] == 3) or (cube.net[1][3] == 3 and cube.net[2][3] == 2 and cube.net[2][4] == 1):
            uCount = 1
        for i in range(uCount):
            cube.performTurns(['u'])
            turns.append('u')
        count = 0
        tmp = Cube.cube(2)
        tmp.net = np.copy(cube.net)
        while True:
            count += 1
            tmp.performTurns(["l'", "u'", 'l', 'u'])
            if tmp.net[4][2] == 1 and tmp.net[3][1] == 2 and tmp.net[3][2] == 3:
                if count <= 3:
                    for i in range(count):
                        turns.extend(["l'", "u'", 'l', 'u'])
                        cube.performTurns(["l'", "u'", 'l', 'u'])
                else:
                    for i in range(6-count):
                        turns.extend(["u'", "l'", "u", "l"])
                        cube.performTurns(["u'", "l'", "u", "l"])
                return turns
    elif corner == 1:
        if cube.net[4][3] == 1 and cube.net[3][3] == 3 and cube.net[3][4] == 5:
            return turns
        if (cube.net[0][2] == 1 and cube.net[2][0] == 3 and cube.net[2][7] == 5) or (cube.net[0][2] == 5 and cube.net[2][0] == 1 and cube.net[2][7] == 3) or (cube.net[0][2] == 3 and cube.net[2][0] == 5 and cube.net[2][7] == 1):
            uCount = 2
        elif (cube.net[0][3] == 1 and cube.net[2][5] == 5 and cube.net[2][6] == 3) or (cube.net[0][3] == 3 and cube.net[2][5] == 1 and cube.net[2][6] == 5) or (cube.net[0][3] == 5 and cube.net[2][5] == 3 and cube.net[2][6] == 1):
            uCount = 1
        elif (cube.net[1][2] == 1 and cube.net[2][1] == 5 and cube.net[2][2] == 3) or (cube.net[1][2] == 3 and cube.net[2][1] == 1 and cube.net[2][2] == 5) or (cube.net[1][2] == 5 and cube.net[2][1] == 3 and cube.net[2][2] == 1):
            uCount = 3
        for i in range(uCount):
            cube.performTurns(['u'])
            turns.append('u')
        count = 0
        tmp = Cube.cube(2)
        tmp.net = np.copy(cube.net)
        while True:
            count += 1
            tmp.performTurns(["r", "u", "r'", "u'"])
            if tmp.net[4][3] == 1 and tmp.net[3][3] == 3 and tmp.net[3][4] == 5:
                if count <= 3:
                    for i in range(count):
                        turns.extend(["r", "u", "r'", "u'"])
                        cube.performTurns(["r", "u", "r'", "u'"])
                else:
                    for i in range(6-count):
                        turns.extend(["u", "r", "u'", "r'"])
                        cube.performTurns(["u", "r", "u'", "r'"])
                return turns
    elif corner == 2:
        if cube.net[5][3] == 1 and cube.net[3][5] == 5 and cube.net[3][6] == 6:
            return turns
        if (cube.net[0][2] == 1 and cube.net[2][0] == 5 and cube.net[2][7] == 6) or (cube.net[0][2] == 6 and cube.net[2][0] == 1 and cube.net[2][7] == 5) or (cube.net[0][2] == 5 and cube.net[2][0] == 6 and cube.net[2][7] == 1):
            uCount = 1
        elif (cube.net[1][3] == 1 and cube.net[2][3] == 6 and cube.net[2][4] == 5) or (cube.net[1][3] == 5 and cube.net[2][3] == 1 and cube.net[2][4] == 6) or (cube.net[1][3] == 6 and cube.net[2][3] == 5 and cube.net[2][4] == 1):
            uCount = 3
        elif (cube.net[1][2] == 1 and cube.net[2][1] == 6 and cube.net[2][2] == 5) or (cube.net[1][2] == 5 and cube.net[2][1] == 1 and cube.net[2][2] == 6) or (cube.net[1][2] == 6 and cube.net[2][1] == 5 and cube.net[2][2] == 1):
            uCount = 2
        for i in range(uCount):
            cube.performTurns(['u'])
            turns.append('u')
        count = 0
        tmp = Cube.cube(2)
        tmp.net = np.copy(cube.net)
        while True:
            count += 1
            tmp.performTurns(["b", "u", "b'", "u'"])
            if tmp.net[5][3] == 1 and tmp.net[3][5] == 5 and tmp.net[3][6] == 6:
                if count <= 3:
                    for i in range(count):
                        turns.extend(["b", "u", "b'", "u'"])
                        cube.performTurns(["b", "u", "b'", "u'"])
                else:
                    for i in range(6-count):
                        turns.extend(["u", "b", "u'", "b'"])
                        cube.performTurns(["u", "b", "u'", "b'"])
                return turns
    elif corner == 3:
        if cube.net[5][2] == 1 and cube.net[3][0] == 2 and cube.net[3][7] == 6:
            return turns
        if (cube.net[0][3] == 1 and cube.net[2][5] == 2 and cube.net[2][6] == 6) or (cube.net[0][3] == 6 and cube.net[2][5] == 1 and cube.net[2][6] == 2) or (cube.net[0][3] == 2 and cube.net[2][5] == 6 and cube.net[2][6] == 1):
            uCount = 3
        elif (cube.net[1][3] == 1 and cube.net[2][3] == 2 and cube.net[2][4] == 6) or (cube.net[1][3] == 6 and cube.net[2][3] == 1 and cube.net[2][4] == 2) or (cube.net[1][3] == 2 and cube.net[2][3] == 6 and cube.net[2][4] == 1):
            uCount = 2
        elif (cube.net[1][2] == 1 and cube.net[2][1] == 2 and cube.net[2][2] == 6) or (cube.net[1][2] == 6 and cube.net[2][1] == 1 and cube.net[2][2] == 2) or (cube.net[1][2] == 2 and cube.net[2][1] == 6 and cube.net[2][2] == 1):
            uCount = 1
        for i in range(uCount):
            cube.performTurns(['u'])
            turns.append('u')
        count = 0
        tmp = Cube.cube(2)
        tmp.net = np.copy(cube.net)
        while True:
            count += 1
            tmp.performTurns(["l", "u", "l'", "u'"])
            if tmp.net[5][2] == 1:
                if count <= 3:
                    for i in range(count):
                        turns.extend(["l", "u", "l'", "u'"])
                        cube.performTurns(["l", "u", "l'", "u'"])
                else:
                    for i in range(6-count):
                        turns.extend(["u", "l", "u'", "l'"])
                        cube.performTurns(["u", "l", "u'", "l'"])
                return turns

def oll2x2(cube):
    turns = []
    while True:
        if cube.net[0][2] == 4 and cube.net[0][3] == 4 and cube.net[1][2] == 4 and cube.net[1][3] == 4:
            return turns
        # U
        if cube.net[0][3] == 4 and cube.net[1][3] == 4 and cube.net[2][0] == 4 and cube.net[2][1] == 4:
            turns.extend(["f", "r", "u", "r'", "u'", "f'"])
            cube.performTurns(["f", "r", "u", "r'", "u'", "f'"])
            break
        # T
        elif cube.net[0][3] == 4 and cube.net[1][3] == 4 and cube.net[2][2] == 4 and cube.net[2][7] == 4:
            turns.extend(["r", "u", "r'", "u'", "r'", "f", "r", "f'"])
            cube.performTurns(["r", "u", "r'", "u'", "r'", "f", "r", "f'"])
            break
        # L
        elif cube.net[0][2] == 4 and cube.net[1][3] == 4 and cube.net[2][5] == 4 and cube.net[2][2] == 4:
            turns.extend(["f", "r", "u'", "r'", "u'", "r", "u", "r'", "f'"])
            cube.performTurns(["f", "r", "u'", "r'", "u'", "r", "u", "r'", "f'"])
            break
        # S
        elif cube.net[1][2] == 4 and cube.net[2][3] == 4 and cube.net[2][5] == 4 and cube.net[2][7] == 4:
            turns.extend(["r", "u", "r'", "u", "r", "u", "u", "r'"])
            cube.performTurns(["r", "u", "r'", "u", "r", "u", "u", "r'"])
            break
        # As
        elif cube.net[0][3] == 4 and cube.net[2][0] == 4 and cube.net[2][2] == 4 and cube.net[2][4] == 4:
            turns.extend(["r", "u", "u", "r'", "u'", "r", "u'", "r'"])
            cube.performTurns(["r", "u", "u", "r'", "u'", "r", "u'", "r'"])
            break
        # Pi
        elif cube.net[2][0] == 4 and cube.net[2][1] == 4 and cube.net[2][3] == 4 and cube.net[2][6] == 4:
            turns.extend(["f", "r", "u", "r'", "u'", "r", "u", "r'", "u'", "f'"])
            cube.performTurns(["f", "r", "u", "r'", "u'", "r", "u", "r'", "u'", "f'"])
            break
        # H
        elif cube.net[2][2] == 4 and cube.net[2][3] == 4 and cube.net[2][6] == 4 and cube.net[2][7] == 4:
            turns.extend(["r", "r", "u", "u", "r", "u", "u", "r", "r"])
            cube.performTurns(["r", "r", "u", "u", "r", "u", "u", "r", "r"])
            break
        else:
            cube.performTurns(['u'])
            turns.append('u')
    return turns

def pll2x2(cube):
    alg = ["R", "B'", "R", "F", "F", "R'", "B", "R", "F", "F", "R", "R"]
    turns = []
    one = False
    if cube.net[2][0] == cube.net[2][1]:
        one = True
    two = False
    if cube.net[2][2] == cube.net[2][3]:
        two = True
    three = False
    if cube.net[2][4] == cube.net[2][5]:
        three = True
    four = False
    if cube.net[2][6] == cube.net[2][7]:
        four = True
    sides = [one, two, three, four]
    count = 0
    for i in sides:
        if i:
            count += 1
    if count == 4:
        while True:
            if cube.checkSolved():
                return turns
            else:
                turns.append("u")
                cube.performTurns(["u"])
    elif count == 0:
        alg = ["f", "r", "u'", "r'", "u'", "r", "u", "r'", "f'", "r", "u", "r'", "u'", "r'", "f", "r", "f'"]
        while True:
            if cube.net[1][2] == 4 and cube.net[2][1] == 2 and cube.net[2][2] == 3:
                turns.extend(alg)
                cube.performTurns(alg)
                return turns
            else:
                cube.performTurns(['u'])
                turns.append('u')
        while True:
            if cube.checkSolved():
                return turns
            else:
                turns.append("u")
                cube.performTurns(["u"])
    elif count == 1:
        uCount = 0
        if one:
            uCount = 3
        elif three:
            uCount = 1
        elif four:
            uCount = 2
        for i in range(uCount):
            turns.append("u")
            cube.performTurns(["u"])
        turns.extend(alg)
        cube.performTurns(alg)
        while True:
            if cube.checkSolved():
                return turns
            else:
                turns.append("u")
                cube.performTurns(["u"])

c = Cube.cube(2)
scramble = c.scramble(10)
print('Scramble: ', end='')
for i in scramble:
    print(i.upper(), end=' ')
print()
solve(c, True, True)

# numSolves = 1000
# c = Cube.cube(2)
# speed = 0
# solves = np.zeros(numSolves)
# for i in range(numSolves):
#     t0  = time.time()
#     print(100*'\b' + 'Solving cube ' + str(i) + ' / ' + str(numSolves) + ', ' + str(round(int(numSolves-i)*speed/60, 2)) +  ' minutes remaining ', end='')
#     scramble = c.scramble(10)
#     solveMoves = solve(c)
#     t1 = time.time()
#     speed = t1-t0
#     if solveMoves == 'failed':
#         print('Solve ' + str(i) + ' failed')
#         for i in scramble:
#             print(i, end=' ')
#     else:
#         solves[i] = solveMoves
#     time.sleep(0.01)
# print(100*'\n')
# plt.xlim([min(solves)-5, max(solves)+5])
# plt.hist(solves, bins=np.arange(0, max(solves)), alpha=0.5)
# plt.xlabel('Number of moves to solve')
# plt.ylabel('Frequency')
# plt.title('Moves to Solve ' + str(numSolves) + ' Cubes')
# plt.show()
# print('Max: ' + str(int(max(solves))))
# print('Min: ' + str(int(min(solves))))
# print('Mean: ' + str(sum(solves)/float(len(solves))))
# print("Stdev: " + str(statistics.stdev(solves)))