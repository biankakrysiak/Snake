import pygame as p
import time
from Snake import Snake
from Food import Food
from Menu import Menu
from SoundManager import SoundManager
from Laser import Laser
from Mongoose import Mongoose

# game window dimensions
WIDTH = 720
HEIGHT = 720
UI_HEIGHT = 60
TOTAL_HEIGHT = HEIGHT + UI_HEIGHT

# grid configuration
SQUARES = 20  # 20x20 grid
SQR_SIZE = HEIGHT // SQUARES


def main():
    # initialize pygame and audio
    p.init()
    p.mixer.init()
    
    # create menu and sound systems
    menu = Menu(WIDTH, HEIGHT)
    sound = SoundManager(menu.settings)
    menu.sound = sound
    sound.play_music()

    # setup window
    screen = p.display.set_mode((WIDTH, TOTAL_HEIGHT))
    p.display.set_caption('Snake')
    clock = p.time.Clock()
    
    # load game assets
    foodImg = p.transform.scale(p.image.load("img/food.png"), (SQR_SIZE, SQR_SIZE))
    background = p.transform.scale(p.image.load("img/grid.jpg"), (WIDTH, HEIGHT))
    snakeTextures = loadSnakeTextures()
    mongooseImg = p.transform.scale(p.image.load("img/mongoose.png"), (SQR_SIZE, SQR_SIZE))
    laserImg = p.transform.scale(p.image.load("img/laser.png"), (SQR_SIZE, SQR_SIZE))

    # main application loop
    running = True
    while running:
        action = menu.showMain(screen, clock)

        if action == "PLAY":
            # run game and show results
            score, playTime = runGame(screen, clock, foodImg, background, snakeTextures, 
                                      menu, sound, mongooseImg, laserImg)
            menu.showGameOver(screen, clock, score, playTime)
            
            # restart menu music if enabled
            if menu.settings.music:
                sound.play_music()

        elif action == "SETTINGS":
            menu.showSettings(screen, clock)
        elif action == "EXIT":
            running = False

    p.quit()

def runGame(screen, clock, foodImg, background, snakeTextures, menu, sound, mongooseImg, laserImg):
    # initialize game objects
    snake = Snake(SQUARES)
    food = Food(SQUARES, snake.segments)
    score = 0
    startTime = time.time()
    paused = False
    pause_btn = None
    
    # advanced mode specific
    mongooses = []
    lasers = []
    mongooseSpawn = 2  # spawn mongoose every N points
    
    running = True
    while running:
        # handle input events
        for e in p.event.get():
            if e.type == p.QUIT:
                return score, time.time() - startTime
            
            elif e.type == p.KEYDOWN:
                # pause/unpause game
                if e.key == p.K_ESCAPE or e.key == p.K_p:
                    paused = not paused 
                
                elif not paused:
                    # snake movement (prevent 180 degree turns)
                    if e.key == p.K_UP and snake.direction != "DOWN":
                        snake.direction = "UP"
                    elif e.key == p.K_DOWN and snake.direction != "UP":
                        snake.direction = "DOWN"
                    elif e.key == p.K_LEFT and snake.direction != "RIGHT":
                        snake.direction = "LEFT"
                    elif e.key == p.K_RIGHT and snake.direction != "LEFT":
                        snake.direction = "RIGHT"
                    
                    # shoot laser in advanced mode
                    elif e.key == p.K_x and menu.settings.game_mode == "Advanced":
                        laser = Laser(snake.segments[0], snake.direction, SQUARES)
                        lasers.append(laser)
                        sound.laser_shot()
            
            elif e.type == p.MOUSEBUTTONDOWN and e.button == 1:
                # pause button click
                if pause_btn and pause_btn.collidepoint(p.mouse.get_pos()):
                    paused = not paused
                
                # ui button clicks
                mx, my = p.mouse.get_pos()
                if my <= UI_HEIGHT:
                    # music toggle
                    if mx >= WIDTH - 110 and mx <= WIDTH - 70:
                        menu.settings.music = not menu.settings.music
                        if menu.settings.music:
                            sound.play_music()
                        else:
                            sound.stop_music()
                    # sfx toggle
                    elif mx >= WIDTH - 60 and mx <= WIDTH - 20:
                        menu.settings.sound = not menu.settings.sound

        # game logic (only when not paused)
        if not paused:
            snake.move()    

            headX, headY = snake.segments[0]
            
            # advanced mode mechanics
            if menu.settings.game_mode == "Advanced":
                # wrap around borders
                headX %= SQUARES
                headY %= SQUARES
                snake.segments[0] = (headX, headY)
                
                # check food collision after wrapping
                if snake.segments[0] == food.position:
                    snake.shouldGrow = True
                    score += 1
                    food.respawn(snake.segments)
                    sound.apple_eaten()
                    
                    # spawn mongoose in advanced mode
                    if score % mongooseSpawn == 0 and score > 0:
                        mongoose = Mongoose(SQUARES, snake.segments)
                        mongooses.append(mongoose)
                
                # check mongoose collision
                for mongoose in mongooses:
                    if snake.segments[0] == mongoose.position:
                        running = False
                        break
                
                # update and check lasers
                for laser in lasers[:]:
                    # laser moves 3x faster than snake
                    for _ in range(3):
                        if laser.active:
                            laser.move()
                            
                            # check laser-mongoose collision
                            for mongoose in mongooses[:]:
                                if laser.pos == mongoose.position:
                                    mongooses.remove(mongoose)
                                    laser.active = False
                                    sound.mongoose_killed()
                                    break
                            
                            # check laser-snake body collision
                            if laser.active and laser.pos in snake.segments[1:]:
                                running = False
                                laser.active = False
                                break

                    # remove inactive lasers
                    if not laser.active:
                        lasers.remove(laser)
                
                if not running:
                    break

            else:
                # check food collision before wall check in classic mode
                if snake.segments[0] == food.position:
                    snake.shouldGrow = True
                    score += 1
                    food.respawn(snake.segments)
                    sound.apple_eaten()
                
                # classic mode: check wall collision
                if headX < 0 or headX >= SQUARES or headY < 0 or headY >= SQUARES:
                    break

            # check self collision
            if snake.segments[0] in snake.segments[1:]:
                running = False

        # render game
        playTime = time.time() - startTime
        pause_btn = draw(screen, snake, food, foodImg, background, snakeTextures, 
                        menu, score, playTime, paused, mongooses, mongooseImg, lasers, laserImg)
        
        # adjust fps based on mode
        fps = menu.settings.fps
        if menu.settings.game_mode == "Advanced":
            # increase speed with score, cap at 14 fps
            fps = 4 + score // 2
            fps = min(fps, 14)
        
        clock.tick(fps)
    
    sound.game_over()
    return score, playTime

def draw(screen, snake, food, foodImg, background, snakeTextures, menu, 
         score, playTime, paused, mongooses, mongooseImg, lasers, laserImg):
    # render background
    screen.fill((30, 30, 40))
    screen.blit(background, (0, UI_HEIGHT))

    # render food
    fx, fy = food.position
    screen.blit(foodImg, (fx*SQR_SIZE, fy*SQR_SIZE + UI_HEIGHT))

    # render mongooses
    for mongoose in mongooses:
        mongoose.draw(screen, mongooseImg, UI_HEIGHT, SQR_SIZE)
    
    # render lasers
    for laser in lasers:
        lx, ly = laser.pos
        # handle wrapping
        lx = lx % SQUARES
        ly = ly % SQUARES
        laserRotated = rotateByDirection(laserImg, laser.direction)
        screen.blit(laserRotated, (lx*SQR_SIZE, ly*SQR_SIZE + UI_HEIGHT))

    # render snake
    drawSnake(screen, snake, snakeTextures, UI_HEIGHT)

    # render ui
    pause_btn = menu.drawUI(screen, score, playTime, paused, UI_HEIGHT)
    
    p.display.flip()
    return pause_btn

def drawSnake(screen, snake, textures, yOffset):
    # render snake with proper textures for each segment
    segments = snake.segments
    n = len(segments)

    for i in range(n):
        x, y = segments[i]
        pos = (x * SQR_SIZE, y * SQR_SIZE + yOffset)

        if i == 0:  
            # head (rotated by direction)
            headImg = rotateByDirection(textures["head"], snake.direction)
            screen.blit(headImg, pos)
        
        elif i == n - 1:  
            # tail (rotated by previous segment direction)
            tail = segments[i]
            before = segments[i - 1]
            vec = getVector(tail, before)
            tailImg = rotateByVector(textures["tail"], vec)
            screen.blit(tailImg, pos)
        
        else:  
            # body segment (straight or turn)
            prev = segments[i - 1]
            curr = segments[i]
            next = segments[i + 1]

            d1 = getVector(curr, prev)
            d2 = getVector(curr, next)

            # check if segment is straight or turn
            if d1[0] == d2[0]:  # vertical
                img = rotateByVector(textures["body"], (0, 1))
            elif d1[1] == d2[1]:  # horizontal
                img = rotateByVector(textures["body"], (1, 0))
            else:  # turn
                img = rotateTurn(textures["turn"], d1, d2)

            screen.blit(img, pos)

def getVector(a, b):
    # calculate direction vector between two points
    return (b[0] - a[0], b[1] - a[1])

def rotateByDirection(image, direction):
    # rotate image based on direction string (for snake head and lasers)
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
    # rotate image based on direction vector (for tail and body of the snake)
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
    # rotate turn texture based on direction change
    pair = (dPrev, dNext)
    if pair in [((0,1),(1,0)), ((1,0),(0,1))]:  # up -> right or right -> up
        return image
    elif pair in [((1,0),(0,-1)), ((0,-1),(1,0))]:  # right -> down or down -> right
        return p.transform.rotate(image, 90)
    elif pair in [((0,-1),(-1,0)), ((-1,0),(0,-1))]:  # down -> left or left -> down
        return p.transform.rotate(image, 180)
    elif pair in [((-1,0),(0,1)), ((0,1),(-1,0))]:  # left -> up or up -> left
        return p.transform.rotate(image, -90)
    else:
        return image

def loadSnakeTextures():
    # load and scale all snake texture parts
    url = "img/snake/"
    return {
        "head": p.transform.scale(p.image.load(url+"head.png"), (SQR_SIZE, SQR_SIZE)),
        "body": p.transform.scale(p.image.load(url+"body.png"), (SQR_SIZE, SQR_SIZE)),
        "tail": p.transform.scale(p.image.load(url+"tail.png"), (SQR_SIZE, SQR_SIZE)),
        "turn": p.transform.scale(p.image.load(url+"turn.png"), (SQR_SIZE, SQR_SIZE)),
    }

if __name__ == "__main__":
    main()