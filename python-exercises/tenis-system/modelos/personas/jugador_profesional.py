from modelos.personas.jugador import Jugador
from modelos.equipamiento.raqueta import Raqueta
from modelos.equipamiento.pelota import Pelota


class JugadorProfesional(Jugador):
    """
    Hereda de Jugador.
    Tiene ranking ATP/WTA, ingresos y participa en torneos profesionales.

    Restricciones:
      - edad mínima: 15 años
      - ranking:     entero > 0
    """

    EDAD_MINIMA = 15

    def __init__(
        self,
        nombre: str,
        edad: int,
        pais: str,
        ranking: int,
        superficie_favorita: str,
        raqueta: Raqueta,
        pelota: Pelota,
        ingresos: float = 0.0,
    ):
        super().__init__(nombre, edad, pais, superficie_favorita, raqueta, pelota)
        # TODO: validar que edad >= EDAD_MINIMA → ValueError("La edad mínima para un profesional es 15 años")
        # TODO: validar que ranking > 0         → ValueError("El ranking debe ser mayor a 0")
        self._ranking = ranking
        self._ingresos = ingresos
        self._puntos_acumulados = 0

    # -------------------------------------------------------------------------
    # Ranking y puntos
    # -------------------------------------------------------------------------

    @property
    def ranking(self) -> int:
        return self._ranking

    def set_ranking(self, nuevo_ranking: int) -> None:
        # TODO: validar que nuevo_ranking > 0
        self._ranking = nuevo_ranking

    def agregar_puntos(self, puntos: int) -> None:
        # TODO: acumular en _puntos_acumulados
        pass

    def get_puntos_acumulados(self) -> int:
        return self._puntos_acumulados

    def compara_ranking(self, otro: "JugadorProfesional") -> int:
        # TODO: comparar por _puntos_acumulados
        #   retornar  1 si self tiene más puntos
        #   retornar -1 si otro tiene más puntos
        #   retornar  0 si son iguales
        pass

    # -------------------------------------------------------------------------
    # Ingresos
    # -------------------------------------------------------------------------

    @property
    def ingresos(self) -> float:
        return self._ingresos

    def agregar_ingresos(self, monto: float) -> None:
        # TODO: sumar monto a _ingresos
        pass

    # -------------------------------------------------------------------------
    # Representación
    # -------------------------------------------------------------------------

    def get_descripcion(self) -> str:
        return f"{self._nombre} (Ranking #{self._ranking})"

    def get_estadisticas(self) -> str:
        # TODO: retornar string con nombre, victorias, derrotas, win rate y puntos
        # Ejemplo:
        #   === Rafael Nadal ===
        #   Victorias: 2 | Derrotas: 1 | Win Rate: 66.67%
        #   Puntos ATP: 3000 | Ingresos: $50000000
        pass
