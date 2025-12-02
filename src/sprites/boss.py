import pygame
import math
import random
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, RED, GREEN, YELLOW
from src.sprites.enemy_bullet import EnemyBullet

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, boss_type, screen_width, screen_height, audio_manager):
        super().__init__()
        self.audio_manager = audio_manager
        self.boss_type = boss_type
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        if self.boss_type == 1:
            self.width = 100
            self.height = 80
            self.hp = 20
            self.color = (255, 165, 0) # Orange
            self.speed_x = 4
            self.speed_y = 2
        else:
            self.width = 150
            self.height = 120
            self.hp = 40
            self.color = (255, 215, 0) # Gold
            self.speed_x = 5
            self.speed_y = 3
            
        self.max_hp = self.hp
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        
        self.t = 0 # Time parameter for movement
        self.attack_delay = 1000 if self.boss_type == 1 else 800
        self.last_attack = pygame.time.get_ticks()
        
        # Cargar sonido de disparo
        self.laser_sound = pygame.mixer.Sound('assets/sounds/laserRetro_003.ogg')

    def update(self):
        self.t += 0.05
        
        if self.boss_type == 1:
            # Boss 1: Horizontal sinusoidal movement + vertical bounce
            self.rect.x += self.speed_x
            self.rect.y += math.sin(self.t) * self.speed_y
            
            if self.rect.right >= self.screen_width or self.rect.left <= 0:
                self.speed_x *= -1
                
        else:
            # Boss 2: Figure-8 movement
            center_x = self.screen_width // 2
            amplitude_x = self.screen_width // 3
            amplitude_y = 50
            
            self.rect.centerx = center_x + math.sin(self.t * 0.5) * amplitude_x
            self.rect.centery = 150 + math.sin(self.t) * amplitude_y
            
        # Keep within screen
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > self.screen_height: self.rect.bottom = self.screen_height

    def attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack > self.attack_delay:
            self.last_attack = now
            # Reproducir sonido de disparo
            self.laser_sound.set_volume(self.audio_manager.sfx_volume)
            self.laser_sound.play()
            return EnemyBullet(self.rect.centerx, self.rect.bottom, self.screen_height)
        return None

    def take_damage(self, amount):
        self.hp -= amount

    def draw_health_bar(self, surface):
        bar_width = self.width
        bar_height = 10
        fill = (self.hp / self.max_hp) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 20, fill, bar_height)
        
        col = GREEN
        if self.hp < self.max_hp * 0.6: col = YELLOW
        if self.hp < self.max_hp * 0.3: col = RED
        
        pygame.draw.rect(surface, col, fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)
