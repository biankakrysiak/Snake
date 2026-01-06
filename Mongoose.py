import random

class Mongoose:
    def __init__(self, squares, snake_segments):
        self.squares = squares # spawn mongoose at initial random position
        self.respawn(snake_segments)

    def respawn(self, snake_segments):
        # find random position that doesn't overlap with snake
        while True:
            # generate random coordinates within grid bounds
            self.position = (random.randint(0, self.squares-1), random.randint(0, self.squares-1))
            # ensure mongoose doesn't spawn on top of snake
            if self.position not in snake_segments:
                break

    def draw(self, screen, image, yOffset, SQR_SIZE):
        # render mongoose
        x, y = self.position
        screen.blit(image, (x*SQR_SIZE, y*SQR_SIZE + yOffset))