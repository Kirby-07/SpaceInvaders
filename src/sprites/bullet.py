import pygame
from src.config import SCREEN_HEIGHT, WHITE

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Placeholder: Rectángulo blanco pequeño
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10  # Se mueve hacia arriba

    def update(self):
        self.rect.y += self.speed
        # Eliminar si sale de la pantalla
        if self.rect.bottom < 0:
            self.kill()
