import random

class Mongoose:
    def __init__(self, squares, snake_segments):
        self.squares = squares
        self.respawn(snake_segments)

    def respawn(self, snake_segments):
        while True:
            self.position = (random.randint(0, self.squares-1), random.randint(0, self.squares-1))
            if self.position not in snake_segments:
                break

    def draw(self, screen, image, yOffset, SQR_SIZE):
        x, y = self.position
        screen.blit(image, (x*SQR_SIZE, y*SQR_SIZE + yOffset))
