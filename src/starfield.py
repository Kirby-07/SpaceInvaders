import pygame
import random

class StarfieldBackground:
    """Fondo animado de estrellas para usar en diferentes escenas"""
    
    def __init__(self, screen_width, screen_height, num_stars=100):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.stars = []
        
        # Generar estrellas
        for _ in range(num_stars):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            speed = random.uniform(0.5, 2.0)
            self.stars.append([x, y, speed])
    
    def update(self):
        """Actualiza la posición de las estrellas"""
        for star in self.stars:
            star[1] += star[2]  # Mover hacia abajo
            
            # Reiniciar si sale de la pantalla
            if star[1] > self.screen_height:
                star[1] = 0
                star[0] = random.randint(0, self.screen_width)
    
    def draw(self, screen):
        """Dibuja las estrellas en la pantalla"""
        for star in self.stars:
            # Brillo basado en velocidad
            brightness = int(255 * (star[2] / 2.0))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (int(star[0]), int(star[1])), 2)
