import pygame
import sys
import random
import math
from src.config import WHITE, BLACK, GREEN, FPS

class Victory:
    def __init__(self, screen, score):
        self.screen = screen
        self.score = score
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font_title = pygame.font.Font(None, 120)
        self.font_stats = pygame.font.Font(None, 50)
        self.font_countdown = pygame.font.Font(None, 40)
        
        self.alpha = 0
        self.countdown = 5
        self.last_second = pygame.time.get_ticks()
        
        # Partículas de confetti
        self.particles = []
        for _ in range(150):
            x = random.randint(0, self.screen_width)
            y = random.randint(-self.screen_height, 0)
            vx = random.uniform(-2, 2)
            vy = random.uniform(2, 5)
            color = random.choice([(255, 215, 0), (0, 255, 0), (255, 255, 255), (0, 255, 255)])
            self.particles.append([x, y, vx, vy, color])
        
        self.pulse = 0
    
    def update_particles(self):
        """Anima las partículas de confetti"""
        for particle in self.particles:
            particle[0] += particle[2]  # x
            particle[1] += particle[3]  # y
            
            # Reiniciar si sale de la pantalla
            if particle[1] > self.screen_height:
                particle[0] = random.randint(0, self.screen_width)
                particle[1] = random.randint(-100, 0)
    
    def draw(self):
        """Dibuja la pantalla de Victoria"""
        # Overlay verde/dorado semi-transparente con fade-in
        if self.alpha < 180:
            self.alpha += 5
        
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(self.alpha)
        overlay.fill((0, 60, 0))  # Verde oscuro
        self.screen.blit(overlay, (0, 0))
        
        # Dibujar partículas
        for particle in self.particles:
            pygame.draw.circle(self.screen, particle[4], (int(particle[0]), int(particle[1])), 4)
        
        # Título "¡VICTORIA!" con efecto de pulso
        self.pulse += 0.1
        pulse_scale = 1 + 0.1 * math.sin(self.pulse)
        title_size = int(120 * pulse_scale)
        font_pulsing = pygame.font.Font(None, title_size)
        
        title_surface = font_pulsing.render("¡VICTORIA!", True, (255, 215, 0))  # Dorado
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
        self.screen.blit(title_surface, title_rect)
        
        # Estadísticas
        score_text = self.font_stats.render(f"Puntuación Final: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 20))
        self.screen.blit(score_text, score_rect)
        
        congrats_text = self.font_stats.render("¡Has completado todos los niveles!", True, GREEN)
        congrats_rect = congrats_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 80))
        self.screen.blit(congrats_text, congrats_rect)
        
        # Countdown
        countdown_text = self.font_countdown.render(f"Volviendo al menú en {self.countdown}...", True, (200, 200, 200))
        countdown_rect = countdown_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 150))
        self.screen.blit(countdown_text, countdown_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Bucle principal de Victoria"""
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
            
            self.update_particles()
            self.draw()
            clock.tick(FPS)
