import pygame

class AudioManager:
    """Administrador global de audio para el juego"""
    
    def __init__(self):
        self.music_volume = 0.3  # 30%
        self.sfx_volume = 0.5    # 50%
        
        self.music_tracks = [
            'assets/sounds/meet-the-princess.wav',
            'assets/sounds/in-the-wreckage.wav'
        ]
        self.current_track_index = 0
        self.music_playing = False
        
    def set_music_volume(self, volume):
        """Establece el volumen de la música (0.0 a 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        """Establece el volumen de los efectos de sonido (0.0 a 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def play_music(self, loop=True):
        """Inicia la reproducción de música"""
        if not self.music_playing:
            pygame.mixer.music.load(self.music_tracks[self.current_track_index])
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1 if loop else 0)
            self.music_playing = True
            # Configurar evento para cuando termine la canción
            pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
    
    def stop_music(self):
        """Detiene la reproducción de música"""
        pygame.mixer.music.stop()
        self.music_playing = False
    
    def next_track(self):
        """Cambia a la siguiente canción"""
        self.current_track_index = (self.current_track_index + 1) % len(self.music_tracks)
        if self.music_playing:
            pygame.mixer.music.load(self.music_tracks[self.current_track_index])
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
    
    def handle_music_end(self):
        """Maneja el evento de fin de canción para alternar"""
        self.next_track()

# Instancia global del administrador de audio
audio_manager = AudioManager()
