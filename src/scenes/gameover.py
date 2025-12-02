import pygame
import sys
import random
from src.config import WHITE, BLACK, RED, FPS

class GameOver:
    def __init__(self, screen, score, level):
        self.screen = screen
        self.score = score
        self.level = level
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font_title = pygame.font.Font(None, 100)
        self.font_stats = pygame.font.Font(None, 50)
        self.font_countdown = pygame.font.Font(None, 40)
        
        self.alpha = 0
        self.countdown = 5  # Segundos para volver al menú
        self.last_second = pygame.time.get_ticks()
        
    def draw(self):
        """Dibuja la pantalla de Game Over"""
        # Overlay rojo semi-transparente con fade-in
        if self.alpha < 180:
            self.alpha += 5
        
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(self.alpha)
        overlay.fill((80, 0, 0))  # Rojo oscuro
        self.screen.blit(overlay, (0, 0))
        
        # Título "GAME OVER"
        title_surface = self.font_title.render("GAME OVER", True, RED)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
        self.screen.blit(title_surface, title_rect)
        
        # Estadísticas
        score_text = self.font_stats.render(f"Puntuación Final: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(score_text, score_rect)
        
        level_text = self.font_stats.render(f"Nivel Alcanzado: {self.level}", True, WHITE)
        level_rect = level_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 60))
        self.screen.blit(level_text, level_rect)
        
        # Countdown
        countdown_text = self.font_countdown.render(f"Volviendo al menú en {self.countdown}...", True, (200, 200, 200))
        countdown_rect = countdown_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 150))
        self.screen.blit(countdown_text, countdown_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Bucle principal de Game Over"""
        clock = pygame.time.Clock()
        
        while self.countdown > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Permitir saltar el countdown con cualquier tecla
                    return
            
            # Actualizar countdown
            now = pygame.time.get_ticks()
            if now - self.last_second >= 1000:
                self.countdown -= 1
                self.last_second = now
            
            self.draw()
            clock.tick(FPS)
