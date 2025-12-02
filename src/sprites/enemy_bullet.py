import pygame
from src.config import SCREEN_HEIGHT, RED

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_height):
        super().__init__()
        self.screen_height = screen_height
        self.image = pygame.Surface((10, 20))  # Más grande
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.kill()
