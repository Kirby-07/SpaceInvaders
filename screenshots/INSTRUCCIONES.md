# Guía para Capturar Screenshots

Necesito que captures las siguientes pantallas del juego:

## Capturas Necesarias:

1. **menu.png** - Menú Principal
   - Ejecuta el juego
   - En la pantalla de inicio, presiona una tecla
   - Captura el menú principal
   - Guarda como: `screenshots/menu.png`

2. **gameplay.png** - Gameplay con Visión
   - Selecciona "Jugar"
   - Espera a que aparezcan enemigos
   - Muestra tu mano a la cámara (para que se vea el recuadro de visión)
   - Captura la pantalla durante el juego
   - Guarda como: `screenshots/gameplay.png`

3. **boss.png** - Batalla contra Boss
   - En el juego, presiona `Ctrl+C` para salir
   - Edita `src/game.py`, línea 35: cambia `self.level = 1` a `self.level = 5`
   - Ejecuta el juego nuevamente
   - Selecciona "Jugar"
   - Captura la batalla contra el boss
   - Guarda como: `screenshots/boss.png`
   - **IMPORTANTE:** Después de la captura, revierte el cambio (level = 1)

## Cómo Capturar (Windows):
- Presiona `Windows + Shift + S` para abrir la herramienta de recorte
- Selecciona el área del juego
- La imagen se guarda en el portapapeles
- Abre Paint, pega (`Ctrl+V`) y guarda en la carpeta `screenshots`

Cuando tengas las 3 imágenes, avísame para actualizar el README.md automáticamente.
