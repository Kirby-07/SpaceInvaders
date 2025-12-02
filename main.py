import pygame
import sys
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, BLACK

from src.audio_manager import audio_manager
from src.scenes.splash import Splash
from src.scenes.menu import Menu
from src.scenes.settings import Settings
from src.game import Game
from src.scenes.instructions import Instructions

def main():
    # Inicializar Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Obtener información de la pantalla
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    
    # Configurar pantalla en modo pantalla completa
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption(TITLE)
    
    # Mostrar pantalla de Splash al inicio
    splash = Splash(screen)
    splash.run()
    
    # Iniciar música del menú
    audio_manager.play_music()
    
    while True:
        # 1. Mostrar Menú
        menu = Menu(screen, audio_manager)
        selection = menu.run()
        
        # 2. Manejar Selección
        if selection == "Jugar":
            game = Game(screen, audio_manager)
            game.run()
            # Reiniciar música del menú al volver
            audio_manager.play_music()
        elif selection == "Configuración":
            settings = Settings(screen, audio_manager)
            settings.run()
        elif selection == "Instrucciones":
            instructions = Instructions(screen)
            instructions.run()
        elif selection == "Salir":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
