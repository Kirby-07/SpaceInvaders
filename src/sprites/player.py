import pygame
from src.sprites.bullet import Bullet
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, bullets_group, screen_width, screen_height, audio_manager):
        super().__init__()
        self.audio_manager = audio_manager
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Cargar nave aleatoria
        ship_types = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        ship_type = random.choice(ship_types)
        image_path = f'assets/images/ship_{ship_type}.png'
        self.image = pygame.image.load(image_path).convert_alpha()
        # Escalar a tamaño deseado (50x40)
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        
        self.speed = 5
        self.all_sprites = all_sprites
        self.bullets_group = bullets_group
        self.last_shot = 0
        self.shoot_delay = 250  # Milisegundos entre disparos
        
        # Sistema de armas
        self.weapon_type = 'normal'  # Tipos: 'normal', 'double', 'triple', 'rapid'
        self.weapon_duration = 0  # Tiempo restante del power-up (en milisegundos)
        self.weapon_start_time = 0
        
        # Cargar sonido de disparo
        self.laser_sound = pygame.mixer.Sound('assets/sounds/laserRetro_002.ogg')

    def update(self, vision_movement=None, vision_shoot=False):
        # Movimiento por teclado
        keys = pygame.key.get_pressed()
        
        # Movimiento: Teclado O Visión
        if keys[pygame.K_LEFT] or vision_movement == 'LEFT':
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or vision_movement == 'RIGHT':
            self.rect.x += self.speed
            
        # Disparo: Espacio O Gesto de Visión
        if keys[pygame.K_SPACE] or vision_shoot:
            self.shoot()

        # Mantener dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        
        # Verificar si el power-up expiró
        if self.weapon_type != 'normal':
            current_time = pygame.time.get_ticks()
            if current_time - self.weapon_start_time > self.weapon_duration:
                self.weapon_type = 'normal'
                self.shoot_delay = 250  # Restaurar velocidad normal
    
    def activate_powerup(self, powerup_type):
        """Activa un power-up de arma."""
        self.weapon_type = powerup_type
        self.weapon_start_time = pygame.time.get_ticks()
        self.weapon_duration = 15000  # 15 segundos
        
        # Ajustar velocidad de disparo si es 'rapid'
        if powerup_type == 'rapid':
            self.shoot_delay = 100  # Disparo más rápido
        else:
            self.shoot_delay = 250  # Velocidad normal

    def shoot(self):
        """Dispara según el tipo de arma actual."""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            # Reproducir sonido de disparo
            self.laser_sound.set_volume(self.audio_manager.sfx_volume)
            self.laser_sound.play()
            
            if self.weapon_type == 'normal':
                # Disparo normal (1 bala al centro)
                bullet = Bullet(self.rect.centerx, self.rect.top)
                self.all_sprites.add(bullet)
                self.bullets_group.add(bullet)
                
            elif self.weapon_type == 'double':
                # Disparo doble (2 balas a los lados)
                bullet1 = Bullet(self.rect.left + 10, self.rect.top)
                bullet2 = Bullet(self.rect.right - 10, self.rect.top)
                self.all_sprites.add(bullet1, bullet2)
                self.bullets_group.add(bullet1, bullet2)
                
            elif self.weapon_type == 'triple':
                # Disparo triple (3 balas: izquierda, centro, derecha)
                bullet1 = Bullet(self.rect.left + 5, self.rect.top)
                bullet2 = Bullet(self.rect.centerx, self.rect.top)
                bullet3 = Bullet(self.rect.right - 5, self.rect.top)
                self.all_sprites.add(bullet1, bullet2, bullet3)
                self.bullets_group.add(bullet1, bullet2, bullet3)
                
            elif self.weapon_type == 'rapid':
                # Disparo rápido (1 bala pero con menor delay)
                bullet = Bullet(self.rect.centerx, self.rect.top)
                self.all_sprites.add(bullet)
                self.bullets_group.add(bullet)