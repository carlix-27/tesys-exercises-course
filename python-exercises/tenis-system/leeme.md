Seguramente vas a tener que tirar estos comandos:

```bash
pip install pytest
cd sistema_tenis 
pytest tests/ -v
```

El sistema_tenis, seria el nombre donde haces toda la logica, es un folder.

Es muy probable que al principio se rompa todo, pero porque tenes que implementar.

A nivel estructura en tu proyecto, podes estructurarlo asi: 

```
sistema_tenis/
├── main.py
├── modelos/
│   ├── equipamiento/   → raqueta.py, pelota.py, superficie.py
│   ├── personas/       → persona.py, jugador.py, jugador_profesional.py, jugador_amateur.py
│   ├── torneos/        → torneo.py, tipos_torneo.py
│   └── partido.py
└── tests/
    ├── test_equipamiento.py
    ├── test_jugadores.py
    ├── test_torneos.py
    └── test_partido.py
```