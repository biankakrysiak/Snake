import pygame as p

class SoundManager:
    def __init__(self, settings):
        self.settings = settings

        # load sound effects
        self.apple = p.mixer.Sound("sounds/appleEaten.wav")
        self.gameover = p.mixer.Sound("sounds/gameOver.wav")
        self.laser = p.mixer.Sound("sounds/laser.wav")
        self.kill = p.mixer.Sound("sounds/kill.mp3")
        
        # set volume levels for each sound
        self.apple.set_volume(0.1)
        self.gameover.set_volume(0.6)
        self.laser.set_volume(0.1)
        self.kill.set_volume(0.1)

        # load background music
        p.mixer.music.load("sounds/classicMusic.mp3")
        p.mixer.music.set_volume(0.1)

    def play_music(self):
        # start or resume background music
        if self.settings.music:
            if not p.mixer.music.get_busy():
                p.mixer.music.play(-1)  # loop forever
            else:
                p.mixer.music.unpause()

    def pause_music(self):
        p.mixer.music.pause()

    def stop_music(self):
        p.mixer.music.stop()

    def toggle_music(self):
        # switch music on/off
        self.settings.music = not self.settings.music
        if self.settings.music:
            self.play_music()
        else:
            self.pause_music()

    def apple_eaten(self):
        # play apple eating sound
        if self.settings.sound:
            self.apple.play()

    def laser_shot(self):
        # play laser shooting sound
        if self.settings.sound:
            self.laser.play()
    
    def mongoose_killed(self):
        # play mongoose kill sound
        if self.settings.sound:
            self.kill.play()

    def game_over(self):
        # pause music and play game over sound
        if self.settings.sound:
            if self.settings.music and p.mixer.music.get_busy():
                p.mixer.music.pause()

            self.gameover.play()