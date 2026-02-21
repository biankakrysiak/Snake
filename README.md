# Snake

A Snake game built with **Python** and **pygame**, with two game modes, animated snake textures, sound effects, background music, and enemies.

---

## Features

- **Two game modes:** Classic and Advanced
- **Three difficulty levels:** Easy, Normal, Hard (Classic mode only)
- Animated snake with **directional textures** for head, body, tail, and turns
- **Mongoose enemies** that spawn as your score grows (Advanced mode)
- **Laser shooting** mechanic to eliminate enemies (Advanced mode)
- Background music and sound effects with in-game toggles
- Pause functionality during gameplay
- Game Over screen showing final score, time, difficulty, and mode

---

## Game Modes

### Classic
The traditional Snake experience. Eat apples to grow longer, avoid the walls, and don't run into yourself. Difficulty controls the snake's speed (Easy / Normal / Hard).

### Advanced
A more chaotic version with no walls. The snake wraps around the borders instead. As your score increases, **mongooses** spawn on the grid. Press **X** to shoot a laser in the direction you're facing to eliminate them. Watch out: lasers wrap around the grid too, and hitting your own body with one ends the game. Speed increases dynamically with your score.

---

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys | Move the snake |
| `X` | Shoot laser (Advanced mode only) |
| `P` or `ESC` | Pause / Unpause |
| `SPACE` / `Enter` | Restart after Game Over |

Music and SFX can be toggled from both the main menu and the in-game UI bar.

---

## Project Structure

```
├── main.py            # Entry point, game loop, rendering
├── Snake.py           # Snake movement and growth logic
├── Food.py            # Food spawning and repositioning
├── Laser.py           # Laser movement and border wrapping
├── Mongoose.py        # Enemy spawning and rendering
├── Menu.py            # UI, menus, settings, game over screen
├── SoundManager.py    # Music and sound effect management
├── img/
│   ├── snake/         # head.png, body.png, tail.png, turn.png
│   ├── food.png
│   ├── mongoose.png
│   ├── laser.png
│   ├── grid.jpg
│   └── menu.png
├── sounds/
│   ├── appleEaten.wav
│   ├── gameOver.wav
│   ├── laser.wav
│   ├── kill.mp3
│   └── classicMusic.mp3
└── fonts/
    └── Jersey10-Regular.ttf
```

---

## Requirements

- Python 3.x
- Pygame

Install Pygame with:

```bash
pip install pygame
```

---

## Running the Game

```bash
python main.py
```

---

## Settings

| Setting | Options |
|---------|---------|
| Difficulty | Easy (4 fps), Normal (8 fps), Hard (12 fps) |
| Game Mode | Classic, Advanced |
| Music | On / Off |
| Sound Effects | On / Off |

In **Advanced mode**, difficulty is disabled. Speed scales automatically from 4 fps up to a cap of 14 fps as your score increases.
