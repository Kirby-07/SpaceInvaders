import pygame
import sys
from src.config import BLACK, WHITE, GREEN, FPS

from src.sprites.player import Player
from src.sprites.enemy import Enemy
from src.sprites.powerup import PowerUp
from src.sprites.boss import Boss
from src.scenes.pause import Pause
from src.starfield import StarfieldBackground
from src.vision_controller import VisionController
import random

class Game:
    def __init__(self, screen, audio_manager):
        self.screen = screen
        self.audio_manager = audio_manager
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font = pygame.font.Font(None, 36)
        
        # Grupos de Sprites
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        
        # Instanciar Jugador
        self.player = Player(self.all_sprites, self.bullets, self.screen_width, self.screen_height, self.audio_manager)
        self.all_sprites.add(self.player)
        
        # Estado del Juego
        self.score = 0
        self.lives = 3
        self.level = 9
        self.max_levels = 10  # Aumentado de 3 a 10 niveles
        
        # Cargar sonidos
        self.explosion_sounds = [
            pygame.mixer.Sound('assets/sounds/explosionCrunch_000.ogg'),
            pygame.mixer.Sound('assets/sounds/explosionCrunch_001.ogg'),
            pygame.mixer.Sound('assets/sounds/explosionCrunch_002.ogg'),
            pygame.mixer.Sound('assets/sounds/explosionCrunch_003.ogg'),
            pygame.mixer.Sound('assets/sounds/explosionCrunch_004.ogg')
        ]
        self.laser_sound = pygame.mixer.Sound('assets/sounds/laserRetro_002.ogg')
        self.powerup_sound = pygame.mixer.Sound('assets/sounds/powerUp1.ogg')
        
        # Fondo de estrellas
        self.starfield = StarfieldBackground(self.screen_width, self.screen_height)
        
        # Controlador de Visión
        self.vision_controller = VisionController()
        
        # Generar Enemigos Iniciales
        self.start_level()

    def start_level(self):
        """Configura los enemigos según el nivel actual."""
        # Limpiar todos los sprites para evitar "fantasmas"
        self.all_sprites.empty()
        self.bullets.empty()
        self.enemies.empty()
        self.enemy_bullets.empty()
        self.powerups.empty()
        
        # Re-añadir al jugador (que no queremos destruir, solo resetear)
        self.all_sprites.add(self.player)
        self.player.rect.centerx = self.screen_width // 2
        self.player.rect.bottom = self.screen_height - 10
        
        # Configuración por nivel (progresivamente más difícil)
        if self.level == 5 or self.level == 10:
            # BOSS FIGHT
            boss_type = 1 if self.level == 5 else 2
            boss = Boss(self.screen_width // 2, 100, boss_type, self.screen_width, self.screen_height, self.audio_manager)
            self.all_sprites.add(boss)
            self.enemies.add(boss)
            return # No generar enemigos normales

        if self.level == 1:
            rows = 3
            cols = 6
            speed = 12
        elif self.level == 2:
            rows = 3
            cols = 8
            speed = 18
        elif self.level == 3:
            rows = 4
            cols = 8
            speed = 24
        elif self.level == 4:
            rows = 4
            cols = 10
            speed = 30
        elif self.level == 6:
            rows = 5
            cols = 10
            speed = 36
        elif self.level == 7:
            rows = 5
            cols = 12
            speed = 42
        elif self.level == 8:
            rows = 6
            cols = 12
            speed = 48
        elif self.level == 9:
            rows = 7
            cols = 12
            speed = 54
        
        # Espaciado reducido para enemigos más pequeños (30x20)
        # Espaciado horizontal: 60px, vertical: 50px
        for row in range(rows):
            for col in range(cols):
                enemy = Enemy(50 + col * 60, 50 + row * 50, self.screen_width, self.screen_height)
                enemy.speed_x = speed
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)

    def run(self):
        """Bucle principal del juego."""
        clock = pygame.time.Clock()
        running = True
        while running:
            # 1. Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.vision_controller.release()
                    pygame.quit()
                    sys.exit()
                
                # Manejo de evento de fin de música para alternar canciones
                if event.type == pygame.USEREVENT + 1:
                    self.audio_manager.handle_music_end()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        # Abrir menú de pausa
                        # Primero dibujamos el estado actual del juego
                        self.screen.fill(BLACK)
                        self.all_sprites.draw(self.screen)
                        
                        # HUD
                        score_text = self.font.render(f"Puntos: {self.score}", True, WHITE)
                        level_text = self.font.render(f"Nivel: {self.level}", True, WHITE)
                        lives_text = self.font.render(f"Vidas: {self.lives}", True, WHITE)
                        
                        self.screen.blit(score_text, (10, 10))
                        self.screen.blit(level_text, (self.screen_width // 2 - 50, 10))
                        self.screen.blit(lives_text, (self.screen_width - 120, 10))
                        
                        # Mostrar menú de pausa
                        pause_menu = Pause(self.screen)
                        pause_action = pause_menu.run()
                        
                        if pause_action == "Continuar":
                            pass  # Continuar el juego
                        elif pause_action == "Configuración":
                            from src.scenes.settings import Settings
                            settings = Settings(self.screen, self.audio_manager)
                            settings.run()
                        elif pause_action == "Reiniciar Nivel":
                            self.start_level()
                        elif pause_action == "Menú Principal":
                            running = False  # Volver al menú principal
            
            # 2. Actualización
            self.starfield.update()
            
            # Procesar visión
            self.vision_controller.process_frame()
            vision_movement, vision_shoot = self.vision_controller.get_command()
            
            # Actualizar sprites individualmente
            self.player.update(vision_movement, vision_shoot)
            self.enemies.update()
            self.bullets.update()
            self.enemy_bullets.update()
            self.powerups.update()
            
            # Boss Attacks
            for enemy in self.enemies:
                if isinstance(enemy, Boss):
                    bullet = enemy.attack()
                    if bullet:
                        self.enemy_bullets.add(bullet)
                        self.all_sprites.add(bullet)
            
            # Verificar Victoria de Nivel
            if len(self.enemies) == 0:
                if self.level < self.max_levels:
                    self.level += 1
                    self.start_level()
                    pygame.time.delay(1000) # Pausa breve entre niveles
                else:
                    # VICTORIA FINAL - Mostrar pantalla de victoria
                    from src.scenes.victory import Victory
                    victory_screen = Victory(self.screen, self.score)
                    victory_screen.run()
                    running = False

            # Colisiones: Balas vs Enemigos (Modificado para Boss)
            hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
            for enemy in hits:
                if isinstance(enemy, Boss):
                    enemy.take_damage(1)
                    if enemy.hp <= 0:
                        self.score += 500
                        enemy.kill()
                        # Drop multiple powerups
                        for _ in range(random.randint(3, 5)):
                            powerup_type = random.choice(['double', 'triple', 'rapid', 'life'])
                            powerup = PowerUp(
                                enemy.rect.centerx + random.randint(-50, 50),
                                enemy.rect.centery + random.randint(-30, 30),
                                powerup_type, 
                                self.screen_height
                            )
                            self.powerups.add(powerup)
                            self.all_sprites.add(powerup)
                else:
                    self.score += 10
                    enemy.kill()
                    # Intentar generar power-up cuando muere el enemigo
                    powerup_type = enemy.drop_powerup()
                    if powerup_type:
                        powerup = PowerUp(enemy.rect.centerx, enemy.rect.centery, powerup_type, self.screen_height)
                        self.all_sprites.add(powerup)
                        self.powerups.add(powerup)
            
            # Colisiones: Jugador vs Balas Enemigas
            if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
                # Sonido de explosión
                sound = random.choice(self.explosion_sounds)
                sound.set_volume(self.audio_manager.sfx_volume)
                sound.play()
                self.lives -= 1
                if self.lives > 0:
                    # Feedback visual: Reiniciar posición del jugador
                    self.player.rect.centerx = self.screen_width // 2
                    self.player.rect.bottom = self.screen_height - 10
                    # Limpiar balas enemigas para evitar muerte instantánea al respawnear
                    self.enemy_bullets.empty()
                    # Pequeña pausa
                    pygame.display.flip()
                    pygame.time.delay(1000)
                else:
                    # GAME OVER - Mostrar pantalla de game over
                    from src.scenes.gameover import GameOver
                    gameover_screen = GameOver(self.screen, self.score, self.level)
                    gameover_screen.run()
                    running = False
                
            # Colisiones: Enemigo vs Jugador (Pierde Vida)
            if pygame.sprite.spritecollide(self.player, self.enemies, False):
                # Sonido de explosión
                sound = random.choice(self.explosion_sounds)
                sound.set_volume(self.audio_manager.sfx_volume)
                sound.play()
                self.lives -= 1
                if self.lives > 0:
                    self.start_level() # Reinicia el nivel actual (o solo posiciones)
                    pygame.time.delay(1000)
                else:
                    # GAME OVER - Mostrar pantalla de game over
                    from src.scenes.gameover import GameOver
                    gameover_screen = GameOver(self.screen, self.score, self.level)
                    gameover_screen.run()
                    running = False

            # Actualizar power-ups
            self.powerups.update()

            # Colisión jugador con power-ups
            powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
            for powerup in powerup_hits:
                self.powerup_sound.set_volume(self.audio_manager.sfx_volume)
                self.powerup_sound.play()
                if powerup.powerup_type == 'life':
                    self.lives += 1
                else:
                    self.player.activate_powerup(powerup.powerup_type)
            
            # 3. Dibujado
            self.screen.fill(BLACK)
            
            # Dibujar fondo de estrellas
            self.starfield.draw(self.screen)
            
            self.all_sprites.draw(self.screen)
            self.enemy_bullets.draw(self.screen)
            
            # Dibujar preview de cámara
            self.vision_controller.draw_preview(self.screen, self.screen_width - 170, self.screen_height - 130, 160, 120)
            
            # Draw Boss Health Bar
            for enemy in self.enemies:
                if isinstance(enemy, Boss):
                    enemy.draw_health_bar(self.screen)
            
            # HUD
            score_text = self.font.render(f"Puntos: {self.score}", True, WHITE)
            level_text = self.font.render(f"Nivel: {self.level}", True, WHITE)
            lives_text = self.font.render(f"Vidas: {self.lives}", True, WHITE)
            
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(level_text, (self.screen_width // 2 - 50, 10))
            self.screen.blit(lives_text, (self.screen_width - 120, 10))
            
            # Mostrar arma activa si no es normal
            if self.player.weapon_type != 'normal':
                weapon_text = self.font.render(f"Arma: {self.player.weapon_type.upper()}", True, GREEN)
                self.screen.blit(weapon_text, (self.screen_width // 2 - 100, 50))
            
            pygame.display.flip()
            clock.tick(FPS)
