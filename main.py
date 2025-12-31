import pygame as p
import time
from Snake import Snake
from Food import Food
from Menu import Menu
from SoundManager import SoundManager

WIDTH = 720
HEIGHT = 720
UI_HEIGHT = 60
TOTAL_HEIGHT = HEIGHT + UI_HEIGHT
SQUARES = 20 # macierz 20x20
SQR_SIZE = HEIGHT // SQUARES


def main():
    p.init()
    p.mixer.init()
    menu = Menu(WIDTH, HEIGHT)
    sound = SoundManager(menu.settings)
    menu.sound = sound
    sound.play_music()

    screen = p.display.set_mode((WIDTH, TOTAL_HEIGHT))
    p.display.set_caption('Snake')
    clock = p.time.Clock()
    foodImg = p.transform.scale(p.image.load("img/food.png"), (SQR_SIZE,SQR_SIZE))
    background = p.transform.scale(p.image.load("img/grid.jpg"), (WIDTH, HEIGHT))
    snakeTextures = loadSnakeTextures()

    running = True
    while running:
        action = menu.showMain(screen, clock)

        if action == "PLAY":
            score, playTime = runGame(screen, clock, foodImg, background, snakeTextures, menu, sound)
            menu.showGameOver(screen, clock, score, playTime)
            if menu.settings.music:
                sound.play_music()  # wznawia muzykę po Game Over, jeśli była włączona

        elif action == "SETTINGS":
            menu.showSettings(screen, clock)
        elif action == "EXIT":
            running = False

    p.quit()

def runGame(screen, clock, foodImg, background, snakeTextures, menu, sound):
    snake = Snake(SQUARES)
    food = Food(SQUARES, snake.segments)
    score = 0
    startTime = time.time()
    paused = False
    
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                return score, time.time() - startTime
            elif e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE or e.key == p.K_p:
                    paused = not paused
                elif not paused:
                    if e.key == p.K_UP and snake.direction != "DOWN":
                        snake.direction = "UP"
                    elif e.key == p.K_DOWN and snake.direction != "UP":
                        snake.direction = "DOWN"
                    elif e.key == p.K_LEFT and snake.direction != "RIGHT":
                        snake.direction = "LEFT"
                    elif e.key == p.K_RIGHT and snake.direction != "LEFT":
                        snake.direction = "RIGHT"
        if not paused:
            snake.move()    

            if snake.segments[0] == food.position:
                snake.shouldGrow = True
                score = score + 1
                food.respawn(snake.segments)
                sound.apple_eaten()
            
            headX, headY = snake.segments[0] # wall collision
            if headX < 0 or headX >= SQUARES or headY < 0 or headY >= SQUARES:
                break

            if snake.segments[0] in snake.segments[1:]: # snake collision
                running = False

        playTime = time.time() - startTime
        draw(screen, snake, food, foodImg, background, snakeTextures, menu, score, playTime, paused)
        clock.tick(menu.settings.fps)
    
    sound.game_over()
    return score, playTime

def draw(screen, snake, food, foodImg, background, snakeTextures, menu, score, playTime, paused):
    screen.fill((30, 30, 40))
    screen.blit(background, (0, UI_HEIGHT))

    fx, fy = food.position
    screen.blit(foodImg, (fx*SQR_SIZE, fy*SQR_SIZE + UI_HEIGHT))

    drawSnake(screen, snake, snakeTextures, UI_HEIGHT)

    menu.drawUI(screen, score, playTime, len(snake.segments), paused, UI_HEIGHT)

    p.display.flip()

def drawSnake(screen, snake, textures, yOffset):
    segments = snake.segments
    n = len(segments)

    for i in range(n):
        x, y = segments[i]
        pos = (x * SQR_SIZE, y * SQR_SIZE + yOffset)

        if i == 0: # head
            headImg = rotateByDirection(textures["head"], snake.direction)
            screen.blit(headImg, pos)
        elif i == n - 1: # tail
            tail = segments[i]
            before = segments[i - 1]
            vec = getVector(tail, before)
            tailImg = rotateByVector(textures["tail"], vec)
            screen.blit(tailImg, pos)
        else: # body
            prev = segments[i - 1]
            curr = segments[i]
            next = segments[i + 1]

            d1 = getVector(curr, prev)
            d2 = getVector(curr, next)

            # straight
            if d1[0] == d2[0]:  # vertical
                img = rotateByVector(textures["body"], (0, 1))
            elif d1[1] == d2[1]:  # horizontal
                img = rotateByVector(textures["body"], (1, 0))
            else:
                img = rotateTurn(textures["turn"], d1,d2)

            screen.blit(img, pos)

def getVector(a, b):
    return (b[0] - a[0], b[1] - a[1])

def rotateByDirection(image, direction):
    if direction == "RIGHT":
        return image
    if direction == "DOWN":
        return p.transform.rotate(image, -90)
    if direction == "LEFT":
        return p.transform.rotate(image, 180)
    if direction == "UP":
        return p.transform.rotate(image, 90)

def rotateByVector(image, vec):
    if vec == (1, 0):
        return image
    if vec == (-1, 0):
        return p.transform.rotate(image, 180)
    if vec == (0, 1):
        return p.transform.rotate(image, -90)
    if vec == (0, -1):
        return p.transform.rotate(image, 90)
    
def rotateTurn(image, dPrev, dNext):
    pair = (dPrev, dNext)
    if pair in [((0,1),(1,0)), ((1,0),(0,1))]: # up -> right
        return image
    elif pair in [((1,0),(0,-1)), ((0,-1),(1,0))]: # right -> down
        return p.transform.rotate(image, 90)
    elif pair in [((0,-1),(-1,0)), ((-1,0),(0,-1))]: # down -> left
        return p.transform.rotate(image, 180)
    elif pair in [((-1,0),(0,1)), ((0,1),(-1,0))]: # left -> up
        return p.transform.rotate(image, -90)
    else:
        return image

def loadSnakeTextures():
    url = "img/snake/"
    return {
        "head": p.transform.scale(p.image.load(url+"head.png"), (SQR_SIZE, SQR_SIZE)),
        "body": p.transform.scale(p.image.load(url+"body.png"), (SQR_SIZE, SQR_SIZE)),
        "tail": p.transform.scale(p.image.load(url+"tail.png"), (SQR_SIZE, SQR_SIZE)),
        "turn": p.transform.scale(p.image.load(url+"turn.png"), (SQR_SIZE, SQR_SIZE)),
    }

if __name__ == "__main__":
    main()