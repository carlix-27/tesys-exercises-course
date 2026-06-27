from abc import abstractmethod
from modelos.personas.persona import Persona
from modelos.equipamiento.raqueta import Raqueta
from modelos.equipamiento.pelota import Pelota


class Jugador(Persona):
    """
    Clase abstracta. Hereda de Persona.
    Define el contrato para cualquier jugador de tenis.

    COMPOSICIÓN: Jugador TIENE una Raqueta y una Pelota.
    """

    def __init__(
        self,
        nombre: str,
        edad: int,
        pais: str,
        superficie_favorita: str,
        raqueta: Raqueta,
        pelota: Pelota,
    ):
        super().__init__(nombre, edad, pais)
        # TODO: validar que raqueta no sea None → ValueError("La raqueta no puede ser None")
        # TODO: validar que pelota no sea None  → ValueError("La pelota no puede ser None")
        self._superficie_favorita = superficie_favorita
        self._raqueta = raqueta
        self._pelota = pelota
        self._victorias = 0
        self._derrotas = 0
        # Clave: nombre de superficie → {"victorias": int, "derrotas": int}
        self._stats_por_superficie: dict = {}

    # -------------------------------------------------------------------------
    # Equipamiento (composición)
    # -------------------------------------------------------------------------

    def get_raqueta(self) -> Raqueta:
        return self._raqueta

    def set_raqueta(self, raqueta: Raqueta) -> None:
        # TODO: validar que raqueta no sea None
        self._raqueta = raqueta

    def get_pelota(self) -> Pelota:
        return self._pelota

    def set_pelota(self, pelota: Pelota) -> None:
        # TODO: validar que pelota no sea None
        self._pelota = pelota

    @property
    def superficie_favorita(self) -> str:
        return self._superficie_favorita

    # -------------------------------------------------------------------------
    # Estadísticas
    # -------------------------------------------------------------------------

    def registrar_victoria(self, contra: "Jugador") -> None:
        # TODO: incrementar _victorias
        pass

    def registrar_derrota(self, contra: "Jugador") -> None:
        # TODO: incrementar _derrotas
        pass

    def get_victorias(self) -> int:
        return self._victorias

    def get_derrotas(self) -> int:
        return self._derrotas

    def get_win_rate(self) -> float:
        # TODO: calcular (victorias / total) * 100
        #       retornar 0.0 si no hay partidos jugados
        #       redondear a 2 decimales
        pass

    def registrar_estadistica_por_superficie(self, superficie: str, es_victoria: bool) -> None:
        # TODO: si la superficie no existe en el dict, inicializarla con victorias=0, derrotas=0
        #       luego sumar según es_victoria
        pass

    def get_estadisticas_por_superficie(self, superficie: str) -> dict:
        # TODO: retornar {"victorias": int, "derrotas": int, "win_rate": float}
        #       si no hay registros para esa superficie, retornar todo en cero
        pass

    # -------------------------------------------------------------------------
    # Métodos abstractos
    # -------------------------------------------------------------------------

    @abstractmethod
    def get_descripcion(self) -> str:
        pass

    @abstractmethod
    def get_estadisticas(self) -> str:
        pass
