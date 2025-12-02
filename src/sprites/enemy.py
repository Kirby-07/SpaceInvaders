import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Cargar imagen de enemigo aleatoria
        enemy_types = ['A', 'B', 'C', 'D', 'E']
        enemy_type = random.choice(enemy_types)
        image_path = f'assets/images/enemy_{enemy_type}.png'
        self.image = pygame.image.load(image_path).convert_alpha()
        # Escalar a tamaño deseado (30x20)
        self.image = pygame.transform.scale(self.image, (30, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movimiento horizontal más variado
        self.speed_x = random.choice([2, 3, 4, 5])  # Velocidad horizontal variable
        self.speed_y = 0  # Velocidad vertical inicial
        
        # Comportamiento impredecible
        self.drop_speed = random.randint(20, 40)  # Caída variable cuando toca bordes
        self.change_direction_chance = 0.03  # 3% de probabilidad de cambiar dirección
        self.vertical_movement_chance = 0.02  # 2% de probabilidad de moverse verticalmente
        
        self.drop_chance = 0.2  # 20% de probabilidad de soltar power-up
        
        # Contador para movimiento vertical
        self.vertical_movement_timer = 0
        self.vertical_movement_duration = random.randint(30, 60)  # Frames que dura el movimiento vertical

    def update(self):
        # Movimiento horizontal
        self.rect.x += self.speed_x
        
        # Cambio de dirección horizontal aleatorio (más frecuente)
        if random.random() < self.change_direction_chance:
            self.speed_x *= -1
            # A veces también cambia de velocidad
            if random.random() < 0.5:
                self.speed_x = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        
        # Movimiento vertical aleatorio
        if self.vertical_movement_timer > 0:
            self.rect.y += self.speed_y
            self.vertical_movement_timer -= 1
        else:
            # Posibilidad de iniciar movimiento vertical
            if random.random() < self.vertical_movement_chance:
                self.speed_y = random.choice([1, 2, -1])  # Puede subir o bajar
                self.vertical_movement_timer = random.randint(20, 50)
        
        # Rebotar en los bordes y bajar (comportamiento clásico)
        if self.rect.right >= self.screen_width or self.rect.left <= 0:
            self.speed_x *= -1
            self.rect.y += self.drop_speed
            # Variar la velocidad después de rebotar
            if random.random() < 0.3:
                self.drop_speed = random.randint(20, 40)
        
        # Limitar movimiento vertical para que no salgan de la pantalla por arriba
        if self.rect.top < 30:  # No subir más allá del HUD
            self.rect.top = 30
            self.speed_y = 0
            self.vertical_movement_timer = 0
        
        # Eliminar enemigo si sale de la pantalla por abajo
        if self.rect.top > self.screen_height:
            self.kill()
    
    def drop_powerup(self):
        """
        Retorna un tipo de power-up aleatorio si pasa la probabilidad.
        Retorna None si no suelta nada.
        """
        if random.random() < self.drop_chance:
            # Elegir tipo aleatorio
            powerup_types = ['double', 'triple', 'rapid']
            return random.choice(powerup_types)
        return None