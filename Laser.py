class Laser:
    def __init__(self, pos, direction, squares):
        self.pos = pos
        self.direction = direction
        self.squares = squares
        self.active = True
        self.wrapped = False  # track if laser crossed border once

    def move(self):
        x, y = self.pos
        
        # move laser in its direction
        if self.direction == "UP":
            y -= 1
        elif self.direction == "DOWN":
            y += 1
        elif self.direction == "LEFT":
            x -= 1
        elif self.direction == "RIGHT":
            x += 1
        
        # handle border crossing (wrapping)
        if x < 0 or x >= self.squares or y < 0 or y >= self.squares:
            if self.wrapped:
                # laser already wrapped once, deactivate it
                self.active = False
                return
            else:
                # first wrap, allow it to continue
                self.wrapped = True
                x = x % self.squares
                y = y % self.squares
        
        self.pos = (x, y)