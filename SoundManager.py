import pygame as p

class SoundManager:
    def __init__(self, settings):
        self.settings = settings

        self.apple = p.mixer.Sound("sounds/appleEaten.wav")
        self.gameover = p.mixer.Sound("sounds/gameOver.wav")
        self.apple.set_volume(0.1)
        self.gameover.set_volume(0.6)

        p.mixer.music.load("sounds/classicMusic.mp3")
        p.mixer.music.set_volume(0.1)

    def play_music(self):
        if self.settings.music:
            if not p.mixer.music.get_busy():
                p.mixer.music.play(-1)
            else:
                p.mixer.music.unpause()

    def pause_music(self):
        p.mixer.music.pause()

    def stop_music(self):
        p.mixer.music.stop()

    def toggle_music(self):
        self.settings.music = not self.settings.music
        if self.settings.music:
            self.play_music()
        else:
            self.pause_music()

    def apple_eaten(self):
        if self.settings.sound:
            self.apple.play()

    def game_over(self):
        if self.settings.sound:
            # Pauzujemy muzykę tylko podczas odtwarzania dźwięku Game Over
            if self.settings.music and p.mixer.music.get_busy():
                p.mixer.music.pause()
                self.music_was_playing = True
            else:
                self.music_was_playing = False

            self.gameover.play()