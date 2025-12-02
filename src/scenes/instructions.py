import pygame
import sys
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, FPS

class Instructions:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font_title = pygame.font.Font(None, 64)
        self.font_text = pygame.font.Font(None, 32)
        
    def draw(self):
        self.screen.fill(BLACK)
        
        # Título (centrado verticalmente)
        title = self.font_title.render("INSTRUCCIONES", True, WHITE)
        title_y = self.screen_height * 0.15  # 15% desde arriba
        title_rect = title.get_rect(center=(self.screen_width // 2, title_y))
        self.screen.blit(title, title_rect)
        
        # Textos
        lines = [
            "Objetivo: Destruye a los invasores antes de que lleguen abajo.",
            "",
            "--- CONTROLES TECLADO ---",
            "Moverse: Flechas Izquierda / Derecha",
            "Disparar: Barra Espaciadora",
            "Pausar: P o ESC",
            "",
            "--- CONTROLES VISIÓN (CÁMARA) ---",
            "Moverse: Mueve tu mano a los lados",
            "Disparar: Levanta el dedo índice (Gesto 'ONE')",
            "",
            "Presiona ESC para volver al menú"
        ]
        
        # Calcular posición inicial centrada
        content_start_y = self.screen_height * 0.3  # Comienza al 30% de la altura
        line_spacing = 35
        
        for i, line in enumerate(lines):
            text = self.font_text.render(line, True, WHITE)
            rect = text.get_rect(center=(self.screen_width // 2, content_start_y + i * line_spacing))
            self.screen.blit(text, rect)
            
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return # Volver al menú
            
            self.draw()
            clock.tick(FPS)
