import pygame as p
import time

class GameSettings:
    def __init__(self):
        self.fps = 8
        self.sound = True
        self.grid_visible = True

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.settings = GameSettings()
        
    def showMain(self, screen, clock):
        """Menu główne"""
        font_title = p.font.Font(None, 80)
        font_menu = p.font.Font(None, 50)
        
        buttons = {
            "PLAY": p.Rect(self.width//2 - 100, 250, 200, 60),
            "SETTINGS": p.Rect(self.width//2 - 100, 340, 200, 60),
            "EXIT": p.Rect(self.width//2 - 100, 430, 200, 60)
        }
        
        while True:
            screen.fill((20, 20, 30))
            
            title = font_title.render("SNAKE", True, (100, 200, 100))
            screen.blit(title, (self.width//2 - title.get_width()//2, 100))
            
            # buttons
            mouse_pos = p.mouse.get_pos()
            for name, rect in buttons.items():
                color = (80, 80, 100) if rect.collidepoint(mouse_pos) else (50, 50, 70)
                p.draw.rect(screen, color, rect, border_radius=10)
                p.draw.rect(screen, (100, 200, 100), rect, 3, border_radius=10)
                
                text = font_menu.render(name, True, (255, 255, 255))
                screen.blit(text, (rect.centerx - text.get_width()//2, 
                                  rect.centery - text.get_height()//2))
            
            for e in p.event.get():
                if e.type == p.QUIT:
                    return "EXIT"
                elif e.type == p.MOUSEBUTTONDOWN:
                    for name, rect in buttons.items():
                        if rect.collidepoint(mouse_pos):
                            return name
            
            p.display.flip()
            clock.tick(60)
    
    def showSettings(self, screen, clock):
        # settings menu
        font_title = p.font.Font(None, 60)
        font_text = p.font.Font(None, 40)
        
        # slider and toggle TO BE CHANGED
        fps_slider = {"rect": p.Rect(200, 200, 320, 20), "min": 4, "max": 20}
        sound_toggle = p.Rect(self.width//2 - 30, 280, 60, 40)
        grid_toggle = p.Rect(self.width//2 - 30, 360, 60, 40)
        back_button = p.Rect(self.width//2 - 100, 500, 200, 60)
        
        dragging = False
        
        while True:
            screen.fill((20, 20, 30))
            
            title = font_title.render("SETTINGS", True, (100, 200, 100))
            screen.blit(title, (self.width//2 - title.get_width()//2, 50))
            
            # fps slider
            label = font_text.render(f"Speed: {self.settings.fps} FPS", True, (255, 255, 255))
            screen.blit(label, (200, 160))
            
            p.draw.rect(screen, (50, 50, 70), fps_slider["rect"], border_radius=10)
            slider_pos = (self.settings.fps - fps_slider["min"]) / (fps_slider["max"] - fps_slider["min"])
            handle_x = fps_slider["rect"].x + slider_pos * fps_slider["rect"].width
            p.draw.circle(screen, (100, 200, 100), (int(handle_x), fps_slider["rect"].centery), 15)
            
            # sound toggle
            label = font_text.render("Sound:", True, (255, 255, 255))
            screen.blit(label, (200, 280))
            color = (100, 200, 100) if self.settings.sound else (100, 50, 50)
            p.draw.rect(screen, color, sound_toggle, border_radius=20)
            
            # grid toggle WILL BE CHANGED
            label = font_text.render("Grid:", True, (255, 255, 255))
            screen.blit(label, (200, 360))
            color = (100, 200, 100) if self.settings.grid_visible else (100, 50, 50)
            p.draw.rect(screen, color, grid_toggle, border_radius=20)
            
            # back button
            p.draw.rect(screen, (50, 50, 70), back_button, border_radius=10)
            p.draw.rect(screen, (100, 200, 100), back_button, 3, border_radius=10)
            text = font_text.render("BACK", True, (255, 255, 255))
            screen.blit(text, (back_button.centerx - text.get_width()//2,
                              back_button.centery - text.get_height()//2))
            
            mouse_pos = p.mouse.get_pos()
            
            for e in p.event.get():
                if e.type == p.QUIT:
                    return
                elif e.type == p.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(mouse_pos):
                        return
                    elif sound_toggle.collidepoint(mouse_pos):
                        self.settings.sound = not self.settings.sound
                    elif grid_toggle.collidepoint(mouse_pos):
                        self.settings.grid_visible = not self.settings.grid_visible
                    elif fps_slider["rect"].collidepoint(mouse_pos):
                        dragging = True
                elif e.type == p.MOUSEBUTTONUP:
                    dragging = False
                elif e.type == p.MOUSEMOTION and dragging:
                    rel_x = mouse_pos[0] - fps_slider["rect"].x
                    rel_x = max(0, min(rel_x, fps_slider["rect"].width))
                    ratio = rel_x / fps_slider["rect"].width
                    self.settings.fps = int(fps_slider["min"] + ratio * (fps_slider["max"] - fps_slider["min"]))
            
            p.display.flip()
            clock.tick(60)
    
    def showGameOver(self, screen, clock, score, play_time):
        font_title = p.font.Font(None, 80)
        font_text = p.font.Font(None, 40)
        
        minutes = int(play_time // 60)
        seconds = int(play_time % 60)
        
        while True:
            screen.fill((20, 20, 30))
            
            title = font_title.render("GAME OVER", True, (200, 50, 50))
            screen.blit(title, (self.width//2 - title.get_width()//2, 150))
            
            score_text = font_text.render(f"Final Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (self.width//2 - score_text.get_width()//2, 280))
            
            time_text = font_text.render(f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
            screen.blit(time_text, (self.width//2 - time_text.get_width()//2, 340))
            
            continue_text = font_text.render("Press SPACE to continue", True, (150, 150, 150))
            screen.blit(continue_text, (self.width//2 - continue_text.get_width()//2, 450))
            
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
        # draws the ui which is displayed during the game
        p.draw.rect(screen, (30, 30, 40), (0, 0, self.width, ui_height))
        
        font = p.font.Font(None, 36)
        
        # time counter
        minutes = int(play_time // 60)
        seconds = int(play_time % 60)
        time_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        screen.blit(time_text, (20, 25))
        
        # score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (250, 25))
        
        # snake length, KINDA USELESS, WILL BE CHANGED
        length_text = font.render(f"Length: {snake_length}", True, (255, 255, 255))
        screen.blit(length_text, (450, 25))
        
        # pause, TO BE DONE -> ADD PAUSE BUTTON TO UI
        if paused:
            pause_font = p.font.Font(None, 80)
            pause_text = pause_font.render("PAUSED", True, (255, 255, 0))
            screen.blit(pause_text, (self.width//2 - pause_text.get_width()//2, 
                                     self.height//2 + ui_height - pause_text.get_height()//2))