#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Title: Cube Solver
# Author: Ryan Slater
# Date: 1/28/2017
# =============================================================================

import RubiksCube as cube
import time

def solve(scrambledCube, printNet=False):
    t0 = time.time()
    tc = cube.cube(int(len(scrambledCube.net)/3))
    tc.net = scrambledCube.net
    if printNet:
        tc.printNet()
        print()
        time.sleep(1)
    if tc.size == 2:
        # First layer
        turns = []
        turns.extend(solve2x2corner(tc, 0))
        turns.extend(solve2x2corner(tc, 1))
        turns.extend(solve2x2corner(tc, 2))
        turns.extend(solve2x2corner(tc, 3))

        # Finish
        if printNet:
            tc.printNet()
            print()
        t1 = time.time()
        turns = cleanSolution(turns)
        print('Solved first layer in ' + str(len(turns)) + ' moves in ' + str(round(t1-t0, 1)) + ' seconds (' + str(round(len(turns)/(t1-t0), 1)) + ' moves/second)')
        for i in turns:
            print(i, end=' ')

def areOpposites(x, y):
    if len(x) != len(y):
        if x[0] == y[0]:
            return True
    return False

def cleanSolution(turns):
    # Removes conecutive different direction turns on the same face (u, u' = /)
    stop = len(turns)
    i = 1
    while i < stop:
        x = turns[i-1]
        y = turns[i]
        if areOpposites(x, y):
            turns = turns[:i-1] + turns[i+1:]
            stop = len(turns)
            i = 0
        i += 1
    # TODO: convert three identical consecutive turns to one opposite turn (u, u, u = u'), also fix scramble to do the same
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
        if (cube.net[0][2] == 1 and cube.net[2][0] == 2 and cube.net[2][7] == 3) or (cube.net[0][2] == 3 and cube.net[2][0] == 1 and cube.net[2][7] == 2) or (cube.net[0][2] == 2 and cube.net[2][0] == 3 and cube.net[2][7] == 1):
            uCount = 3
        elif (cube.net[0][3] == 1 and cube.net[2][5] == 3 and cube.net[2][6] == 2) or (cube.net[0][3] == 2 and cube.net[2][5] == 1 and cube.net[2][6] == 3) or (cube.net[0][3] == 3 and cube.net[2][5] == 2 and cube.net[2][6] == 1):
            uCount = 2
        elif (cube.net[1][3] == 1 and cube.net[2][3] == 3 and cube.net[2][4] == 2) or (cube.net[1][3] == 2 and cube.net[2][3] == 1 and cube.net[2][4] == 3) or (cube.net[1][3] == 3 and cube.net[2][3] == 2 and cube.net[2][4] == 1):
            uCount = 1
        for i in range(uCount):
            cube.performTurns(['u'])
            turns.append('u')
        while True:
            cube.performTurns(["l'", "u'", 'l', 'u'])
            turns.extend(["l'", "u'", 'l', 'u'])
            if cube.net[4][2] == 1 and cube.net[3][1] == 2 and cube.net[3][2] == 3:
                return turns
    elif corner == 1:
        if (cube.net[0][2] == 1 and cube.net[2][0] == 3 and cube.net[2][7] == 5) or (cube.net[0][2] == 5 and cube.net[2][0] == 1 and cube.net[2][7] == 3) or (cube.net[0][2] == 3 and cube.net[2][0] == 5 and cube.net[2][7] == 1):
            uCount = 2
        elif (cube.net[0][3] == 1 and cube.net[2][5] == 5 and cube.net[2][6] == 3) or (cube.net[0][3] == 3 and cube.net[2][5] == 1 and cube.net[2][6] == 5) or (cube.net[0][3] == 5 and cube.net[2][5] == 3 and cube.net[2][6] == 1):
            uCount = 1
        elif (cube.net[1][2] == 1 and cube.net[2][1] == 5 and cube.net[2][2] == 3) or (cube.net[1][2] == 3 and cube.net[2][1] == 1 and cube.net[2][2] == 5) or (cube.net[1][2] == 5 and cube.net[2][1] == 3 and cube.net[2][2] == 1):
            uCount = 3
        for i in range(uCount):
            cube.performTurns(['u'])
            turns.append('u')
        while True:
            cube.performTurns(["r", "u", "r'", "u'"])
            turns.extend(["r", "u", "r'", "u'"])
            if cube.net[4][3] == 1 and cube.net[3][3] == 3 and cube.net[3][4] == 5:
                return turns
    elif corner == 2:
        if (cube.net[0][2] == 1 and cube.net[2][0] == 5 and cube.net[2][7] == 6) or (cube.net[0][2] == 6 and cube.net[2][0] == 1 and cube.net[2][7] == 5) or (cube.net[0][2] == 5 and cube.net[2][0] == 6 and cube.net[2][7] == 1):
            uCount = 1
        elif (cube.net[1][3] == 1 and cube.net[2][3] == 6 and cube.net[2][4] == 5) or (cube.net[1][3] == 5 and cube.net[2][3] == 1 and cube.net[2][4] == 6) or (cube.net[1][3] == 6 and cube.net[2][3] == 5 and cube.net[2][4] == 1):
            uCount = 3
        elif (cube.net[1][2] == 1 and cube.net[2][1] == 6 and cube.net[2][2] == 5) or (cube.net[1][2] == 5 and cube.net[2][1] == 1 and cube.net[2][2] == 6) or (cube.net[1][2] == 6 and cube.net[2][1] == 5 and cube.net[2][2] == 1):
            uCount = 2
        for i in range(uCount):
            cube.performTurns(['u'])
            turns.append('u')
        while True:
            cube.performTurns(["b", "u", "b'", "u'"])
            turns.extend(["b", "u", "b'", "u'"])
            if cube.net[5][3] == 1 and cube.net[3][5] == 5 and cube.net[3][6] == 6:
                return turns
    elif corner == 3:
        if (cube.net[0][3] == 1 and cube.net[2][5] == 2 and cube.net[2][6] == 6) or (cube.net[0][3] == 6 and cube.net[2][5] == 1 and cube.net[2][6] == 2) or (cube.net[0][3] == 2 and cube.net[2][5] == 6 and cube.net[2][6] == 1):
            uCount = 3
        elif (cube.net[1][3] == 1 and cube.net[2][3] == 2 and cube.net[2][4] == 6) or (cube.net[1][3] == 6 and cube.net[2][3] == 1 and cube.net[2][4] == 2) or (cube.net[1][3] == 2 and cube.net[2][3] == 6 and cube.net[2][4] == 1):
            uCount = 2
        elif (cube.net[1][2] == 1 and cube.net[2][1] == 2 and cube.net[2][2] == 6) or (cube.net[1][2] == 6 and cube.net[2][1] == 1 and cube.net[2][2] == 2) or (cube.net[1][2] == 2 and cube.net[2][1] == 6 and cube.net[2][2] == 1):
            uCount = 1
        for i in range(uCount):
            cube.performTurns(['u'])
            turns.append('u')
        while True:
            cube.performTurns(["l", "u", "l'", "u'"])
            turns.extend(["l", "u", "l'", "u'"])
            if cube.net[5][2] == 1:
                return turns


c = cube.cube(2)
scramble = c.scramble(50)
print('Scramble: ', end='')
for i in scramble:
    print(i, end=' ')
print()
solve(c, True)