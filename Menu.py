import pygame as p

class GameSettings:
    def __init__(self):
        self.difficulty = "Normal"  # easy, normal, hard
        self.fps = 8
        self.sound = True  # sound effects
        self.music = True 
        self.game_mode = "Classic"  # classic, advanced
        
    def updateFPS(self):
        # update fps based on difficulty level
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
    
    def showMain(self, screen, clock):
        # main menu with logo and game options
        font_button = p.font.Font("fonts/Jersey10-Regular.ttf", 50)
        font_small = p.font.Font("fonts/Jersey10-Regular.ttf", 18)
        iFont = p.font.Font("fonts/Jersey10-Regular.ttf", 25)
        modeFont = p.font.Font("fonts/Jersey10-Regular.ttf", 40)
        
        try:
            logo = p.image.load("img/menu.png")
            logo = p.transform.scale(logo, (self.width, 780))
        except:
            logo = None
        
        # difficulty selector arrows
        difficulties = ["Easy", "Normal", "Hard"]
        diff_index = difficulties.index(self.settings.difficulty)
        
        left_arrow = p.Rect(250, 470, 40, 40)
        right_arrow = p.Rect(450, 470, 40, 40)
        diff_rect = p.Rect(210, 470, 320, 50)
        
        # game mode buttons
        classic_btn = p.Rect(170, 570, 160, 60)
        advanced_btn = p.Rect(400, 570, 160, 60)
        
        # top right control buttons
        info_btn = p.Rect(self.width - 160, 20, 40, 40)
        music_btn = p.Rect(self.width - 60, 20, 40, 40)
        sound_btn = p.Rect(self.width - 110, 20, 40, 40)
        
        # start game button
        start_btn = p.Rect(self.width//2 - 125, 660, 250, 70)
        
        # track info panel visibility
        show_info = False
        
        while True:
            screen.fill((255, 255, 255))
            
            # display logo or title
            if logo:
                screen.blit(logo, (0, 0))
            else:
                jersey_font = p.font.Font("fonts/Jersey10-Regular.ttf", 80)
                title = jersey_font.render("Snake Game", True, (50, 50, 50))
                screen.blit(title, (self.width//2 - title.get_width()//2, 100))
                
            mouse_pos = p.mouse.get_pos()
            
            # difficulty controls (disabled in advanced mode)
            if self.settings.game_mode == "Advanced":
                left_arrow_color = right_arrow_color = (180, 180, 180)
                diff_text_color = (150, 150, 150)
            else:
                left_arrow_color = (102, 75, 166) if left_arrow.collidepoint(mouse_pos) else (179, 164, 214)
                right_arrow_color = (102, 75, 166) if right_arrow.collidepoint(mouse_pos) else (179, 164, 214)
                diff_text_color = (50, 50, 50)
            
            # draw left arrow
            p.draw.polygon(screen, left_arrow_color, [
                (left_arrow.right - 5, left_arrow.top + 5),
                (left_arrow.left + 5, left_arrow.centery),
                (left_arrow.right - 5, left_arrow.bottom - 5)
            ])
            
            # draw difficulty text
            diff_text = font_button.render(self.settings.difficulty, True, diff_text_color)
            screen.blit(diff_text, (diff_rect.centerx - diff_text.get_width()//2,
                        diff_rect.centery - diff_text.get_height()//2))

            # draw right arrow
            p.draw.polygon(screen, right_arrow_color, [
                (right_arrow.left + 5, right_arrow.top + 5),
                (right_arrow.right - 5, right_arrow.centery),
                (right_arrow.left + 5, right_arrow.bottom - 5)
            ])
            
            # classic mode button
            is_classic = self.settings.game_mode == "Classic"
            color = (179, 164, 214) if is_classic else (200, 210, 220)
            border_color = (102, 75, 166) if is_classic else (150, 150, 150)
            p.draw.rect(screen, color, classic_btn, border_radius=10)
            p.draw.rect(screen, border_color, classic_btn, 3, border_radius=10)
            text = modeFont.render("Classic", True, (50, 50, 50))
            screen.blit(text, (classic_btn.centerx - text.get_width()//2,
                              classic_btn.centery - text.get_height()//2))
            
            # advanced mode button
            is_advanced = self.settings.game_mode == "Advanced"
            color = (179, 164, 214) if is_advanced else (200, 210, 220)
            border_color = (102, 75, 166) if is_advanced else (150, 150, 150)
            p.draw.rect(screen, color, advanced_btn, border_radius=10)
            p.draw.rect(screen, border_color, advanced_btn, 3, border_radius=10)
            text = modeFont.render("Advanced", True, (50, 50, 50))
            screen.blit(text, (advanced_btn.centerx - text.get_width()//2,
                              advanced_btn.centery - text.get_height()//2))
            
            # start button
            color = (102, 75, 166) if start_btn.collidepoint(mouse_pos) else (179, 164, 214)
            p.draw.rect(screen, color, start_btn, border_radius=15)
            p.draw.rect(screen, (102, 75, 166), start_btn, 4, border_radius=15)
            text = font_button.render("START", True, (50, 50, 50))
            screen.blit(text, (start_btn.centerx - text.get_width()//2,
                              start_btn.centery - text.get_height()//2))
            
            # info button (i)
            color = (179, 164, 214) if show_info else (150, 150, 150)
            p.draw.circle(screen, color, info_btn.center, 20)
            info_text = iFont.render("i", True, (255, 255, 255))
            screen.blit(info_text, (info_btn.centerx - info_text.get_width()//2,
                                   info_btn.centery - info_text.get_height()//2 - 2))
            
            # music toggle button
            color = (179, 164, 214) if self.settings.music else (150, 150, 150)
            if music_btn.collidepoint(mouse_pos):
                color = tuple(min(c + 30, 255) for c in color)
            p.draw.circle(screen, color, music_btn.center, 20)
            music_text = font_small.render("Music", True, (255, 255, 255))
            screen.blit(music_text, (music_btn.centerx - music_text.get_width()//2,
                                    music_btn.centery - music_text.get_height()//2))
            
            # sound effects toggle button
            color = (179, 164, 214) if self.settings.sound else (150, 150, 150)
            if sound_btn.collidepoint(mouse_pos):
                color = tuple(min(c + 30, 255) for c in color)
            p.draw.circle(screen, color, sound_btn.center, 20)
            txt = font_small.render("SFX", True, (255, 255, 255))
            screen.blit(txt, (
                sound_btn.centerx - txt.get_width() // 2,
                sound_btn.centery - txt.get_height() // 2
            ))

            # show info popup if toggled
            if show_info:
                self.drawInfoPanel(screen)
            
            # handle events
            for e in p.event.get():
                if e.type == p.QUIT:
                    return "EXIT"
                elif e.type == p.MOUSEBUTTONDOWN:
                    # difficulty arrows (only in classic mode)
                    if self.settings.game_mode != "Advanced":
                        if left_arrow.collidepoint(mouse_pos):
                            diff_index = (diff_index - 1) % len(difficulties)
                            self.settings.difficulty = difficulties[diff_index]
                        elif right_arrow.collidepoint(mouse_pos):
                            diff_index = (diff_index + 1) % len(difficulties)
                            self.settings.difficulty = difficulties[diff_index]
                    
                    # start game
                    if start_btn.collidepoint(mouse_pos):
                        self.settings.updateFPS()
                        return "PLAY"
                    
                    # mode selection
                    elif classic_btn.collidepoint(mouse_pos):
                        self.settings.game_mode = "Classic"
                    elif advanced_btn.collidepoint(mouse_pos):
                        self.settings.game_mode = "Advanced"
                        self.settings.difficulty = "Hard"
                    
                    # info panel toggle
                    elif info_btn.collidepoint(mouse_pos):
                        show_info = not show_info
                    
                    # music toggle
                    elif music_btn.collidepoint(mouse_pos):
                        self.settings.music = not self.settings.music
                        if self.settings.music:
                            self.sound.play_music()
                        else:
                            self.sound.stop_music()
                    
                    # sound effects toggle
                    elif sound_btn.collidepoint(mouse_pos):
                        self.settings.sound = not self.settings.sound
            
            p.display.flip()
            clock.tick(60)

    def drawInfoPanel(self, screen):
        # display controls and game info popup
        panel = p.Rect(100, 150, self.width - 200, 450)
        p.draw.rect(screen, (255, 255, 255), panel, border_radius=15)
        p.draw.rect(screen, (102, 75, 166), panel, 4, border_radius=15)
        
        font = p.font.Font("fonts/Jersey10-Regular.ttf",40)
        title = font.render("CONTROLS & INFO", True, (70, 70, 70))
        screen.blit(title, (panel.centerx - title.get_width()//2, panel.top + 20))
        
        instructions = [
            "                 Arrow Keys - Move snake",
            "                    P or ESC - Pause game",
            "Difficulty level changes the speed of a snake",
            "Classic Mode:",
            "  - Eat apples and grow longer",
            "  - Don't touch the border",
            "Advanced Mode:",
            "  - Enemies appear",
            "  - Press X to shoot lasers",
            "  - Don't touch the enemies and your lasers!",
            "",
            "       Try to survive and get high score!"
        ]
        
        # render instruction lines
        y = panel.top + 70
        font_small = p.font.Font("fonts/Jersey10-Regular.ttf", 30)
        for line in instructions:
            text = font_small.render(line, True, (50, 50, 50))
            screen.blit(text, (panel.left + 30, y))
            y += 30
    
    def showGameOver(self, screen, clock, score, play_time):
        # display game over screen with stats
        font_title = p.font.Font("fonts/Jersey10-Regular.ttf", 80)
        font_text = p.font.Font("fonts/Jersey10-Regular.ttf", 40)
        
        minutes = int(play_time // 60)
        seconds = int(play_time % 60)
        
        while True:
            screen.fill((230, 240, 250))        
            
            # game over panel
            panel = p.Rect(self.width//2 - 260, 200, 520, 360)
            p.draw.rect(screen, (245, 240, 255), panel, border_radius=20)
            p.draw.rect(screen, (102, 75, 166), panel, 4, border_radius=20)

            y = panel.top + 30

            # title
            title = font_title.render("GAME OVER", True, (200, 50, 50))
            screen.blit(title, (self.width//2 - title.get_width()//2, y))
            y += 90

            # final score
            score_text = font_text.render(f"Final Score: {score}", True, (50, 50, 50))
            screen.blit(score_text, (self.width//2 - score_text.get_width()//2, y))
            y += 50

            # play time
            time_text = font_text.render(f"Time: {minutes:02d}:{seconds:02d}", True, (50, 50, 50))
            screen.blit(time_text, (self.width//2 - time_text.get_width()//2, y))
            y += 50

            # difficulty level
            diff_text = font_text.render(f"Difficulty: {self.settings.difficulty}", True, (50, 50, 50))
            screen.blit(diff_text, (self.width//2 - diff_text.get_width()//2, y))
            y += 50

            # game mode
            mode_text = font_text.render(f"Mode: {self.settings.game_mode}", True, (50, 50, 50))
            screen.blit(mode_text, (self.width//2 - mode_text.get_width()//2, y))

            # restart hint
            hint_font = p.font.Font("fonts/Jersey10-Regular.ttf", 22)
            hint = hint_font.render("Press SPACE to restart", True, (90, 70, 150))
            screen.blit(
                hint,
                (self.width//2 - hint.get_width()//2,
                 panel.bottom - 40)
            )

            # handle events
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    exit()
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_SPACE or e.key == p.K_RETURN:
                        return
            
            p.display.flip()
            clock.tick(60)
    
    def drawUI(self, screen, score, play_time, paused, ui_height):
        # draw top ui bar with game info and controls
        bg_color = (225, 215, 245)   
        border_color = (102, 75, 166)
        text_color = (50, 50, 50)

        # ui background
        ui_rect = p.Rect(0, 0, self.width, ui_height)
        p.draw.rect(screen, bg_color, ui_rect)
        p.draw.line(screen, border_color, (0, ui_height-1), (self.width, ui_height-1), 3)

        font_small = p.font.Font("fonts/Jersey10-Regular.ttf", 16)
        font_medium = p.font.Font("fonts/Jersey10-Regular.ttf", 26)

        # time display
        minutes = int(play_time // 60)
        seconds = int(play_time % 60)
        time_text = font_medium.render(f"TIME {minutes:02d}:{seconds:02d}", True, text_color)
        screen.blit(time_text, (20, 18))

        # score display
        score_text = font_medium.render(f"SCORE {score}", True, text_color)
        screen.blit(score_text, (140, 18))

        # difficulty display
        diff_text = font_medium.render("Difficulty: " + self.settings.difficulty.upper(), True, (90, 70, 150))
        screen.blit(diff_text, (240, 18))

        # mode display (only in advanced)
        if self.settings.game_mode == "Advanced":
            mode_text = font_medium.render("Mode: Advanced", True, (200, 70, 90))
            screen.blit(mode_text, (400, 18))

        # control buttons
        music_btn = p.Rect(self.width - 110, 10, 40, 40)
        sound_btn = p.Rect(self.width - 60, 10, 40, 40)
        pause_btn = p.Rect(self.width - 160, 10, 40, 40)

        mouse_pos = p.mouse.get_pos()

        # music button
        color = (179, 164, 214) if self.settings.music else (150, 150, 150)
        if music_btn.collidepoint(mouse_pos):
            color = tuple(min(c + 20, 255) for c in color)
        p.draw.circle(screen, color, music_btn.center, 18)
        txt = font_small.render("Music", True, (255, 255, 255))
        screen.blit(txt, (music_btn.centerx - txt.get_width()//2,
                          music_btn.centery - txt.get_height()//2))

        # sfx button
        color = (179, 164, 214) if self.settings.sound else (150, 150, 150)
        if sound_btn.collidepoint(mouse_pos):
            color = tuple(min(c + 20, 255) for c in color)
        p.draw.circle(screen, color, sound_btn.center, 18)
        txt = font_small.render("SFX", True, (255, 255, 255))
        screen.blit(txt, (sound_btn.centerx - txt.get_width()//2,
                          sound_btn.centery - txt.get_height()//2))
        
        # pause button
        color = (179, 164, 214) if paused else (150, 150, 150)
        if pause_btn.collidepoint(mouse_pos):
            color = tuple(min(c + 20, 255) for c in color)
        
        p.draw.circle(screen, color, pause_btn.center, 18)
        txt = font_small.render("||", True, (255, 255, 255))
        screen.blit(
            txt,
            (pause_btn.centerx - txt.get_width()//2,
             pause_btn.centery - txt.get_height()//2)
        )

        # pause overlay
        if paused:
            overlay = p.Surface((self.width, self.height), p.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, ui_height))

            pause_font = p.font.Font("fonts/Jersey10-Regular.ttf", 90)
            pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
            screen.blit(
                pause_text,
                (self.width//2 - pause_text.get_width()//2,
                 self.height//2 + ui_height - pause_text.get_height()//2)
            )
        
        return pause_btn