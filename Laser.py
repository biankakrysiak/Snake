class Laser:
    def __init__(self, pos, direction, squares):
        self.pos = pos
        self.direction = direction
        self.squares = squares
        self.active = True
        self.wrapped = False # border checks

    def move(self):
        x, y = self.pos
        old_x, old_y = x, y
        
        if self.direction == "UP":
            y -= 1
        elif self.direction == "DOWN":
            y += 1
        elif self.direction == "LEFT":
            x -= 1
        elif self.direction == "RIGHT":
            x += 1
        
        # checks if laser went trough the border
        if x < 0 or x >= self.squares or y < 0 or y >= self.squares:
            if self.wrapped:
                # if the laser already went through it once, delete it
                self.active = False
                return
            else:
                # first crossing with the border
                self.wrapped = True
                x = x % self.squares
                y = y % self.squares
        
        self.pos = (x, y)