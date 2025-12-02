import pygame
import sys
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, FPS
from src.starfield import StarfieldBackground

class Menu:
    def __init__(self, screen, audio_manager):
        self.screen = screen
        self.audio_manager = audio_manager
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font_title = pygame.font.Font(None, 74)
        self.font_option = pygame.font.Font(None, 50)
        self.options = ["Jugar", "Configuración", "Instrucciones", "Salir"]
        self.selected_index = 0
        
        # Fondo de estrellas
        self.starfield = StarfieldBackground(self.screen_width, self.screen_height)
        
        # Calcular rectángulos de opciones para detección de mouse
        self.option_rects = []
        self.calculate_option_rects()
        
    def calculate_option_rects(self):
        """Calcula las posiciones y rectángulos de las opciones"""
        options_start_y = self.screen_height * 0.45
        option_spacing = 60
        self.option_rects = []
        
        for i, option in enumerate(self.options):
            option_surface = self.font_option.render(option, True, WHITE)
            option_rect = option_surface.get_rect(center=(self.screen_width // 2, options_start_y + i * option_spacing))
            self.option_rects.append(option_rect)
        
    def handle_input(self):
        """Maneja la navegación del menú con teclado y mouse."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Detectar hover del mouse
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                self.selected_index = i
                break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Manejo de evento de fin de música para alternar canciones
            if event.type == pygame.USEREVENT + 1:
                self.audio_manager.handle_music_end()
            
            # Click del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(mouse_pos):
                            return self.options[i]
            
            # Teclado (mantener compatibilidad)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_index]
        return None

    def draw(self):
        """Dibuja el menú en pantalla."""
        self.screen.fill(BLACK)
        
        # Dibujar fondo de estrellas
        self.starfield.draw(self.screen)
        
        # Dibujar Título
        title_surface = self.font_title.render("Space Invader", True, WHITE)
        title_y = self.screen_height * 0.25
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, title_y))
        self.screen.blit(title_surface, title_rect)
        
        # Dibujar Opciones con efecto hover
        for i, (option, rect) in enumerate(zip(self.options, self.option_rects)):
            # Color según selección
            if i == self.selected_index:
                color = WHITE
                # Escala ligeramente más grande cuando está seleccionado
                font_hover = pygame.font.Font(None, 55)
                option_surface = font_hover.render(option, True, color)
            else:
                color = (100, 100, 100)
                option_surface = self.font_option.render(option, True, color)
            
            option_rect = option_surface.get_rect(center=rect.center)
            self.screen.blit(option_surface, option_rect)
            
        pygame.display.flip()

    def run(self):
        """Bucle principal del menú."""
        clock = pygame.time.Clock()
        while True:
            action = self.handle_input()
            if action:
                return action
            
            self.starfield.update()
            self.draw()
            clock.tick(FPS)
