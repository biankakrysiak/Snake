import pygame as p
import random
from Snake import Snake
from Food import Food

WIDTH = 1024
HEIGHT = 1024
SQUARES = 32  # macierz 32x32
SQR_SIZE = HEIGHT // SQUARES
FPS = 10

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption('Snake')
    clock = p.time.Clock()


    running = True
    while running:
        score = runGame(screen, clock)
        print("Twój wynik:", score)
        running = False
    p.quit()

def runGame(screen, clock):
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

        draw(screen, snake, food)
        clock.tick(FPS)

    return score



def draw(screen, snake, food):
    screen.fill(p.Color("white"))

    fx, fy = food.position
    p.draw.rect(screen, p.Color("red"), (fx*SQR_SIZE, fy*SQR_SIZE, SQR_SIZE, SQR_SIZE))

    for x, y in snake.segments:
        p.draw.rect(screen, p.Color("green"), (x*SQR_SIZE, y*SQR_SIZE, SQR_SIZE, SQR_SIZE))

    p.display.flip()


if __name__ == "__main__":
    main()