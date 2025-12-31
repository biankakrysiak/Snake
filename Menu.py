import pygame as p
import time

class GameSettings:
    def __init__(self):
        self.difficulty = "Normal"  # Easy, Normal, Hard
        self.fps = 8
        self.info = False
        self.sound = True # effects
        self.music = True 
        self.game_mode = "Classic"  # Classic, Advanced
        
    def updateFPS(self):
        """Aktualizuje FPS na podstawie trudności"""
        if self.difficulty == "Easy":
            self.fps = 4
        elif self.difficulty == "Normal":
            self.fps = 8
        elif self.difficulty == "Hard":
            self.fps = 12

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.settings = GameSettings()
        self.jersey_font = None
        self.loadFonts()
        
    def loadFonts(self):
        """Ładuje niestandardowe czcionki"""
        try:
            self.jersey_font = p.font.Font("Jersey10-Regular.ttf", 80)
        except:
            print("Jersey 10 font not found, using default")
            self.jersey_font = p.font.Font(None, 80)
    
    def showMain(self, screen, clock):
        """Menu główne z logo"""
        font_button = p.font.Font(None, 45)
        font_small = p.font.Font(None, 35)
        
        # Logo - full screen background
        try:
            logo = p.image.load("img/menu.png")
            logo = p.transform.scale(logo, (self.width, 780))  # 720x780
        except:
            logo = None
        
        # Przyciski trudności (strzałki) - obok głowy węża
        difficulties = ["Easy", "Normal", "Hard"]
        diff_index = difficulties.index(self.settings.difficulty)
        
        left_arrow = p.Rect(250, 470, 40, 40)
        right_arrow = p.Rect(450, 470, 40, 40)
        diff_rect = p.Rect(210, 470, 320, 50)
        
        # Przyciski trybu gry - niżej
        classic_btn = p.Rect(170, 570, 160, 60)
        advanced_btn = p.Rect(400, 570, 160, 60)
        
        # Przyciski górne (info i muzyka)
        info_btn = p.Rect(self.width - 160, 20, 40, 40)
        music_btn = p.Rect(self.width - 60, 20, 40, 40)
        sound_btn = p.Rect(self.width - 110, 20, 40, 40)
        
        # Przycisk START - na dole
        start_btn = p.Rect(self.width//2 - 125, 660, 250, 70)
        
        while True:
            # Białe tło
            screen.fill((255, 255, 255))
            
            # Logo jako tło na cały ekran
            if logo:
                screen.blit(logo, (0, 0))
            else:
                title = self.jersey_font.render("Snake Game", True, (50, 50, 50))
                screen.blit(title, (self.width//2 - title.get_width()//2, 100))
            
            mouse_pos = p.mouse.get_pos()
            
            # === DIFFICULTY SELECTOR ===
            # Usunięty label "Difficulty:" - nie jest potrzebny
            
            # Strzałka lewa
            color = (102, 75, 166) if left_arrow.collidepoint(mouse_pos) else (179, 164, 214)
            p.draw.polygon(screen, color, [
                (left_arrow.right - 5, left_arrow.top + 5),
                (left_arrow.left + 5, left_arrow.centery),
                (left_arrow.right - 5, left_arrow.bottom - 5)
            ])
            
            # Trudność - sam tekst bez ramki
            diff_text = font_button.render(self.settings.difficulty, True, (50, 50, 50))
            screen.blit(diff_text, (diff_rect.centerx - diff_text.get_width()//2,
                                   diff_rect.centery - diff_text.get_height()//2))
            
            # Strzałka prawa
            color = (102, 75, 166) if right_arrow.collidepoint(mouse_pos) else (179, 164, 214)
            p.draw.polygon(screen, color, [
                (right_arrow.left + 5, right_arrow.top + 5),
                (right_arrow.right - 5, right_arrow.centery),
                (right_arrow.left + 5, right_arrow.bottom - 5)
            ])
            
            # === GAME MODE ===
            # Classic
            is_classic = self.settings.game_mode == "Classic"
            color = (179, 164, 214) if is_classic else (200, 210, 220)
            border_color = (102, 75, 166) if is_classic else (150, 150, 150)
            p.draw.rect(screen, color, classic_btn, border_radius=10)
            p.draw.rect(screen, border_color, classic_btn, 3, border_radius=10)
            text = font_small.render("Classic", True, (50, 50, 50))
            screen.blit(text, (classic_btn.centerx - text.get_width()//2,
                              classic_btn.centery - text.get_height()//2))
            
            # Advanced
            is_advanced = self.settings.game_mode == "Advanced"
            color = (179, 164, 214) if is_advanced else (200, 210, 220)
            border_color = (102, 75, 166) if is_advanced else (150, 150, 150)
            p.draw.rect(screen, color, advanced_btn, border_radius=10)
            p.draw.rect(screen, border_color, advanced_btn, 3, border_radius=10)
            text = font_small.render("Advanced", True, (50, 50, 50))
            screen.blit(text, (advanced_btn.centerx - text.get_width()//2,
                              advanced_btn.centery - text.get_height()//2))
            
            # === START BUTTON ===
            color = (102, 75, 166) if start_btn.collidepoint(mouse_pos) else (179, 164, 214)
            p.draw.rect(screen, color, start_btn, border_radius=15)
            p.draw.rect(screen, (102, 75, 166), start_btn, 4, border_radius=15)
            text = font_button.render("START", True, (50, 50, 50))
            screen.blit(text, (start_btn.centerx - text.get_width()//2,
                              start_btn.centery - text.get_height()//2))
            
            # === TOP BUTTONS ===
            # Info button (i)
            color = (179, 164, 214) if self.settings.info else (150, 150, 150)
            p.draw.circle(screen, color, info_btn.center, 20)
            info_text = font_button.render("i", True, (255, 255, 255))
            screen.blit(info_text, (info_btn.centerx - info_text.get_width()//2,
                                   info_btn.centery - info_text.get_height()//2 - 2))
            
            # Music button (♪)
            small_font = p.font.Font(None, 20)

            color = (179, 164, 214) if self.settings.music else (150, 150, 150)
            if music_btn.collidepoint(mouse_pos):
                color = tuple(min(c + 30, 255) for c in color)
            p.draw.circle(screen, color, music_btn.center, 20)
            music = "Music"
            music_text = small_font.render(music, True, (255, 255, 255))
            screen.blit(music_text, (music_btn.centerx - music_text.get_width()//2,
                                    music_btn.centery - music_text.get_height()//2))
            
            color = (179, 164, 214) if self.settings.sound else (150, 150, 150)
            if sound_btn.collidepoint(mouse_pos):
                color = tuple(min(c + 30, 255) for c in color)
            p.draw.circle(screen, color, sound_btn.center, 20)
            symbol = "SFX"
            txt = small_font.render(symbol, True, (255, 255, 255))
            screen.blit(txt, (
                sound_btn.centerx - txt.get_width() // 2,
                sound_btn.centery - txt.get_height() // 2
            ))

            # === INFO PANEL ===
            if self.settings.info:
                self.drawInfoPanel(screen, font_small)
            
            # === EVENTS ===
            for e in p.event.get():
                if e.type == p.QUIT:
                    return "EXIT"
                elif e.type == p.MOUSEBUTTONDOWN:
                    if start_btn.collidepoint(mouse_pos):
                        self.settings.updateFPS()
                        return "PLAY"
                    elif left_arrow.collidepoint(mouse_pos):
                        diff_index = (diff_index - 1) % len(difficulties)
                        self.settings.difficulty = difficulties[diff_index]
                    elif right_arrow.collidepoint(mouse_pos):
                        diff_index = (diff_index + 1) % len(difficulties)
                        self.settings.difficulty = difficulties[diff_index]
                    elif classic_btn.collidepoint(mouse_pos):
                        self.settings.game_mode = "Classic"
                    elif advanced_btn.collidepoint(mouse_pos):
                        self.settings.game_mode = "Advanced"
                    elif info_btn.collidepoint(mouse_pos):
                        self.settings.info = not self.settings.info
                    elif music_btn.collidepoint(mouse_pos):
                        self.sound.toggle_music()
                    elif sound_btn.collidepoint(mouse_pos):
                        self.settings.sound = not self.settings.sound
            
            p.display.flip()
            clock.tick(60)
    
    def drawInfoPanel(self, screen, font):
        """Rysuje panel informacyjny"""
        panel = p.Rect(100, 150, self.width - 200, 450)
        p.draw.rect(screen, (255, 255, 255), panel, border_radius=15)
        p.draw.rect(screen, (102, 75, 166), panel, 4, border_radius=15)
        
        # Tytuł
        title = font.render("CONTROLS & INFO", True, (50, 50, 50))
        screen.blit(title, (panel.centerx - title.get_width()//2, panel.top + 20))
        
        # Instrukcje
        instructions = [
            "                      Arrow Keys - Move snake",
            "                         P or ESC - Pause game",
            "       Difficulty level changes the speed of a snake",
            "Classic Mode:",
            "  Eat apples and grow longer",
            "  Don't touch the border",
            "Advanced Mode:",
            "  Enemies appear!",
            "  Press X to shoot lasers",
            "  Don't touch the enemies!",
            "",
            "                   Try to survive and get high score!"
        ]
        
        y = panel.top + 70
        font_small = p.font.Font(None, 28)
        for line in instructions:
            text = font_small.render(line, True, (50, 50, 50))
            screen.blit(text, (panel.left + 30, y))
            y += 30
    
    def showGameOver(self, screen, clock, score, play_time):
        """Ekran Game Over"""
        font_title = p.font.Font(None, 80)
        font_text = p.font.Font(None, 40)
        
        minutes = int(play_time // 60)
        seconds = int(play_time % 60)
        
        while True:
            screen.fill((230, 240, 250))
            
            title = font_title.render("GAME OVER", True, (200, 50, 50))
            screen.blit(title, (self.width//2 - title.get_width()//2, 150))
            
            score_text = font_text.render(f"Final Score: {score}", True, (50, 50, 50))
            screen.blit(score_text, (self.width//2 - score_text.get_width()//2, 280))
            
            time_text = font_text.render(f"Time: {minutes:02d}:{seconds:02d}", True, (50, 50, 50))
            screen.blit(time_text, (self.width//2 - time_text.get_width()//2, 340))
            
            diff_text = font_text.render(f"Difficulty: {self.settings.difficulty}", True, (50, 50, 50))
            screen.blit(diff_text, (self.width//2 - diff_text.get_width()//2, 400))
            
            mode_text = font_text.render(f"Mode: {self.settings.game_mode}", True, (50, 50, 50))
            screen.blit(mode_text, (self.width//2 - mode_text.get_width()//2, 460))
            
            continue_text = font_text.render("Press SPACE to continue", True, (100, 100, 100))
            screen.blit(continue_text, (self.width//2 - continue_text.get_width()//2, 550))
            
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    exit()
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_SPACE or e.key == p.K_RETURN:
                        return
            
            p.display.flip()
            clock.tick(60)
    
    def drawUI(self, screen, score, play_time, snake_length, paused, ui_height):
        """Rysuje UI podczas gry"""
        p.draw.rect(screen, (30, 30, 40), (0, 0, self.width, ui_height))
        
        font = p.font.Font(None, 36)
        
        # Czas
        minutes = int(play_time // 60)
        seconds = int(play_time % 60)
        time_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        screen.blit(time_text, (20, 25))
        
        # Wynik
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (220, 25))
        
        # Trudność
        diff_text = font.render(f"{self.settings.difficulty}", True, (255, 255, 100))
        screen.blit(diff_text, (420, 25))
        
        # Tryb gry (jeśli Advanced)
        if self.settings.game_mode == "Advanced":
            mode_text = font.render("ADV", True, (255, 100, 100))
            screen.blit(mode_text, (600, 25))
        
        # Pauza
        if paused:
            pause_font = p.font.Font(None, 80)
            pause_text = pause_font.render("PAUSED", True, (102, 75, 166))
            screen.blit(pause_text, (self.width//2 - pause_text.get_width()//2, 
                                     self.height//2 + ui_height - pause_text.get_height()//2))