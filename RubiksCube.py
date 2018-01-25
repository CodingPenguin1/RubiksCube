#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Title: Rubiks Cube Simulator
# Author: Ryan Slater
# Date: 1/24/2018
# =============================================================================

import numpy as np

class colors():
    BLACK = '\033[30m'
    RED = '\033[31m'
    ORANGE = '\033[33m'
    BLUE = '\033[36m'
    GREEN = '\033[32m'
    WHITE = '\033[379m'
    YELLOW = '\033[37m'

    def getFaceColor(x):
        BLACK = '\033[30m'
        RED = '\033[31m'
        ORANGE = '\033[33m'
        BLUE = '\033[36m'
        GREEN = '\033[32m'
        WHITE = '\033[39m'
        YELLOW = '\033[37m'
        if x == 0:
            return BLACK
        elif x == 1:
            return WHITE
        elif x == 2:
            return BLUE
        elif x == 3:
            return RED
        elif x == 4:
            return YELLOW
        elif x == 5:
            return GREEN
        elif x == 6:
            return ORANGE

class cube():
    def __init__(self, size):
        self.size = size
        self.net = np.zeros((size*3, size*4), np.int32)
        for row in range(size, 2*size):
            for col in range(size, 2*size):
                self.net[row][col] = 1
                self.net[row-size][col] = 2
                self.net[row+size][col] = 5
                self.net[row][col+size] = 3
                self.net[row][col+2*size] = 4
                self.net[row][col-size] = 6
        self.solvedState = np.copy(self.net)

    def printNet(self):
        for row in range(3*self.size):
            for col in range(4*self.size):
                print(colors.getFaceColor(self.net[row][col]) + str(self.net[row][col]), end='  ')
            print()

    def rotateClockwise(self, face):
        original = np.copy(self.net)

        if face == 1:
            self.net[self.size][self.size] = original[2*self.size-1][self.size]
            self.net[2*self.size-1][self.size] = original[2*self.size-1][2*self.size-1]
            self.net[2*self.size-1][2*self.size-1] = original[self.size][2*self.size-1]
            self.net[self.size][2*self.size-1] = original[self.size][self.size]
            self.net[self.size][self.size+1] = original[self.size+1][self.size]
            self.net[self.size+1][2*self.size-1] = original[self.size][self.size+1]
            self.net[2*self.size-1][self.size+1] = original[self.size+1][2*self.size-1]
            self.net[self.size+1][self.size] = original[2*self.size-1][self.size+1]
            for i in range(self.size):
                self.net[self.size-1][self.size+i] = original[2*self.size-1-i][self.size-1]
                self.net[self.size+i][2*self.size] = original[self.size-1][self.size+i]
                self.net[2*self.size][2*self.size-1-i] = original[self.size+i][2*self.size]
                self.net[2*self.size-1-i][self.size-1] = original[2*self.size][2*self.size-1-i]

    def rotateFace(self, face, inverse=False):
        # TODO: make this work for size n cube
        self.rotateClockwise(face)
        if inverse:
            for i in range(2):
                self.rotateClockwise(face)

c = cube(3)
c.printNet()
c.rotateFace(1, True)
print()
c.printNet()
c.rotateFace(1)
print()
c.printNet()
print()

c = cube(4)
c.printNet()
c.rotateFace(1, True)
print()
c.printNet()
c.rotateFace(1)
print()
c.printNet()