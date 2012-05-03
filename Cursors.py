#!/usr/bin/env python

import pygame

class Cursors():
    def __init__(self):
        self.arrow = ( "xX                      ",
                  "X.X                     ",
                  "X..X                    ",
                  "X...X                   ",
                  "X....X                  ",
                  "X.....X                 ",
                  "X......X                ",
                  "X.......X               ",
                  "X........X              ",
                  "X.........X             ",
                  "X......XXXXX            ",
                  "X...X..X                ",
                  "X..XX..X                ",
                  "X.X XX..X               ",
                  "XX   X..X               ",
                  "X     X..X              ",
                  "      X..X              ",
                  "       X..X             ",
                  "       X..X             ",
                  "        XX              ",
                  "                        ",
                  "                        ",
                  "                        ",
                  "                        ")


        self.no = ("                        ",
                 "                        ",
                 "         XXXXXX         ",
                 "       XX......XX       ",
                 "      X..........X      ",
                 "     X....XXXX....X     ",
                 "    X...XX    XX...X    ",
                 "   X.....X      X...X   ",
                 "   X..X...X      X..X   ",
                 "  X...XX...X     X...X  ",
                 "  X..X  X...X     X..X  ",
                 "  X..X   X...X    X..X  ",
                 "  X..X    X.,.X   X..X  ",
                 "  X..X     X...X  X..X  ",
                 "  X...X     X...XX...X  ",
                 "   X..X      X...X..X   ",
                 "   X...X      X.....X   ",
                 "    X...XX     X...X    ",
                 "     X....XXXXX...X     ",
                 "      X..........X      ",
                 "       XX......XX       ",
                 "         XXXXXX         ",
                 "                        ",
                 "                        ",
                )
        
        self.move = ("                        ",
                "                        ",
                "            X           ",
                "            XX          ",
                "            X X         ",
                "            X..X        ",
                "            X...X       ",
                "            X....X      ",
                " XXXXXXXXXXXX.....X     ",
                " X.................X    ",
                " X..................X   ",
                " X...................x  ",
                " X..................X   ",
                " X.................X    ",
                " XXXXXXXXXXXX.....X     ",
                "            X....X      ",
                "            X...X       ",
                "            X..X        ",
                "            X.X         ",
                "            XX          ",
                "            X           ",
                "                        ",
                "                        ",
                "                        ",
                )
        self.hand= (
                "     xX         ",
                "    X..X        ",
                "    X..X        ",
                "    X..X        ",
                "    X..XXXXX    ",
                "    X..X..X.XX  ",
                " XX X..X..X.X.X ",
                "X..XX.........X ",
                "X...X.........X ",
                " X.....X.X.X..X ",
                "  X....X.X.X..X ",
                "  X....X.X.X.X  ",
                "   X...X.X.X.X  ",
                "    X.......X   ",
                "     X....X.X   ",
                "     XXXXX XX   ")

    def SetCursor(self,arrow):
        hotspot = None
        for y in range(len(arrow)):
            for x in range(len(arrow[y])):
                if arrow[y][x] in ['x', ',', 'O']:
                    hotspot = x,y
                    break
            if hotspot != None:
                break
        if hotspot == None:
            raise Exception("No hotspot specified for cursor!" )
        s2 = []
        for line in arrow:
            s2.append(line.replace('x', 'X').replace(',', '.').replace('O', 'o'))
        cursor, mask = pygame.cursors.compile(s2, 'X', '.', 'o')
        size = len(arrow[0]), len(arrow)
        return size, hotspot, cursor, mask
        



