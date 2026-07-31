# Dungeon of Shadows

Mini RPG de mazmorras hecho con `pygame`, basado en las ideas de `sample_code.py`
(personajes, armas, armaduras, combate por turnos y puertas con encuentros aleatorios),
llevado a una interfaz gráfica jugable con mouse y teclado.

## Cómo jugar

Solo necesitas ejecutar un script, no hace falta instalar nada a mano:

```bash
./run.sh
```

La primera vez crea automáticamente un entorno virtual (`venv/`) e instala `pygame`.
Las siguientes veces arranca el juego directamente.

Si preferís hacerlo manualmente:

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python main.py
```

## Controles

- Todo se maneja con el mouse (botones en pantalla).
- `ENTER` en el menú principal para empezar.
- `ESC` para volver atrás / salir según la pantalla.

## Cómo se juega

1. Elegís tu personaje: **Espadachín** (resistente) o **Pícaro** (rápido y letal).
2. Explorás la mazmorra piso a piso, eligiendo entre 3 puertas con distinto riesgo/recompensa.
3. Cada puerta puede llevarte a un cofre, un pasillo vacío, un enemigo o eventos especiales.
4. En combate podés **Atacar**, **Usar poción** o **Huir**, por turnos.
5. Tras varios pisos aparece el **Rey Goblin**: derrotalo para ganar la partida.

## Estructura del proyecto

```
game/
├── assets/              # Carpetas reservadas para audio/fuentes/imágenes futuras
├── src/
│   ├── config.py        # Constantes y colores
│   ├── data.py          # Bestiario, ítems, botín y lógica de puertas
│   ├── game.py           # Bucle principal y máquina de estados
│   ├── entities/         # Personaje, Jugador, Enemigo, Arma, Armadura
│   ├── states/            # Menú, selección de personaje, mazmorra, combate, fin de partida
│   └── ui/                 # Botones, barras de vida, fondo, fuentes
├── main.py                # Punto de entrada
├── run.sh                  # Script de arranque (crea el venv la primera vez)
└── requirements.txt
```

El juego no depende de ningún archivo de imagen o audio externo: todos los gráficos
(fondos de piedra, paneles, barras) se dibujan por código con `pygame`, así que
funciona apenas lo clonás y ejecutás.
