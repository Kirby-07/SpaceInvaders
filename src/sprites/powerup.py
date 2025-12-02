import pygame
from src.config import WHITE, GREEN, BLUE, RED
import random

class PowerUp(pygame.sprite.Sprite):
    """Clase base para power-ups que caen cuando eliminas enemigos."""
    
    def __init__(self, x, y, powerup_type, screen_height):
        super().__init__()
        self.screen_height = screen_height
        self.powerup_type = powerup_type  # 'double', 'triple', 'rapid', 'life'
        self.speed = 3  # Velocidad de caída
        
        # Crear superficie visual según el tipo
        self.image = pygame.Surface((30, 30))
        
        # Color según el tipo de power-up
        if powerup_type == 'double':
            self.image.fill(GREEN)
            self.label = "2X"
        elif powerup_type == 'triple':
            self.image.fill(BLUE)
            self.label = "3X"
        elif powerup_type == 'rapid':
            self.image.fill(RED)
            self.label = "R"
        elif powerup_type == 'life':
            self.image.fill((0, 255, 255)) # Cyan
            self.label = "+1"
        
        # Dibujar texto en el power-up
        font = pygame.font.Font(None, 24)
        text = font.render(self.label, True, WHITE)
        text_rect = text.get_rect(center=(15, 15))
        self.image.blit(text, text_rect)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        """Hace que el power-up caiga hacia abajo."""
        self.rect.y += self.speed
        
        # Eliminar si sale de la pantalla
        if self.rect.top > self.screen_height:
            self.kill()