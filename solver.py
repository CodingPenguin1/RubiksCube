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
    if printNet:
        tc.printNet()
        print()
    tc.net = scrambledCube.net
    if printNet:
        tc.printNet()
        print()
    turns = []
    if tc.size == 2:
        # First layer
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

    elif tc.size == 3:
        # First layer edges
        turns.extend(solve3x3FirstLayerEdges(tc))
        # F2L
        turns.extend(solve3x3F2L(tc))

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
        print('\nSolution:')
        for i in turns:
            print(i.upper(), end=' ')
        print()
    if not tc.checkSolved():
        return 'failed'
    return(turns)


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

def find3x3Edge(cube, primCol, secCol):
    # Returns: Tuple (location, orientation)
    if cube.net[6][4] == primCol and cube.net[5][4] == secCol:
        return (0, 0)
    elif cube.net[6][4] == secCol and cube.net[5][4] == primCol:
        return (0, 1)
    elif cube.net[7][5] == primCol and cube.net[5][7] == secCol:
        return (1, 0)
    elif cube.net[7][5] == secCol and cube.net[5][7] == primCol:
        return (1, 1)
    elif cube.net[8][4] == primCol and cube.net[5][10] == secCol:
        return (2, 0)
    elif cube.net[8][4] == secCol and cube.net[5][10] == primCol:
        return (2, 1)
    elif cube.net[7][3] == primCol and cube.net[5][1] == secCol:
        return (3, 0)
    elif cube.net[7][3] == secCol and cube.net[5][1] == primCol:
        return (3, 1)
    elif cube.net[4][6] == primCol and cube.net[4][5] == secCol:
        return (4, 0)
    elif cube.net[4][6] == secCol and cube.net[4][5] == primCol:
        return (4, 1)
    elif cube.net[4][9] == primCol and cube.net[4][8] == secCol:
        return (5, 0)
    elif cube.net[4][9] == secCol and cube.net[4][8] == primCol:
        return (5, 1)
    elif cube.net[4][0] == primCol and cube.net[4][11] == secCol:
        return (6, 0)
    elif cube.net[4][0] == secCol and cube.net[4][11] == primCol:
        return (6, 1)
    elif cube.net[4][3] == primCol and cube.net[4][2] == secCol:
        return (7, 0)
    elif cube.net[4][3] == secCol and cube.net[4][2] == primCol:
        return (7, 1)
    elif cube.net[2][4] == primCol and cube.net[3][4] == secCol:
        return (8, 0)
    elif cube.net[2][4] == secCol and cube.net[3][4] == primCol:
        return (8, 1)
    elif cube.net[1][5] == primCol and cube.net[3][7] == secCol:
        return (9, 0)
    elif cube.net[1][5] == secCol and cube.net[3][7] == primCol:
        return (9, 1)
    elif cube.net[0][4] == primCol and cube.net[3][10] == secCol:
        return (10, 0)
    elif cube.net[0][4] == secCol and cube.net[3][10] == primCol:
        return (10, 1)
    elif cube.net[1][3] == primCol and cube.net[3][1] == secCol:
        return (11, 0)
    elif cube.net[1][3] == secCol and cube.net[3][1] == primCol:
        return (11, 1)

def solve3x3Edge(cube, edgeIndex):
    # 0 - W/R
    # 1 - W/G
    # 2 - W/O
    # 3 - W/B
    turns = []
    if edgeIndex == 0:
        primCol = 1
        secCol = 3
        if find3x3Edge(cube, primCol, secCol) == (0, 0):
            return turns
        elif find3x3Edge(cube, primCol, secCol) == (0, 1):
            turns = ["f'", "r'", "d'"]
        elif find3x3Edge(cube, primCol, secCol) == (1, 0):
            turns = ["d'"]
        elif find3x3Edge(cube, primCol, secCol) == (1, 1):
            turns = ["r", "f"]
        elif find3x3Edge(cube, primCol, secCol) == (2, 0):
            turns = ["d'", "d'"]
        elif find3x3Edge(cube, primCol, secCol) == (2, 1):
            turns = ["b", "r", "d'"]
        elif find3x3Edge(cube, primCol, secCol) == (3, 0):
            turns = ["d"]
        elif find3x3Edge(cube, primCol, secCol) == (3, 1):
            turns = ["l'", "f'"]
        elif find3x3Edge(cube, primCol, secCol) == (4, 0):
            turns = ["f"]
        elif find3x3Edge(cube, primCol, secCol) == (4, 1):
            turns = ["r'", "d'"]
        elif find3x3Edge(cube, primCol, secCol) == (5, 0):
            turns = ["r", "d'"]
        elif find3x3Edge(cube, primCol, secCol) == (5, 1):
            turns = ["b'", "d", "d"]
        elif find3x3Edge(cube, primCol, secCol) == (6, 0):
            turns = ["b", "d", "d"]
        elif find3x3Edge(cube, primCol, secCol) == (6, 1):
            turns = ["l'", "d"]
        elif find3x3Edge(cube, primCol, secCol) == (7, 0):
            turns = ["l", "d"]
        elif find3x3Edge(cube, primCol, secCol) == (7, 1):
            turns = ["f'"]
        elif find3x3Edge(cube, primCol, secCol) == (8, 0):
            turns = ["f", "f"]
        elif find3x3Edge(cube, primCol, secCol) == (8, 1):
            turns = ["u'", "r'", "f"]
        elif find3x3Edge(cube, primCol, secCol) == (9, 0):
            turns = ["u", "f", "f"]
        elif find3x3Edge(cube, primCol, secCol) == (9, 1):
            turns = ["r'", "f"]
        elif find3x3Edge(cube, primCol, secCol) == (10, 0):
            turns = ["u", "u", "f", "f"]
        elif find3x3Edge(cube, primCol, secCol) == (10, 1):
            turns = ["u", "r'", "f"]
        elif find3x3Edge(cube, primCol, secCol) == (11, 0):
            turns = ["u'", "f", "f"]
        elif find3x3Edge(cube, primCol, secCol) == (11, 1):
            turns = ["l", "f'"]
    elif edgeIndex == 1:
        primCol = 1
        secCol = 5
        if find3x3Edge(cube, primCol, secCol) == (1, 0):
            return turns
        elif find3x3Edge(cube, primCol, secCol) == (1, 1):
            turns = ["r'", "d", "b'", "d'"]
        elif find3x3Edge(cube, primCol, secCol) == (2, 0):
            turns = ["d'", "r", "d", "r'"]
        elif find3x3Edge(cube, primCol, secCol) == (2, 1):
            turns = ["b", "r"]
        elif find3x3Edge(cube, primCol, secCol) == (3, 0):
            turns = ["f", "d", "d", "f'"]
        elif find3x3Edge(cube, primCol, secCol) == (3, 1):
            turns = ["l", "d", "b", "d'"]
        elif find3x3Edge(cube, primCol, secCol) == (4, 0):
            turns = ["d'", "f", "d"]
        elif find3x3Edge(cube, primCol, secCol) == (4, 1):
            turns = ["r'"]
        elif find3x3Edge(cube, primCol, secCol) == (5, 0):
            turns = ["r"]
        elif find3x3Edge(cube, primCol, secCol) == (5, 1):
            turns = ["b", "u", "r", "r"]
        elif find3x3Edge(cube, primCol, secCol) == (6, 0):
            turns = ["d", "b", "d'"]
        elif find3x3Edge(cube, primCol, secCol) == (6, 1):
            turns = ["b", "b", "r"]
        elif find3x3Edge(cube, primCol, secCol) == (7, 0):
            turns = ["d", "d", "l", "d", "d"]
        elif find3x3Edge(cube, primCol, secCol) == (7, 1):
            turns = ["f'", "d", "f"]
        elif find3x3Edge(cube, primCol, secCol) == (8, 0):
            turns = ["u'", "r", "r"]
        elif find3x3Edge(cube, primCol, secCol) == (8, 1):
            turns = ["f", "r'", "f'"]
        elif find3x3Edge(cube, primCol, secCol) == (9, 0):
            turns = ["r", "r"]
        elif find3x3Edge(cube, primCol, secCol) == (9, 1):
            turns = ["u", "f", "r'", "f'"]
        elif find3x3Edge(cube, primCol, secCol) == (10, 0):
            turns = ["u", "r", "r"]
        elif find3x3Edge(cube, primCol, secCol) == (10, 1):
            turns = ["b'", "r"]
        elif find3x3Edge(cube, primCol, secCol) == (11, 0):
            turns = ["u", "u", "r", "r"]
        elif find3x3Edge(cube, primCol, secCol) == (11, 1):
            turns = ["u'", "f", "r'", "f'"]
    elif edgeIndex == 2:
        primCol = 1
        secCol = 6
        if find3x3Edge(cube, primCol, secCol) == (2, 0):
            return turns
        elif find3x3Edge(cube, primCol, secCol) == (2, 1):
            turns = ["b", "d'", "r", "d"]
        elif find3x3Edge(cube, primCol, secCol) == (3, 0):
            turns = ["d'", "b", "d", "b'"]
        elif find3x3Edge(cube, primCol, secCol) == (3, 1):
            turns = ["l", "b"]
        elif find3x3Edge(cube, primCol, secCol) == (4, 0):
            turns = ["r", "r", "b'", "r", "r"]
        elif find3x3Edge(cube, primCol, secCol) == (4, 1):
            turns = ["d'", "r'", "d"]
        elif find3x3Edge(cube, primCol, secCol) == (5, 0):
            turns = ["d'", "r", "d"]
        elif find3x3Edge(cube, primCol, secCol) == (5, 1):
            turns = ["b'"]
        elif find3x3Edge(cube, primCol, secCol) == (6, 0):
            turns = ["b"]
        elif find3x3Edge(cube, primCol, secCol) == (6, 1):
            turns = ["d", "l'", "d'"]
        elif find3x3Edge(cube, primCol, secCol) == (7, 0):
            turns = ["d", "l", "d'"]
        elif find3x3Edge(cube, primCol, secCol) == (7, 1):
            turns = ["l", "l", "b"]
        elif find3x3Edge(cube, primCol, secCol) == (8, 0):
            turns = ["u", "u", "b", "b"]
        elif find3x3Edge(cube, primCol, secCol) == (8, 1):
            turns = ["u'", "r", "b'", "r'"]
        elif find3x3Edge(cube, primCol, secCol) == (9, 0):
            turns = ["u'", "b", "b"]
        elif find3x3Edge(cube, primCol, secCol) == (9, 1):
            turns = ["r", "b'", "r'"]
        elif find3x3Edge(cube, primCol, secCol) == (10, 0):
            turns = ["b", "b"]
        elif find3x3Edge(cube, primCol, secCol) == (10, 1):
            turns = ["u", "r", "b'", "r'"]
        elif find3x3Edge(cube, primCol, secCol) == (11, 0):
            turns = ["u", "b", "b"]
        elif find3x3Edge(cube, primCol, secCol) == (11, 1):
            turns = ["l'", "b"]
    elif edgeIndex == 3:
        primCol = 1
        secCol = 2
        if find3x3Edge(cube, primCol, secCol) == (3, 0):
            return turns
        elif find3x3Edge(cube, primCol, secCol) == (3, 1):
            turns = ["l'", "d", "f'", "d'"]
        elif find3x3Edge(cube, primCol, secCol) == (4, 0):
            turns = ["d", "f", "d'"]
        elif find3x3Edge(cube, primCol, secCol) == (4, 1):
            turns = ["d", "d", "r'", "d", "d"]
        elif find3x3Edge(cube, primCol, secCol) == (5, 0):
            turns = ["d", "d", "r", "d", "d"]
        elif find3x3Edge(cube, primCol, secCol) == (5, 1):
            turns = ["d'", "b'", "d"]
        elif find3x3Edge(cube, primCol, secCol) == (6, 0):
            turns = ["d'", "b", "d"]
        elif find3x3Edge(cube, primCol, secCol) == (6, 1):
            turns = ["l'"]
        elif find3x3Edge(cube, primCol, secCol) == (7, 0):
            turns = ["l"]
        elif find3x3Edge(cube, primCol, secCol) == (7, 1):
            turns = ["d", "f'", "d'"]
        elif find3x3Edge(cube, primCol, secCol) == (8, 0):
            turns = ["u", "l", "l"]
        elif find3x3Edge(cube, primCol, secCol) == (8, 1):
            turns = ["f'", "l", "f"]
        elif find3x3Edge(cube, primCol, secCol) == (9, 0):
            turns = ["u", "u", "l", "l"]
        elif find3x3Edge(cube, primCol, secCol) == (9, 1):
            turns = ["u", "f'", "l", "f"]
        elif find3x3Edge(cube, primCol, secCol) == (10, 0):
            turns = ["u'", "l", "l"]
        elif find3x3Edge(cube, primCol, secCol) == (10, 1):
            turns = ["b", "l'", "b'"]
        elif find3x3Edge(cube, primCol, secCol) == (11, 0):
            turns = ["l", "l"]
        elif find3x3Edge(cube, primCol, secCol) == (11, 1):
            turns = ["u'", "f'", "l", "f"]
    cube.performTurns(turns)
    return turns

def solve3x3FirstLayerEdges(cube):
    # 0 - W/R
    # 1 - W/G
    # 2 - W/O
    # 3 - W/B
    turns = []
    # White/Red edge
    if cube.net[6][4] != 1 or cube.net[5][4] != 3:
        turns.extend(solve3x3Edge(cube, 0))
    # White/Green edge
    if cube.net[7][5] != 1 or cube.net[4][7] != 5:
        turns.extend(solve3x3Edge(cube, 1))
    # White/Orange edge
    if cube.net[8][4] != 1 or cube.net[4][10] != 6:
        turns.extend(solve3x3Edge(cube, 2))
    # White/Blue edge
    if cube.net[7][3] != 1 or cube.net[5][1] != 2:
        turns.extend(solve3x3Edge(cube, 3))
    return turns

def solve3x3F2LPair(cube, pairIndex):
    turns = []
    uCount = 0
    if pairIndex == 0:
        primCol = 5
        secCol = 3
        while True:
            # 1: Easy Cases
            if cube.net[3][6] == 1 and cube.net[3][5] == 3 and cube.net[2][5] == 5 and find3x3Edge(cube, primCol, secCol) == (10, 1):
                turns = ["r", "u", "r'"]
                break
            elif cube.net[3][6] == 1 and cube.net[3][5] == 3 and cube.net[2][5] == 5 and find3x3Edge(cube, primCol, secCol) == (8, 0):
                turns = ["u'", "f'", "u", "f"]
                break
            elif cube.net[3][6] == 5 and cube.net[3][5] == 1 and cube.net[2][5] == 3 and find3x3Edge(cube, primCol, secCol) == (11, 0):
                turns = ["f'", "u'", "f"]
                break
            elif cube.net[3][6] == 5 and cube.net[3][5] == 1 and cube.net[2][5] == 3 and find3x3Edge(cube, primCol, secCol) == (9, 1):
                turns = ["u", "r", "u'", "r'"]
                break
            # 2: Corner in bottom, edge in top layer
            elif cube.net[6][5] == 1 and cube.net[5][5] == 3 and cube.net[5][6] == 5 and find3x3Edge(cube, primCol, secCol) == (8, 0):
                turns = ["u", "r", "u'", "r'", "u'", "f'", "u", "f"]
                break
            elif cube.net[6][5] == 3 and cube.net[5][5] == 5 and cube.net[5][6] == 1 and find3x3Edge(cube, primCol, secCol) == (8, 0):
                turns = ["f'", "u", "f", "u'", "f'", "u", "f"]
                break
            elif cube.net[6][5] == 5 and cube.net[5][5] == 1 and cube.net[5][6] == 3 and find3x3Edge(cube, primCol, secCol) == (8, 0):
                turns = ["f'", "u'", "f", "u", "f'", "u'", "f"]
                break
            elif cube.net[6][5] == 1 and cube.net[5][5] == 3 and cube.net[5][6] == 5 and find3x3Edge(cube, primCol, secCol) == (9, 1):
                turns = ["u'", "f'", "u", "f", "u", "r", "u'", "r'"]
                break
            elif cube.net[6][5] == 3 and cube.net[5][5] == 5 and cube.net[5][6] == 1 and find3x3Edge(cube, primCol, secCol) == (9, 1):
                turns = ["r", "u", "r'", "u'", "r", "u", "r'"]
                break
            elif cube.net[6][5] == 5 and cube.net[5][5] == 1 and cube.net[5][6] == 3 and find3x3Edge(cube, primCol, secCol) == (9, 1):
                turns = ["r", "u'", "r'", "u", "r", "u'", "r'"]
                break
            # 3: Corner in top, edge in middle
            elif cube.net[2][5] == 1 and cube.net[3][5] == 5 and cube.net[3][6] == 3 and find3x3Edge(cube, primCol, secCol) == (4, 0):
                turns = ["r", "u", "r'", "u'", "r", "u", "r'", "u'", "r", "u", "r'"]
                break
            elif cube.net[2][5] == 5 and cube.net[3][5] == 3 and cube.net[3][6] == 1 and find3x3Edge(cube, primCol, secCol) == (4, 0):
                turns = ["u", "f'", "u", "f", "u", "f'", "u", "u", "f"]
                break
            elif cube.net[2][5] == 3 and cube.net[3][5] == 1 and cube.net[3][6] == 5 and find3x3Edge(cube, primCol, secCol) == (4, 0):
                turns = ["u'", "r", "u'", "r'", "u'", "r", "u", "u", "r'"]
                break
            elif cube.net[2][5] == 1 and cube.net[3][5] == 5 and cube.net[3][6] == 3 and find3x3Edge(cube, primCol, secCol) == (4, 1):
                turns = ["r", "u'", "r'", "f'", "u", "u", "f"]
                break
            elif cube.net[2][5] == 5 and cube.net[3][5] == 3 and cube.net[3][6] == 1 and find3x3Edge(cube, primCol, secCol) == (4, 1):
                turns = ["u", "f'", "u'", "f", "u'", "r", "u", "r'"]
                break
            elif cube.net[2][5] == 3 and cube.net[3][5] == 1 and cube.net[3][6] == 5 and find3x3Edge(cube, primCol, secCol) == (4, 1):
                turns = ["u'", "r", "u", "r'", "u", "f'", "u'", "f"]
                break
            uCount += 1
            cube.performTurns(["u"])
    cube.performTurns(turns)
    for i in range(uCount):
        turns.insert(0, "u")
    return turns

def solve3x3F2L(cube):
    # 0 - R/G
    # 1 - G/O
    # 2 - O/B
    # 3 - B/R
    turns = []
    if cube.net[6][5] != 1 or cube.net[5][5] != 3 or cube.net[5][6] != 5 or cube.net[4][5] != 3 or cube.net[4][6] != 5:
        turns.extend(solve3x3F2LPair(cube, 0))
    return turns

numSolves = 1
c = Cube.cube(3)
scrambleMoves = 10

if numSolves == 1:
    scramble = c.scramble(scrambleMoves)
    # scramble = ["f'", "u", "f", "u'", "r", "u'", "r'", "u"]
    # c.performTurns(scramble)
    print('Scramble: ', end='')
    for i in scramble:
        print(i.upper(), end=' ')
    print()
    solve(c, True, True)
else:
    speed = [0]
    solves = np.zeros(numSolves)
    for i in range(numSolves):
        t0  = time.time()
        print(100*'\b' + 'Solving cube ' + str(i) + ' / ' + str(numSolves) + ', ' + str(round(int(numSolves-i)*(sum(speed)/len(speed))/60, 2)) +  ' minutes remaining ', end='')
        scramble = c.scramble(scrambleMoves)
        solveMoves = solve(c)
        t1 = time.time()
        speed.append(t1-t0)
        if solveMoves == 'failed':
            print('Solve ' + str(i) + ' failed')
            for i in scramble:
                print(i, end=' ')
        else:
            solves[i] = len(solveMoves)
        time.sleep(0.01)
    print(100*'\n')
    plt.xlim([min(solves)-5, max(solves)+5])
    plt.hist(solves, bins=np.arange(0, max(solves)), alpha=0.5)
    plt.xlabel('Number of moves to solve')
    plt.ylabel('Frequency')
    plt.title('Moves to Solve ' + str(numSolves) + ' Cubes')
    plt.show()
    print('Max: ' + str(int(max(solves))))
    print('Min: ' + str(int(min(solves))))
    print('Mean: ' + str(sum(solves)/float(len(solves))))
    print("Stdev: " + str(round(statistics.stdev(solves), 4)))