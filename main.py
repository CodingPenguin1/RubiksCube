#!/usr/bin/env python

import json
from time import time

import pygame
from pygame.locals import *

from cube import Cube


def text_objects(text, font, color=(0, 0, 0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None, fontSize=20):
    mouse = pygame.mouse.get_pos()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x, y, w, h))
        if pygame.mouse.get_pressed()[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(window, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", fontSize)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    window.blit(textSurf, textRect)


def switchViewMode():
    global changeViewmodeTimeout

    if time() - changeViewmodeTimeout > .5:
        if config['viewMode'] == 'net':
            config['viewMode'] = 'cube'
        else:
            config['viewMode'] = 'net'
        changeViewmodeTimeout = time()


def drawNet(cube):
    black = (0, 0, 0)
    squareSize = round(min(displayHeight, displayWidth) / 10.8 * (3 / cube.size))

    for row in range(cube.size*3):
        for col in range(cube.size*4):
            draw = False
            if row < cube.size:
                if col >= 2*cube.size and col < 3*cube.size:
                    draw = True
            if row >= cube.size and row < 2*cube.size:
                draw = True
            if row >= 2*cube.size:
                if col >= 2*cube.size and col < 3*cube.size:
                    draw = True
            if draw:
                # Draw outline
                x = displayWidth/2 + squareSize*(col-2*cube.size) - col + 2*(cube.size-1) + 1
                y = displayHeight/2 + squareSize*(row-(2*cube.size-1)) + (cube.size-2)*0.5*squareSize - row + cube.size + (cube.size/2-1)
                pygame.draw.rect(window, black, (x, y, squareSize, squareSize), 1)

                # Fill with color
                color = config['color' + str(cube.net[row][col])]
                pygame.draw.rect(window, color, (x+1, y+1, squareSize-2, squareSize-2))


def drawCube(cube):
    pass


def main():
    global cubeTurnTimeout
    cube = Cube(20)

    # Main loop
    running = True
    while running:
        # White background
        window.fill((255, 255, 255))

        # TextSurf, TextRect = text_objects("TEXT", font)
        # TextRect.center = ((displayWidth/2), (displayHeight/2))
        # window.blit(TextSurf, TextRect)

        # Change view mode button
        button(config['viewMode'], displayWidth-210, 10, 200, 100, (100, 100, 100), (150, 150, 150), switchViewMode)

        # Draw cube or net
        if config['viewMode'] == 'net':
            drawNet(cube)
        else:
            drawCube(cube)

        # Push the frame to the screen
        pygame.display.update()

        # Game quitting handling
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                # Save current config to config.json
                with open('config.json', 'w') as file:
                    json.dump(config, file, indent=4, sort_keys=True)

                # Exit
                running = False
                break

        # Normal input handling
        if time() - cubeTurnTimeout > 0.05:
            cubeTurnTimeout = time()
            allKeys = pygame.key.get_pressed()
            if allKeys[pygame.K_f]:
                if allKeys[pygame.K_LSHIFT] or allKeys[pygame.K_RSHIFT]:
                    cube.turn(1, -1)
                else:
                    cube.turn(1, 1)
            if allKeys[pygame.K_u]:
                if allKeys[pygame.K_LSHIFT] or allKeys[pygame.K_RSHIFT]:
                    cube.turn(0, -1)
                else:
                    cube.turn(0, 1)
            if allKeys[pygame.K_r]:
                if allKeys[pygame.K_LSHIFT] or allKeys[pygame.K_RSHIFT]:
                    cube.turn(2, -1)
                else:
                    cube.turn(2, 1)
            if allKeys[pygame.K_l]:
                if allKeys[pygame.K_LSHIFT] or allKeys[pygame.K_RSHIFT]:
                    cube.turn(5, -1)
                else:
                    cube.turn(5, 1)
            if allKeys[pygame.K_d]:
                if allKeys[pygame.K_LSHIFT] or allKeys[pygame.K_RSHIFT]:
                    cube.turn(3, -1)
                else:
                    cube.turn(3, 1)
            if allKeys[pygame.K_b]:
                if allKeys[pygame.K_LSHIFT] or allKeys[pygame.K_RSHIFT]:
                    cube.turn(4, -1)
                else:
                    cube.turn(4, 1)


if __name__ == '__main__':
    # Pygame Initialization
    pygame.init()
    pygame.font.init()
    displayWidth, displayHeight = 1920, 1080
    window = pygame.display.set_mode((displayWidth, displayHeight))
    font = pygame.font.Font('freesansbold.ttf', 115)
    clock = pygame.time.Clock()

    # Read config file
    with open('config.json', 'r') as file:
        config = json.loads(' '.join(file.readlines()))
    for key in config.keys():
        print(key, ':', config[key])

    # Other global vars
    changeViewmodeTimeout = time()  # You can only change the view mode once every 0.5s (so that you don't press the button a million times with one press)
    cubeTurnTimeout = time()        # You can only turn a face once every 0.05s

    # Print instructions
    print("Turn | Keybinding")
    print("  F' |     f")
    print("  F  |     F")
    print("  R  |     r")
    print("  R' |     R")
    print("  U  |     u")
    print("  U' |     U")
    print("  B  |     b")
    print("  B' |     B")
    print("  L  |     l")
    print("  L' |     L")
    print("  D  |     d")
    print("  D' |     D")

    # Go to main control loop
    main()
