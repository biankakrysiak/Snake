import pygame as p
import random

class Snake:
    def __init__(self, squares):
        margin = 5
        startX = random.randint(margin, squares - margin - 1)
        startY = random.randint(margin, squares - margin - 1)

        self.segments = [(startX,     startY),
                         (startX - 1, startY),
                         (startX - 2, startY)]
        
        self.direction = "RIGHT"
        self.shouldGrow = False

    def move(self):
        headX, headY = self.segments[0]
        
        if self.direction == "UP":
            newHead = (headX, headY - 1)
        elif self.direction == "DOWN":
            newHead = (headX, headY + 1)
        elif self.direction == "LEFT":
            newHead = (headX - 1, headY)
        elif self.direction == "RIGHT":
            newHead = (headX + 1, headY)
        
        self.segments.insert(0, newHead)
        if not self.shouldGrow:
            self.segments.pop()
        else:
            self.shouldGrow = False
    