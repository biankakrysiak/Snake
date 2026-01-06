import random

class Snake:
    def __init__(self, squares):
        # spawn snake away from edges
        margin = 5
        startX = random.randint(margin, squares - margin - 1)
        startY = random.randint(margin, squares - margin - 1)

        # initial snake with 3 segments (head + 2 body parts)
        self.segments = [(startX,     startY),
                         (startX - 1, startY),
                         (startX - 2, startY)]
        
        self.direction = "RIGHT"
        self.shouldGrow = False

    def move(self):
        headX, headY = self.segments[0]
        
        # calculate new head position based on direction
        if self.direction == "UP":
            newHead = (headX, headY - 1)
        elif self.direction == "DOWN":
            newHead = (headX, headY + 1)
        elif self.direction == "LEFT":
            newHead = (headX - 1, headY)
        elif self.direction == "RIGHT":
            newHead = (headX + 1, headY)
        
        # add new head at front
        self.segments.insert(0, newHead)
        
        # remove tail unless snake should grow
        if not self.shouldGrow:
            self.segments.pop()
        else:
            self.shouldGrow = False