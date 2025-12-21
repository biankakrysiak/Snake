import random

class Food:
    def __init__(self, squares, snakeSegments):
        self.squares = squares
        self.position = self.randomPosition(snakeSegments)

    def randomPosition(self, snakeSegments):
        while True:
            position = (random.randint(0, self.squares - 1), random.randint(0, self.squares - 1))
            if position not in snakeSegments:
                return position
            
    def respawn(self, snakeSegments):
        self.position = self.randomPosition(snakeSegments)