#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Title: Rubiks Cube Simulator
# Author: Ryan Slater
# Date: 1/24/2018
# =============================================================================

import numpy as np
import random as rand

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
        else:
            return WHITE

class cube():
    def __init__(self, size):
        self.size = size
        self.net = np.zeros((size*3, size*4), np.int32)
        for row in range(size, 2*size):
            for col in range(size, 2*size):
                self.net[row][col] = 3
                self.net[row-size][col] = 4
                self.net[row+size][col] = 1
                self.net[row][col+size] = 5
                self.net[row][col+2*size] = 6
                self.net[row][col-size] = 2
        self.solvedState = np.copy(self.net)

    def checkSolved(self):
        one = np.zeros((self.size, self.size), np.int32)
        two = np.zeros((self.size, self.size), np.int32)
        three = np.zeros((self.size, self.size), np.int32)
        four = np.zeros((self.size, self.size), np.int32)
        five = np.zeros((self.size, self.size), np.int32)
        six = np.zeros((self.size, self.size), np.int32)
        for row in range(self.size):
            for col in range(self.size):
                one[row][col] = self.net[2*self.size+row][self.size+col]
                two[row][col] = self.net[self.size+row][col]
                three[row][col] = self.net[self.size+row][self.size+col]
                four[row][col] = self.net[row][self.size+col]
                five[row][col] = self.net[self.size+row][2*self.size+col]
                six[row][col] = self.net[self.size+row][3*self.size+col]
        for row in range(self.size):
            for col in range(self.size):
                if one[row][col] != 1 or two[row][col] != 2 or three[row][col] != 3 or four[row][col] != 4 or five[row][col] != 5 or six[row][col] != 6:
                    return False
        return True

    def printNet(self):
        for row in range(3*self.size):
            for col in range(4*self.size):
                print(colors.getFaceColor(self.net[row][col]) + str(self.net[row][col]) + colors.getFaceColor(9), end='  ')
            print()

    def rotateLayer(self, face, index, prime=False):
        if face == 'U' or face == 'u' or face =='D' or face == 'd':
            rotCount = 3
            if prime:
                rotCount = 1
            if face == 'D' or face == 'd':
                rotCount = 1
                if prime:
                    rotCount = 3
                index = self.size-1-index
            for i in range(rotCount):
                # Rotate Layer Horizontally
                original = np.copy(self.net)
                for i in range(self.size):
                    self.net[self.size+index][self.size+i] = original[self.size+index][i]
                    self.net[self.size+index][2*self.size+i] = original[self.size+index][self.size+i]
                    self.net[self.size+index][3*self.size+i] = original[self.size+index][2*self.size+i]
                    self.net[self.size+index][i] = original[self.size+index][3*self.size+i]
                # Rotate Adjacent Face
                if index == 0:
                    tmpFace = np.zeros((self.size, self.size), np.int32)
                    for row in range(self.size):
                        for col in range(self.size, 2*self.size):
                            tmpFace[row][col-self.size] = original[row][col]
                    tmpFace = np.rot90(tmpFace)
                    for row in range(self.size):
                        for col in range(self.size):
                            self.net[row][self.size+col] = tmpFace[row][col]
                if index == self.size-1:
                    tmpFace = np.zeros((self.size, self.size), np.int32)
                    for row in range(2*self.size, 3*self.size):
                        for col in range(self.size, 2*self.size):
                            tmpFace[row-2*self.size][col-self.size] = original[row][col]
                    tmpFace = np.rot90(tmpFace, 3)
                    for row in range(self.size):
                        for col in range(self.size):
                            self.net[2*self.size+row][self.size+col] = tmpFace[row][col]
        elif face == 'R' or face == 'r' or face == 'L' or face == 'l':
            rotCount = 1
            if prime:
                rotCount = 3
            if face == 'L' or face == 'l':
                rotCount = 3
                if prime:
                    rotCount = 1
                index = self.size-1-index
            for i in range(rotCount):
                # Rotate Layer Horizontally
                original = np.copy(self.net)
                for i in range(self.size):
                    self.net[2*self.size-i-1][2*self.size-1-index] = original[3*self.size-1-i][2*self.size-1-index]
                    self.net[self.size-i-1][2*self.size-1-index] = original[2*self.size-1-i][2*self.size-1-index]
                    self.net[self.size+i][3*self.size+index] = original[self.size-1-i][2*self.size-1-index]
                    self.net[3*self.size-1-i][2*self.size-1-index] = original[self.size+i][3*self.size+index]
                # Rotate Adjacent Face
                if index == 0:
                    tmpFace = np.zeros((self.size, self.size), np.int32)
                    for row in range(self.size, 2*self.size):
                        for col in range(2*self.size, 3*self.size):
                            tmpFace[row-self.size][col-2*self.size] = original[row][col]
                    tmpFace = np.rot90(tmpFace, 3)
                    for row in range(self.size):
                        for col in range(self.size):
                            self.net[row-2*self.size][col-2*self.size] = tmpFace[row][col]
                if index == self.size-1:
                    tmpFace = np.zeros((self.size, self.size), np.int32)
                    for row in range(self.size, 2*self.size):
                        for col in range(self.size):
                            tmpFace[row-self.size][col] = original[row][col]
                    tmpFace = np.rot90(tmpFace)
                    for row in range(self.size):
                        for col in range(self.size):
                            self.net[row+self.size][col] = tmpFace[row][col]
        elif face == 'F' or face == 'f' or face == 'B' or face == 'b':
            rotCount = 1
            if prime:
                rotCount = 3
            if face == 'B' or face == 'b':
                rotCount = 3
                if prime:
                    rotCount = 1
                index = self.size-1-index
            for i in range(rotCount):
                # Rotate Layer Horizontally
                original = np.copy(self.net)
                for i in range(self.size):
                    self.net[self.size-1-index][self.size+i] = original[2*self.size-1-i][self.size-1-index]
                    self.net[self.size+i][2*self.size+index] = original[self.size-1-index][self.size+i]
                    self.net[2*self.size+index][2*self.size-1-i] = original[self.size+i][2*self.size+index]
                    self.net[2*self.size-1-i][self.size-1-index] = original[2*self.size+index][2*self.size-1-i]
                # Rotate Adjacent Face
                if index == 0:
                    tmpFace = np.zeros((self.size, self.size), np.int32)
                    for row in range(self.size, 2*self.size):
                        for col in range(self.size, 2*self.size):
                            tmpFace[row-self.size][col-self.size] = original[row][col]
                    tmpFace = np.rot90(tmpFace, 3)
                    for row in range(self.size):
                        for col in range(self.size):
                            self.net[row+self.size][col+self.size] = tmpFace[row][col]
                if index == self.size-1:
                    tmpFace = np.zeros((self.size, self.size), np.int32)
                    for row in range(self.size, 2*self.size):
                        for col in range(3*self.size, 4*self.size):
                            tmpFace[row-self.size][col-3*self.size] = original[row][col]
                    tmpFace = np.rot90(tmpFace)
                    for row in range(self.size):
                        for col in range(self.size):
                            self.net[row+self.size][col+3*self.size] = tmpFace[row][col]

    def scramble(self, turns, printNet=False):
        moves = []
        if type(turns) == int:
            numMoves = turns
            turns = []
            for i in range(numMoves):
                move = self.getRandomMove()
                while i > 0:
                    prevMove = moves[len(moves)-1]
                    if len(prevMove) != len(move) and prevMove[0] == move[0] and prevMove[1] == move[1]:
                        move = self.getRandomMove()
                    else:
                        break
                moves.append(move)
            self.performTurns(moves)
            return moves
        else:
            self.performTurns(turns, printNet)
            return turns

    def getRandomMove(self):
        faces = ['u', 'd', 'r', 'l', 'f', 'b']
        directions = ["", "'"]
        return(faces[rand.randint(0, 5)] + str(rand.randint(0, int(self.size/2)-1)) + directions[rand.randint(0, 1)])

    def performTurns(self, turns, printNet=False):
        for i in turns:
            face = i[0]
            index = 0
            prime = False
            if len(i) > 1:
                if i[1] == "'":
                    prime = True
                elif i[1] in '0123456789':
                    index = int(i[1])
            if len(i) > 2:
                prime = True
            self.rotateLayer(face, index, prime)
            if printNet:
                rev = ''
                if prime:
                    rev = "'"
                print(face.upper() + str(index) + rev)
                self.printNet()
                print()