import pygame
import sys
from src.config import WHITE, BLACK, FPS

class Pause:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font_title = pygame.font.Font(None, 74)
        self.font_option = pygame.font.Font(None, 50)
        self.options = ["Continuar", "Configuración", "Reiniciar Nivel", "Menú Principal"]
        self.selected_index = 0
        
        # Calcular rectángulos de opciones
        self.option_rects = []
        self.calculate_option_rects()
        
    def calculate_option_rects(self):
        """Calcula las posiciones y rectángulos de las opciones"""
        options_start_y = self.screen_height * 0.5
        option_spacing = 60
        self.option_rects = []
        
        for i, option in enumerate(self.options):
            option_surface = self.font_option.render(option, True, WHITE)
            option_rect = option_surface.get_rect(center=(self.screen_width // 2, options_start_y + i * option_spacing))
            self.option_rects.append(option_rect)
        
    def handle_input(self):
        """Maneja la navegación del menú de pausa con teclado y mouse."""
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
            
            # Click del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(mouse_pos):
                            return self.options[i]
            
            # Teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_index]
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    return "Continuar"
        return None

    def draw(self):
        """Dibuja el menú de pausa en pantalla."""
        # Overlay semi-transparente
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Título
        title_surface = self.font_title.render("PAUSA", True, WHITE)
        title_y = self.screen_height * 0.3
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, title_y))
        self.screen.blit(title_surface, title_rect)
        
        # Opciones con efecto hover
        for i, (option, rect) in enumerate(zip(self.options, self.option_rects)):
            if i == self.selected_index:
                color = WHITE
                font_hover = pygame.font.Font(None, 55)
                option_surface = font_hover.render(option, True, color)
            else:
                color = (100, 100, 100)
                option_surface = self.font_option.render(option, True, color)
            
            option_rect = option_surface.get_rect(center=rect.center)
            self.screen.blit(option_surface, option_rect)
        
        # Texto de ayuda
        help_font = pygame.font.Font(None, 30)
        help_text = help_font.render("Presiona P o ESC para continuar", True, (150, 150, 150))
        help_rect = help_text.get_rect(center=(self.screen_width // 2, self.screen_height * 0.85))
        self.screen.blit(help_text, help_rect)
            
        pygame.display.flip()

    def run(self):
        """Bucle principal del menú de pausa."""
        clock = pygame.time.Clock()
        while True:
            action = self.handle_input()
            if action:
                return action
            
            self.draw()
            clock.tick(FPS)
