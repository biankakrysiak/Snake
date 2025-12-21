import pygame as p
import random

WIDTH = 1024
HEIGHT = 1024
DIMENSION = 32
SQR_SIZE = HEIGHT // DIMENSION
FPS = 30

def main():
    p.init()
    FPS = p.time.Clock()
    p.display.set_caption('Snake')
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(p.Color("white"))

    while True:
        runGame()


def runGame():
    startX = random.randint(5, SQR_SIZE - 6)
    startY = random.randint(5, SQR_SIZE - 6)
    snakeCoordinates = [{'x': startX,     'y': startY},
                        {'x': startX - 1, 'y': startY},
                        {'x': startX - 2, 'y': startY}]