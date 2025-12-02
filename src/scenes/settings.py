import pygame
import sys
from src.config import WHITE, BLACK, GREEN, FPS

class Settings:
    def __init__(self, screen, audio_manager):
        self.screen = screen
        self.audio_manager = audio_manager
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font_title = pygame.font.Font(None, 60)
        self.font_option = pygame.font.Font(None, 40)
        
        self.selected_index = 0
        self.options = ["Música", "Efectos", "Volver"]
        
        # Rectángulos para detección de mouse
        self.music_bar_rect = None
        self.sfx_bar_rect = None
        self.back_button_rect = None
        self.dragging = None  # None, 'music', o 'sfx'
        
    def handle_input(self):
        """Maneja la navegación y ajustes del menú de configuración"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Detectar hover en botón Volver
        if self.back_button_rect and self.back_button_rect.collidepoint(mouse_pos):
            self.selected_index = 2
        # Detectar hover en barras
        elif self.music_bar_rect and self.music_bar_rect.collidepoint(mouse_pos):
            self.selected_index = 0
        elif self.sfx_bar_rect and self.sfx_bar_rect.collidepoint(mouse_pos):
            self.selected_index = 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Click en barras de volumen
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    if self.music_bar_rect and self.music_bar_rect.collidepoint(mouse_pos):
                        self.dragging = 'music'
                        self.adjust_volume_from_mouse(mouse_pos, 'music')
                    elif self.sfx_bar_rect and self.sfx_bar_rect.collidepoint(mouse_pos):
                        self.dragging = 'sfx'
                        self.adjust_volume_from_mouse(mouse_pos, 'sfx')
                    elif self.back_button_rect and self.back_button_rect.collidepoint(mouse_pos):
                        return "Volver"
            
            # Soltar mouse
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = None
            
            # Arrastrar
            if event.type == pygame.MOUSEMOTION:
                if self.dragging == 'music':
                    self.adjust_volume_from_mouse(mouse_pos, 'music')
                elif self.dragging == 'sfx':
                    self.adjust_volume_from_mouse(mouse_pos, 'sfx')
            
            # Teclado (mantener compatibilidad)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    if self.selected_index == 2 or event.key == pygame.K_ESCAPE:
                        return "Volver"
                elif event.key == pygame.K_LEFT:
                    if self.selected_index == 0:
                        self.audio_manager.set_music_volume(self.audio_manager.music_volume - 0.1)
                    elif self.selected_index == 1:
                        self.audio_manager.set_sfx_volume(self.audio_manager.sfx_volume - 0.1)
                elif event.key == pygame.K_RIGHT:
                    if self.selected_index == 0:
                        self.audio_manager.set_music_volume(self.audio_manager.music_volume + 0.1)
                    elif self.selected_index == 1:
                        self.audio_manager.set_sfx_volume(self.audio_manager.sfx_volume + 0.1)
        return None
    
    def adjust_volume_from_mouse(self, mouse_pos, volume_type):
        """Ajusta el volumen basado en la posición del mouse en la barra"""
        if volume_type == 'music' and self.music_bar_rect:
            rect = self.music_bar_rect
            relative_x = mouse_pos[0] - rect.x
            volume = max(0.0, min(1.0, relative_x / rect.width))
            self.audio_manager.set_music_volume(volume)
        elif volume_type == 'sfx' and self.sfx_bar_rect:
            rect = self.sfx_bar_rect
            relative_x = mouse_pos[0] - rect.x
            volume = max(0.0, min(1.0, relative_x / rect.width))
            self.audio_manager.set_sfx_volume(volume)
    
    def draw(self):
        """Dibuja el menú de configuración"""
        self.screen.fill(BLACK)
        
        # Título
        title_surface = self.font_title.render("Configuración de Audio", True, WHITE)
        title_y = self.screen_height * 0.2
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, title_y))
        self.screen.blit(title_surface, title_rect)
        
        # Opciones con barras de volumen
        options_start_y = self.screen_height * 0.4
        option_spacing = 80
        
        for i, option in enumerate(self.options):
            y_pos = options_start_y + i * option_spacing
            color = GREEN if i == self.selected_index else WHITE
            
            if option == "Música":
                # Texto
                text = f"Música: {int(self.audio_manager.music_volume * 100)}%"
                text_surface = self.font_option.render(text, True, color)
                text_rect = text_surface.get_rect(center=(self.screen_width // 2, y_pos))
                self.screen.blit(text_surface, text_rect)
                
                # Barra de volumen
                bar_width = 300
                bar_height = 20
                bar_x = (self.screen_width - bar_width) // 2
                bar_y = y_pos + 40
                
                self.music_bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
                
                # Fondo de la barra
                pygame.draw.rect(self.screen, (50, 50, 50), self.music_bar_rect)
                # Relleno según volumen
                fill_width = int(bar_width * self.audio_manager.music_volume)
                pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, fill_width, bar_height))
                # Borde
                pygame.draw.rect(self.screen, WHITE, self.music_bar_rect, 2)
                
            elif option == "Efectos":
                # Texto
                text = f"Efectos: {int(self.audio_manager.sfx_volume * 100)}%"
                text_surface = self.font_option.render(text, True, color)
                text_rect = text_surface.get_rect(center=(self.screen_width // 2, y_pos))
                self.screen.blit(text_surface, text_rect)
                
                # Barra de volumen
                bar_width = 300
                bar_height = 20
                bar_x = (self.screen_width - bar_width) // 2
                bar_y = y_pos + 40
                
                self.sfx_bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
                
                # Fondo de la barra
                pygame.draw.rect(self.screen, (50, 50, 50), self.sfx_bar_rect)
                # Relleno según volumen
                fill_width = int(bar_width * self.audio_manager.sfx_volume)
                pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, fill_width, bar_height))
                # Borde
                pygame.draw.rect(self.screen, WHITE, self.sfx_bar_rect, 2)
            else:
                # Botón "Volver"
                if i == self.selected_index:
                    font_hover = pygame.font.Font(None, 45)
                    text_surface = font_hover.render(option, True, color)
                else:
                    text_surface = self.font_option.render(option, True, color)
                text_rect = text_surface.get_rect(center=(self.screen_width // 2, y_pos))
                self.back_button_rect = text_rect
                self.screen.blit(text_surface, text_rect)
        
        # Instrucciones
        help_text = "Haz click en las barras o usa ← → | ENTER o ESC para volver"
        help_surface = self.font_option.render(help_text, True, (150, 150, 150))
        help_rect = help_surface.get_rect(center=(self.screen_width // 2, self.screen_height * 0.85))
        self.screen.blit(help_surface, help_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Bucle principal del menú de configuración"""
        clock = pygame.time.Clock()
        while True:
            action = self.handle_input()
            if action == "Volver":
                return
            
            self.draw()
            clock.tick(FPS)
