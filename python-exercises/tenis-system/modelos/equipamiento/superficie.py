from modelos.equipamiento.equipamiento import Equipamiento


class Superficie(Equipamiento):
    """
    Superficie de juego. Usada por Partido y Torneo.
    La velocidad y el bote afectan el estilo de juego.

    Tipos válidos: Pasto | Arcilla | Cemento Duro
    """

    TIPOS_VALIDOS = {"Pasto", "Arcilla", "Cemento Duro"}

    def __init__(self, tipo: str, velocidad: float, bote: float):
        super().__init__("Superficie")
        # TODO: validar que tipo esté en TIPOS_VALIDOS
        #       lanzar ValueError si no cumple
        self._tipo_superficie = tipo
        self._velocidad = velocidad
        self._bote = bote

    @property
    def tipo(self) -> str:
        return self._tipo_superficie

    @property
    def velocidad(self) -> float:
        return self._velocidad

    @property
    def bote(self) -> float:
        return self._bote

    def get_caracteristicas(self) -> str:
        # TODO: describir la superficie según su velocidad
        #   velocidad > 1.2  → "rápida"
        #   velocidad < 0.8  → "lenta"
        #   en el medio      → "media"
        # Ejemplo retorno: "Pasto (rápida)"
        pass

    def get_descripcion(self) -> str:
        return self.get_caracteristicas()
