import pygame as p
import random
from Snake import Snake
from Food import Food

WIDTH = 800
HEIGHT = 800
SQUARES = 32  # macierz 32x32
SQR_SIZE = HEIGHT // SQUARES
FPS = 6

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption('Snake')
    clock = p.time.Clock()
    foodImg = p.transform.scale(p.image.load("img/food.png"), (SQR_SIZE,SQR_SIZE))
    background = p.transform.scale(p.image.load("img/grid.jpg"), (WIDTH, HEIGHT))

    running = True
    while running:
        score = runGame(screen, clock, foodImg, background)
        print("Twój wynik:", score)
        running = False
    p.quit()

def runGame(screen, clock, foodImg, background):
    snake = Snake(SQUARES)
    food = Food(SQUARES, snake.segments)
    score = 0
    
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.KEYDOWN:
                if e.key == p.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif e.key == p.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif e.key == p.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif e.key == p.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"
        
        snake.move()    
        if snake.segments[0] == food.position:
            snake.shouldGrow = True
            score = score + 1
            food.respawn(snake.segments)

        headX, headY = snake.segments[0] # wall collision
        if headX < 0 or headX >= SQUARES or headY < 0 or headY >= SQUARES:
            running = False

        if snake.segments[0] in snake.segments[1:]: # snake collision
            running = False

        draw(screen, snake, food, foodImg, background)
        clock.tick(FPS)

    return score



def draw(screen, snake, food, foodImg, background):
    screen.blit(background, (0,0))

    fx, fy = food.position
    screen.blit(foodImg, (fx*SQR_SIZE, fy*SQR_SIZE))

    for x, y in snake.segments:
        p.draw.rect(screen, p.Color("blue"), (x*SQR_SIZE, y*SQR_SIZE, SQR_SIZE, SQR_SIZE))

    p.display.flip()


if __name__ == "__main__":
    main()