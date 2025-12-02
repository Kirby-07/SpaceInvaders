# 🚀 Space Invader - Vision Control Edition

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-Community-brightgreen?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-Vision-red?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-ML-blue?style=for-the-badge)

> **Una reimaginación del clásico arcade implementando visión artificial para controlar la nave mediante gestos de la mano en tiempo real.**

---

## 📋 Descripción

Este proyecto fue desarrollado como parte de la asignatura de **Computación Gráfica** por un estudiante de Ingeniería en Sistemas.

El objetivo principal es demostrar la integración de un **Game Loop** tradicional (usando Pygame) con un **pipeline de procesamiento de imágenes** (usando OpenCV y MediaPipe) sin sacrificar el rendimiento. El juego permite al usuario elegir entre el control clásico por teclado o pilotar la nave moviendo su mano frente a la cámara web.

## ✨ Características Principales

*   **🕹️ Control Híbrido:** Juega con teclado o usa tu cámara web para una experiencia sin contacto.
*   **🧠 IA de Detección:** Algoritmo capaz de detectar la posición de la muñeca para el movimiento y el gesto del dedo índice para disparar.
*   **👾 Sistema de Progresión:** 10 Niveles con dificultad incremental.
*   **💀 Batallas contra Jefes:** Enfrentamientos únicos contra Naves Nodrizas en los niveles 5 y 10.
*   **⚡ Power-ups:** Mejoras de disparo (Doble, Triple, Rápido) y Vida Extra.
*   **🏗️ Arquitectura Modular:** Código estructurado profesionalmente, separando lógica, vista y controladores.

---

## 📸 Capturas de Pantalla

| Menú Principal | Gameplay (Visión) | Batalla Boss |
|:---:|:---:|:---:|
| *[Inserta aquí tu imagen]* | *[Inserta aquí tu imagen]* | *[Inserta aquí tu imagen]* |

> *Nota: Reemplaza estos textos con capturas reales de tu juego para hacerlo más atractivo en GitHub.*

---

## 🛠️ Instalación y Ejecución

Sigue estos pasos para correr el juego en tu máquina local.

### Prerrequisitos
*   Python 3.8 o superior.
*   Una cámara web (para el modo visión).

### Pasos

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/TU_USUARIO/space-invader-vision.git
    cd space-invader-vision
    ```

2.  **Crear un entorno virtual (Opcional pero recomendado):**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar el juego:**
    ```bash
    python main.py
    ```

---

## 🎮 Guía de Controles

El juego detecta automáticamente ambos métodos de entrada simultáneamente.

| Acción | ⌨️ Teclado (Clásico) | 📷 Visión Artificial (Cámara) |
| :--- | :--- | :--- |
| **Mover Izquierda** | Flecha Izquierda (`←`) | Mueve tu mano hacia la **izquierda** de la pantalla. |
| **Mover Derecha** | Flecha Derecha (`→`) | Mueve tu mano hacia la **derecha** de la pantalla. |
| **Disparar** | Barra Espaciadora | Levanta tu **dedo índice** (Gesto de señalar ☝️). |
| **Pausa** | Tecla `P` o `ESC` | *N/A* |

### Indicadores Visuales (Modo Cámara)
En la esquina inferior derecha verás una vista previa de lo que ve la cámara:
*   **Borde Blanco:** Mano detectada, sin disparo.
*   **Borde Verde + Texto "DISPARANDO":** Gesto de disparo reconocido exitosamente.

---

## 📂 Estructura del Proyecto

```text
space-invader-vision/
├── assets/                 # Recursos (Imágenes y Sonidos)
├── src/                    # Código Fuente
│   ├── scenes/             # Gestor de pantallas (Menú, Juego, Game Over)
│   ├── sprites/            # Clases de entidades (Jugador, Enemigos, Balas)
│   ├── audio_manager.py    # Controlador de sonido (Singleton)
│   ├── config.py           # Constantes globales
│   ├── game.py             # Lógica principal del juego
│   └── vision_controller.py # Lógica de OpenCV y MediaPipe
├── main.py                 # Punto de entrada
└── requirements.txt        # Dependencias del proyecto