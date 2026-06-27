# Sistema de Gestión de Torneos de Tenis 🎾
## Ejercicio de Programación Orientada a Objetos — Python

---

## Estructura del proyecto

```
sistema_tenis/
│
├── main.py                        # Ejemplo de uso (para ver cómo interactúan las clases)
│
├── modelos/
│   ├── equipamiento/
│   │   ├── equipamiento.py        # Clase abstracta base (NO modificar)
│   │   ├── raqueta.py             # ← implementar
│   │   ├── pelota.py              # ← implementar
│   │   └── superficie.py          # ← implementar
│   │
│   ├── personas/
│   │   ├── persona.py             # Clase abstracta base (NO modificar estructura)
│   │   ├── jugador.py             # Clase abstracta (NO modificar estructura)
│   │   ├── jugador_profesional.py # ← implementar
│   │   └── jugador_amateur.py     # ← implementar
│   │
│   ├── torneos/
│   │   ├── torneo.py              # Clase abstracta base (NO modificar estructura)
│   │   └── tipos_torneo.py        # ← implementar (GrandSlam, Masters, Challenger, Amateur)
│   │
│   └── partido.py                 # ← implementar
│
└── tests/
    ├── test_equipamiento.py       # Tests de Raqueta, Pelota, Superficie
    ├── test_jugadores.py          # Tests de JugadorProfesional y JugadorAmateur
    ├── test_torneos.py            # Tests de herencia y polimorfismo en torneos
    └── test_partido.py            # Tests de Partido (integración de todo)
```

---

## Cómo correr los tests

```bash
# Instalar pytest (solo la primera vez)
pip install pytest

# Desde la carpeta sistema_tenis/, correr todos los tests
pytest tests/ -v

# Correr solo un archivo
pytest tests/test_equipamiento.py -v

# Correr tests de una clase específica
pytest tests/test_jugadores.py::TestJugadorProfesional -v
```

---

## Orden de implementación sugerido

Seguí este orden para que cada fase se apoye en la anterior:

```
Fase 1 → equipamiento/raqueta.py
       → equipamiento/pelota.py
       → equipamiento/superficie.py

Fase 2 → personas/persona.py        (validaciones del constructor)
       → personas/jugador.py         (estadísticas, composición)
       → personas/jugador_profesional.py
       → personas/jugador_amateur.py

Fase 3 → torneos/torneo.py          (validaciones, agregar_jugador)
       → torneos/tipos_torneo.py     (validar_jugador en cada subclase)

Fase 4 → partido.py                 (registrar_set, finalizar_partido)

Fase 5 → main.py                    (integrar todo y ver que funcione)
```

---

## Conceptos clave que vas a practicar

| Concepto | Dónde aparece |
|---|---|
| **Composición** | `Jugador` TIENE `Raqueta` y `Pelota` |
| **Herencia** | `JugadorProfesional` ES-UN `Jugador` ES-UNA `Persona` |
| **Polimorfismo** | `get_puntos_para_ganador()` se comporta diferente en cada torneo |
| **Encapsulamiento** | Atributos con `_` protegidos, acceso via properties y métodos |
| **Métodos abstractos** | `Torneo` define el contrato, subclases lo implementan |
| **Validaciones** | `ValueError` con mensajes descriptivos en constructores |
| **Testing** | Un test por concepto, fixtures para reutilizar objetos |
