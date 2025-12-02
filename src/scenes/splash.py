import pygame
import sys
import random
import math
from src.config import WHITE, BLACK, FPS

class Splash:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font_title = pygame.font.Font(None, 120)
        self.font_subtitle = pygame.font.Font(None, 40)
        
        # Estrellas de fondo
        self.stars = []
        for _ in range(100):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            speed = random.uniform(0.5, 2.0)
            self.stars.append([x, y, speed])
        
        self.alpha = 0  # Para efecto fade-in
        self.blink_timer = 0
        self.show_text = True
        
    def update_stars(self):
        """Anima las estrellas moviéndolas hacia abajo"""
        for star in self.stars:
            star[1] += star[2]
            if star[1] > self.screen_height:
                star[1] = 0
                star[0] = random.randint(0, self.screen_width)
    
    def draw(self):
        """Dibuja la pantalla de splash"""
        self.screen.fill(BLACK)
        
        # Dibujar estrellas
        for star in self.stars:
            brightness = int(255 * (star[2] / 2.0))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (int(star[0]), int(star[1])), 2)
        
        # Título con fade-in
        if self.alpha < 255:
            self.alpha += 3
        
        title_surface = self.font_title.render("SPACE INVADER", True, WHITE)
        title_surface.set_alpha(self.alpha)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(title_surface, title_rect)
        
        # Texto parpadeante
        if self.alpha >= 255:
            self.blink_timer += 1
            if self.blink_timer > 30:
                self.show_text = not self.show_text
                self.blink_timer = 0
            
            if self.show_text:
                subtitle = self.font_subtitle.render("Presiona cualquier tecla para comenzar", True, (150, 150, 150))
                subtitle_rect = subtitle.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 80))
                self.screen.blit(subtitle, subtitle_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Bucle principal de la pantalla de splash"""
        clock = pygame.time.Clock()
        waiting = True
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.alpha >= 255:  # Solo permitir saltar cuando el fade-in esté completo
                        waiting = False
            
            self.update_stars()
            self.draw()
            clock.tick(FPS)
