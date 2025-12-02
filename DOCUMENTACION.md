# Manual de Usuario y Documentación Técnica - Space Invader

## 1. Guía de Usuario

### 🚀 Introducción
**Space Invader** es una reimaginación moderna del clásico juego de arcade, desarrollada en Python con Pygame. Esta versión incluye gráficos mejorados, música dinámica, batallas contra jefes épicos y un innovador sistema de control por visión artificial que te permite pilotar tu nave usando gestos con tu mano.

### 💻 Requisitos del Sistema
- **Sistema Operativo:** Windows, macOS o Linux.
- **Python:** Versión 3.8 o superior.
- **Cámara Web:** Requerida para el modo de control por visión.
- **Librerías:** `pygame`, `opencv-python`, `mediapipe`.

### 🎮 Cómo Jugar

#### Menú Principal
Navega por el menú usando el **Teclado** (Flechas ↑ ↓ + Enter) o el **Mouse** (Click izquierdo).
- **Jugar:** Inicia la partida.
- **Configuración:** Ajusta el volumen de la música y efectos.
- **Instrucciones:** Repaso rápido de los controles.
- **Salir:** Cierra el juego.

#### Controles de Juego

Tienes dos formas de controlar la nave. Puedes usarlas simultáneamente.

**1. Teclado (Clásico)**
- **Moverse:** Flechas Izquierda (←) y Derecha (→).
- **Disparar:** Barra Espaciadora.
- **Pausa:** Tecla `P` o `ESC`.

**2. Visión Artificial (Cámara)**
El juego detectará tu mano a través de la webcam.
- **Moverse:** Mueve tu mano hacia la izquierda o derecha de la pantalla. La nave seguirá tu movimiento.
- **Disparar:** Levanta tu **dedo índice** (gesto de señalar hacia arriba).
  - *Indicador:* Verás un recuadro en la esquina inferior derecha. Cuando el borde se ponga **VERDE**, significa que estás disparando.

#### Mecánicas de Juego
- **Objetivo:** Destruye a todos los enemigos para avanzar de nivel.
- **Vidas:** Comienzas con 3 vidas. Pierdes una si te toca una bala enemiga o chocas con una nave.
- **Power-ups:** Los enemigos pueden soltar mejoras al morir:
  - 🔵 **Doble:** Disparas 2 balas a la vez.
  - 🟢 **Triple:** Disparas 3 balas en abanico.
  - 🔴 **Rápido:** Aumenta drásticamente tu velocidad de disparo.
  - 💗 **Vida Extra:** Recuperas 1 vida.
- **Jefes (Bosses):** En los niveles 5 y 10 te enfrentarás a naves nodrizas gigantes con mucha vida y ataques especiales.

---

## 2. Documentación Técnica y Educativa

Esta sección está diseñada para explicar **cómo funciona el código internamente**. El objetivo es que entiendas los conceptos de programación de videojuegos aplicados aquí para que puedas replicarlos o modificarlos en el futuro.

### 🏗️ Arquitectura del Proyecto

El proyecto está estructurado de manera **modular**. En lugar de tener un solo archivo gigante con todo el código, dividimos el programa en archivos pequeños, cada uno con una responsabilidad específica. Esto facilita la lectura y el mantenimiento.

#### Estructura de Archivos
*   **`main.py`**: Es el **Punto de Entrada**. Su única función es inicializar las librerías principales y lanzar la primera escena. No contiene lógica del juego.
*   **`src/config.py`**: Contiene las **Constantes Globales** (variables que no cambian). Aquí definimos el ancho de pantalla, colores y FPS. Si quieres cambiar el tamaño del juego, solo modificas este archivo.
*   **`src/game.py`**: El **Corazón del Juego**. Contiene la clase `Game`, que maneja el bucle principal, la creación de enemigos y las reglas.
*   **`src/audio_manager.py`**: Un **Gestor Centralizado** para el sonido. Permite que cualquier parte del juego pida reproducir un sonido sin preocuparse por cargar archivos o volúmenes.
*   **`src/vision_controller.py`**: El cerebro de la **Inteligencia Artificial**. Procesa la imagen de la cámara y la traduce a comandos simples (Izquierda, Derecha, Disparo).

---

### 🧠 Conceptos Clave Implementados

#### 1. El Bucle de Juego (Game Loop)
Es el concepto más importante en videojuegos. Un juego no es estático; es un ciclo infinito que se repite 60 veces por segundo.
En `src/game.py`, el método `run()` implementa este ciclo con tres fases críticas:
1.  **Entrada (Events):** ¿El usuario presionó una tecla? ¿Movió el mouse? ¿La cámara detectó algo?
2.  **Actualización (Update):** Calcular la nueva posición de todo. Si la bala iba a 10px/frame, ahora está 10px más arriba. Si chocó, se borra.
3.  **Dibujado (Draw):** Borrar la pantalla (pintarla de negro) y volver a dibujar todo en sus nuevas posiciones.

#### 2. Programación Orientada a Objetos (POO)
Todo en el juego es un **Objeto**.
*   **Herencia:** `Player`, `Enemy` y `Bullet` heredan de `pygame.sprite.Sprite`. Esto significa que Pygame ya sabe cómo manejarlos (tienen una imagen `image` y una posición `rect`), y nosotros solo agregamos la lógica específica.
*   **Polimorfismo:** Todos tienen un método `update()`, pero cada uno hace algo diferente. Al llamar a `all_sprites.update()`, Pygame ejecuta el código específico de cada objeto automáticamente.

#### 3. Grupos de Sprites
En lugar de manejar una lista de enemigos `[enemigo1, enemigo2...]` y recorrerla manualmente, usamos `pygame.sprite.Group`.
*   **Ventaja:** Permite detección de colisiones ultra-rápida.
*   **Ejemplo:** `pygame.sprite.groupcollide(enemigos, balas, ...)` revisa automáticamente si *cualquier* bala tocó a *cualquier* enemigo, sin que tengamos que escribir dos bucles `for` anidados.

---

### 📚 Explicación Detallada de Clases y Métodos

#### A. Clase `Game` (`src/game.py`)
Es la clase principal que orquesta la partida.

*   **`__init__`**: Prepara el escenario. Crea al jugador, los grupos de sprites y carga los sonidos.
*   **`start_level()`**:
    *   **Lógica:** Define la dificultad. Si el nivel es 1, crea pocos enemigos lentos. Si es 10, crea muchos rápidos.
    *   **Boss:** Si el nivel es 5 o 10, en lugar de crear enemigos normales, instancia un objeto `Boss`.
*   **`run()`**: El bucle infinito.
    *   Llama a `vision_controller.process_frame()` para "ver" al jugador.
    *   Llama a `player.update(vision_movement)` para mover la nave.
    *   Verifica condiciones de victoria (¿Quedan enemigos?) o derrota (¿Vidas < 0?).

#### B. Clase `Player` (`src/sprites/player.py`)
Representa al usuario.

*   **`update(vision_movement, vision_shoot)`**:
    *   Recibe inputs tanto del teclado como de la cámara.
    *   Usa lógica `OR`: Se mueve si presionas la flecha O si la cámara detecta la mano. Esto permite usar ambos controles a la vez.
*   **`shoot()`**:
    *   Controla la cadencia de disparo (`shoot_delay`). Evita que salgan 60 balas por segundo; solo permite una cada 250ms (o 100ms con power-up).
    *   Crea instancias de `Bullet` y las añade a los grupos.

#### C. Clase `VisionController` (`src/vision_controller.py`)
Aquí ocurre la magia de la visión artificial.

*   **`__init__`**: Configura MediaPipe.
    *   `model_complexity=0`: Usamos el modelo más ligero para que el juego no se ponga lento.
*   **`process_frame()`**:
    1.  Lee una imagen de la webcam.
    2.  La invierte (efecto espejo) para que sea intuitivo.
    3.  Busca manos. Si encuentra una:
        *   **Movimiento:** Toma la coordenada X de la muñeca (`WRIST`). Si es < 0.4 (izquierda de la pantalla), mueve a la izquierda.
        *   **Disparo:** Compara la altura (Y) de la punta del dedo índice (`INDEX_FINGER_TIP`) con su nudillo (`INDEX_FINGER_PIP`). En computación gráfica, Y crece hacia abajo. Por tanto, si `TIP.y < PIP.y`, el dedo está levantado.

#### D. Clase `AudioManager` (`src/audio_manager.py`)
Implementa un patrón similar a un **Singleton**.

*   **Problema:** Si cada enemigo carga su propio sonido de explosión, la memoria se llena. Si queremos bajar el volumen, tendríamos que avisarle a cada objeto.
*   **Solución:** El `AudioManager` se crea una sola vez en `main.py` y se pasa a todos. Guarda el volumen global. Cuando cambias el volumen en el menú, actualizas una sola variable y todos los sonidos futuros la leen de ahí.

#### E. Clase `Menu` y `Settings` (`src/scenes/`)
Manejan la Interfaz de Usuario (UI).

*   **Detección de Mouse:**
    *   Calculamos rectángulos (`pygame.Rect`) alrededor de cada texto.
    *   En cada frame, preguntamos `rect.collidepoint(mouse_pos)`. Si es verdadero, cambiamos el color del texto (efecto Hover).
    *   Si hay un click dentro del rectángulo, ejecutamos la acción.

---

### 🚀 Guía para Modificar el Juego

Si quieres experimentar, aquí tienes algunos retos sugeridos:

1.  **Cambiar la velocidad del juego:**
    *   Ve a `src/config.py` y cambia `FPS = 60` a 30 o 120.
    *   O ve a `src/sprites/player.py` y cambia `self.speed = 5` a 10.

2.  **Crear un arma nueva:**
    *   En `Player.shoot()`, agrega una condición `elif self.weapon_type == 'laser_gigante':`.
    *   Crea una bala más grande en `src/sprites/bullet.py`.

3.  **Modificar la dificultad:**
    *   En `Game.start_level()`, cambia la cantidad de filas (`rows`) o la velocidad (`speed`) de los enemigos.

---

### 📝 Conclusión
Este proyecto combina gráficos 2D clásicos con tecnología de visión moderna. La clave es la **separación de responsabilidades**: La cámara no sabe nada del juego, solo dice "Izquierda". El juego no sabe nada de la cámara, solo recibe "Izquierda". Esta independencia hace que el código sea robusto y fácil de expandir.
