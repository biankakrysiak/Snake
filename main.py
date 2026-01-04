import pygame as p
import time
from Snake import Snake
from Food import Food
from Menu import Menu
from SoundManager import SoundManager
from Laser import Laser
from Mongoose import Mongoose

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
    mongooseImg = p.transform.scale(p.image.load("img/mongoose.png"), (SQR_SIZE, SQR_SIZE))
    laserImg = p.transform.scale(p.image.load("img/laser.png"), (SQR_SIZE, SQR_SIZE))


    running = True
    while running:
        action = menu.showMain(screen, clock)

        if action == "PLAY":
            score, playTime = runGame(screen, clock, foodImg, background, snakeTextures, 
                                      menu, sound, mongooseImg, laserImg)
            menu.showGameOver(screen, clock, score, playTime)
            if menu.settings.music:
                sound.play_music()  # music in main menu after game over (if it was turned on)

        elif action == "SETTINGS":
            menu.showSettings(screen, clock)
        elif action == "EXIT":
            running = False

    p.quit()

def runGame(screen, clock, foodImg, background, snakeTextures, menu, sound, mongooseImg, laserImg):
    snake = Snake(SQUARES)
    food = Food(SQUARES, snake.segments)
    score = 0
    startTime = time.time()
    paused = False
    pause_btn = None
    
    mongooses = []
    lasers = []
    mongooseSpawn = 2
    
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
                    elif e.key == p.K_x and menu.settings.game_mode == "Advanced":
                        laser = Laser(snake.segments[0], snake.direction, SQUARES)
                        lasers.append(laser)
                        sound.laser_shot()
            elif e.type == p.MOUSEBUTTONDOWN and e.button == 1:
                if pause_btn and pause_btn.collidepoint(p.mouse.get_pos()):
                    paused = not paused
                mx, my = p.mouse.get_pos()
                if my <= UI_HEIGHT:
                    if mx >= WIDTH - 110 and mx <= WIDTH - 70:
                        menu.settings.music = not menu.settings.music
                        if menu.settings.music:
                            sound.play_music()
                        else:
                            sound.stop_music()
                    elif mx >= WIDTH - 60 and mx <= WIDTH - 20:
                        menu.settings.sound = not menu.settings.sound

        if not paused:
            snake.move()    

            if snake.segments[0] == food.position:
                snake.shouldGrow = True
                score = score + 1
                food.respawn(snake.segments)
                sound.apple_eaten()
                if menu.settings.game_mode == "Advanced":
                    if score % mongooseSpawn == 0 and score > 0:
                        mongoose = Mongoose(SQUARES, snake.segments)
                        mongooses.append(mongoose)

            
            headX, headY = snake.segments[0] 
            if menu.settings.game_mode == "Advanced":
                headX %= SQUARES
                headY %= SQUARES
                snake.segments[0] = (headX, headY)
                
                # mongoose collision
                for mongoose in mongooses:
                    if snake.segments[0] == mongoose.position:
                        running = False
                        break
                
                # move and check lasers
                for laser in lasers[:]:
                    # laser speed 3x
                    for _ in range(3):
                        if laser.active:
                            laser.move()
                            
                            # check if laser hits mongoose po każdym ruchu
                            for mongoose in mongooses[:]:
                                if laser.pos == mongoose.position:
                                    mongooses.remove(mongoose)
                                    laser.active = False
                                    sound.mongoose_killed()
                                    break
                            
                            # check if laser hits snake body
                            if laser.active and laser.pos in snake.segments[1:]:
                                running = False
                                laser.active = False
                                break

                    if not laser.active:
                        lasers.remove(laser)
                if not running:
                    break

            else:  # wall collision
                if headX < 0 or headX >= SQUARES or headY < 0 or headY >= SQUARES:
                    break

            if snake.segments[0] in snake.segments[1:]: # snake collision
                running = False

        playTime = time.time() - startTime
        pause_btn = draw(screen, snake, food, foodImg, background, snakeTextures, menu, score, playTime, paused, mongooses, mongooseImg, lasers, laserImg)
        fps = menu.settings.fps
        if menu.settings.game_mode == "Advanced":
            fps = 4 + score // 2
            fps = min(fps, 14)
        clock.tick(fps)
    
    sound.game_over()
    return score, playTime

def draw(screen, snake, food, foodImg, background, snakeTextures, menu, score, playTime, paused, mongooses, mongooseImg, lasers, laserImg):
    screen.fill((30, 30, 40))
    screen.blit(background, (0, UI_HEIGHT))

    fx, fy = food.position
    screen.blit(foodImg, (fx*SQR_SIZE, fy*SQR_SIZE + UI_HEIGHT))

    for mongoose in mongooses:
        mongoose.draw(screen, mongooseImg, UI_HEIGHT, SQR_SIZE)
    
    for laser in lasers:
        lx, ly = laser.pos
        lx = lx % SQUARES
        ly = ly % SQUARES
        laserRotated = rotateByDirection(laserImg, laser.direction)
        screen.blit(laserRotated, (lx*SQR_SIZE, ly*SQR_SIZE + UI_HEIGHT))

    drawSnake(screen, snake, snakeTextures, UI_HEIGHT)

    pause_btn = menu.drawUI(screen, score, playTime, len(snake.segments), paused, UI_HEIGHT)
    
    p.display.flip()
    return pause_btn

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
    elif direction == "DOWN":
       return p.transform.rotate(image, -90)
    elif direction == "LEFT":
        return p.transform.rotate(image, 180)
    elif direction == "UP":
        return p.transform.rotate(image, 90)
    else:
        return image

def rotateByVector(image, vec):
    if vec == (1, 0):
        return image
    elif vec == (-1, 0):
        return p.transform.rotate(image, 180)
    elif vec == (0, 1):
        return p.transform.rotate(image, -90)
    elif vec == (0, -1):
        return p.transform.rotate(image, 90)
    else:
        return image

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
