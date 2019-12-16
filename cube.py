#!/usr/bin/env python

import numpy as np


class Cube:
    def __init__(self, size):
        # size (int) : cube will be of dimensions size x size x size
        # Make a net in the form of:
        #        5
        #    4 3 1 0
        #        2
        # Side 1 is considered the "front" and side 0 is considered the "top"
        self.size = size
        self.net = np.full((size*3, size*4), -1, dtype=np.int8)
        for row in range(size):
            for col in range(size*2, size*3):
                self.net[row][col] = 5
        for row in range(size, size*2):
            for col in range(size):
                self.net[row][col] = 4
            for col in range(size, size*2):
                self.net[row][col] = 3
            for col in range(size*2, size*3):
                self.net[row][col] = 1
            for col in range(size*3, size*4):
                self.net[row][col] = 0
        for row in range(size*2, size*3):
            for col in range(size*2, size*3):
                self.net[row][col] = 2

    def turn(self, side, direction, depth=0):
        # side (int) : side number to rotate
        # direction (int) : -1 or 1, -1 is ccw 1 is cw
        # depth (int) : how many layers into the cube to turn. 0 is outer layer and 1 is next layer in (outer layer is not rotated). depth should always be < size - 1

        # Top face (0)
        if side == 0:
            # U
            layer = np.append(self.net[:, size*3-1-depth], self.net[size:size*2, depth])
            if direction == 1:
                if depth == 0:
                    self.net[self.size*1: self.size*2, self.size*3: self.size*4] = np.rot90(self.net[self.size*1: self.size*2, self.size*3: self.size*4], k=3)
                layer = np.roll(layer, -3)
            # U'
            else:
                if depth == 0:
                    self.net[self.size*1: self.size*2, self.size*3: self.size*4] = np.rot90(self.net[self.size*1: self.size*2, self.size*3: self.size*4], k=1)
                layer = np.roll(layer, 3)
            self.net[:, size*3-1-depth] = layer[:size*3]
            self.net[size:size*2, depth] = layer[size*3:]

        # Front Face (1)
        if side == 1:
            # F
            layer = np.append(self.net[self.size-1-depth, self.size*2:self.size*3], [self.net[self.size:self.size*2, self.size*2-1-depth], self.net[self.size*2+depth, self.size*2:self.size*3], self.net[self.size:self.size*2, self.size*3+depth]])
            if direction == 1:
                if depth == 0:
                    self.net[self.size*1: self.size*2, self.size*2: self.size*3] = np.rot90(self.net[self.size*1: self.size*2, self.size*2: self.size*3], k=3)
                layer = np.roll(layer, -3)
            # F'
            else:
                if depth == 0:
                    self.net[self.size*1: self.size*2, self.size*2: self.size*3] = np.rot90(self.net[self.size*1: self.size*2, self.size*2: self.size*3], k=1)
                layer = np.roll(layer, 3)
            self.net[self.size-1-depth, self.size*2:self.size*3] = layer[:size]
            self.net[self.size:self.size*2, self.size*2-1-depth] = layer[size:size*2]
            self.net[self.size*2+depth, self.size*2:self.size*3] = layer[size*2:size*3]
            self.net[self.size:self.size*2, self.size*3+depth] = layer[size*3:]

        # Right Face (2)
        if side == 2:
            # R
            layer = self.net[size*2-1-depth, :]
            if direction == 1:
                if depth == 0:
                    self.net[self.size*2:, self.size*2: self.size*3] = np.rot90(self.net[self.size*2:, self.size*2: self.size*3], k=3)
                layer = np.roll(layer, 3)
            # R'
            else:
                if depth == 0:
                    self.net[self.size*2:, self.size*2: self.size*3] = np.rot90(self.net[self.size*2:, self.size*2: self.size*3], k=1)
                layer = np.roll(layer, -3)
            self.net[size*2-1-depth, :] = layer

        # Bottom (Down) Face (3)
        if side == 3:
            # D
            layer = np.append(self.net[:, self.size*2+depth], self.net[self.size:self.size*2, self.size-1-depth])
            if direction == 1:
                if depth == 0:
                    self.net[self.size:self.size*2, self.size:self.size*2] = np.rot90(self.net[self.size:self.size*2, self.size:self.size*2], k=3)
                layer = np.roll(layer, 3)
            # D'
            else:
                if depth == 0:
                    self.net[self.size:self.size*2:, self.size:self.size*2] = np.rot90(self.net[self.size:self.size*2, self.size:self.size*2], k=1)
                layer = np.roll(layer, -3)
            self.net[:, self.size*2+depth] = layer[:self.size*3]
            self.net[self.size:self.size*2, self.size-1-depth] = layer[self.size*3:]

        # Back Face (4)
        if side == 4:
            # B
            layer = np.append(self.net[self.size:self.size*2, self.size+depth], [self.net[depth, self.size*2:self.size*3], self.net[self.size:self.size*2, self.size*4-1-depth], self.net[self.size*3-1-depth, self.size*2:self.size*3]])
            if direction == 1:
                if depth == 0:
                    self.net[self.size:self.size*2, :self.size] = np.rot90(self.net[self.size:self.size*2, :self.size], k=3)
                layer = np.roll(layer, -3)
            # B'
            else:
                if depth == 0:
                    self.net[self.size:self.size*2:, :self.size] = np.rot90(self.net[self.size:self.size*2, :self.size], k=1)
                layer = np.roll(layer, 3)
            self.net[self.size:self.size*2, self.size+depth] = layer[:self.size]
            self.net[depth, self.size*2:self.size*3] = layer[self.size:self.size*2]
            self.net[self.size:self.size*2, self.size*4-1-depth] = layer[self.size*2:self.size*3]
            self.net[self.size*3-1-depth, self.size*2:self.size*3] = layer[self.size*3:]

        # Left Face (5)
        if side == 5:
            # L
            layer = self.net[self.size+depth]
            if direction == 1:
                if depth == 0:
                    self.net[:self.size, self.size*2:self.size*3] = np.rot90(self.net[:self.size, self.size*2:self.size*3], k=3)
                layer = np.roll(layer, -3)
            # L'
            else:
                if depth == 0:
                    self.net[:self.size:, self.size*2:self.size*3] = np.rot90(self.net[:self.size, self.size*2:self.size*3], k=1)
                layer = np.roll(layer, 3)
            self.net[self.size+depth] = layer


if __name__ == '__main__':
    size = 3
    cube = Cube(size)
    print(cube.net)
    print()
    cube.turn(5, 1, 1)
    print(cube.net)
