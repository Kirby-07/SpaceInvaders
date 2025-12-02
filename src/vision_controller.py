import cv2
import mediapipe as mp
import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT

class VisionController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,  # Modelo más ligero para mejor rendimiento
            min_detection_confidence=0.5, # Bajamos un poco para detectar más fácil
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Inicializar cámara
        self.cap = cv2.VideoCapture(0)
        
        # Estado del controlador
        self.hand_x = 0.5
        self.is_shooting = False
        self.active = True
        
        if not self.cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
            self.active = False

    def process_frame(self):
        """Captura un frame y procesa la detección de manos"""
        if not self.active:
            return

        success, image = self.cap.read()
        if not success:
            return

        # Espejo horizontal
        image = cv2.flip(image, 1)
        
        # Convertir a RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Procesar
        results = self.hands.process(image_rgb)
        
        self.is_shooting = False # Resetear estado
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 1. Movimiento: Usar la muñeca
                wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                self.hand_x = wrist.x
                
                # 2. Disparo: Dedo índice levantado
                # Comparamos la altura (Y) de la punta del dedo con el nudillo (PIP)
                # En coordenadas de imagen, Y crece hacia abajo.
                # Si TIP < PIP, el dedo está hacia arriba.
                index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]
                
                if index_tip.y < index_pip.y:
                    self.is_shooting = True
                
                # Dibujar esqueleto para feedback visual
                self.mp_draw.draw_landmarks(
                    image, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    self.mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                )
        
        self.current_frame = image

    def get_command(self):
        """Retorna comandos de movimiento y acción"""
        if not self.active:
            return None, False

        movement = None
        
        # Zonas de movimiento (ajustadas para ser más cómodas)
        if self.hand_x < 0.4:
            movement = 'LEFT'
        elif self.hand_x > 0.6:
            movement = 'RIGHT'
        
        return movement, self.is_shooting

    def draw_preview(self, screen, x, y, width, height):
        """Dibuja vista previa"""
        if not self.active or not hasattr(self, 'current_frame'):
            return
            
        frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        frame = cv2.flip(frame, 0)
        
        pygame_surface = pygame.surfarray.make_surface(frame)
        pygame_surface = pygame.transform.scale(pygame_surface, (width, height))
        
        # Borde
        color = (0, 255, 0) if self.is_shooting else (255, 255, 255)
        pygame.draw.rect(screen, color, (x-2, y-2, width+4, height+4), 2)
        screen.blit(pygame_surface, (x, y))
        
        # Texto de estado
        if self.is_shooting:
            font = pygame.font.Font(None, 24)
            text = font.render("DISPARANDO", True, (0, 255, 0))
            screen.blit(text, (x, y - 20))

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
